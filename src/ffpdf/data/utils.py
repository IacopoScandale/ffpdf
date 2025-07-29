import glob
import json
import os
import sys
import tempfile
from math import gcd
from pathlib import Path
from typing import NoReturn

import ffmpeg
from PIL import Image, UnidentifiedImageError
from PyPDF2 import PdfReader

from .strings import (
    DIR_TMP,
    FILE_COUNTER_JSON,
    SEP_DIM,
    SEP_RATIO,
)


def is_image(filepath: str | Path) -> bool:
    """
    Returns `True` whether `filepath` is an image file (i.e. its suffix
    is in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}); `False` otherwise
    """
    if isinstance(filepath, str):
        filepath: Path = Path(filepath)
    return filepath.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


def flush_tmp_dir():
    """
    Removes all temporary files in `DIR_TMP` directory
    """
    for file in DIR_TMP.iterdir():
        file.unlink()


def convert_image_to_pdf(img_path: str | Path) -> Path:
    """
    If `img_path` is an image (i.e. its suffix is in {".png", ".jpg",
    ".jpeg", ".bmp", ".tiff"}) the function converts the image in a temp
    pdf and returns the path of the temporary file (that will be in
    `DIR_TEMP` folder)
    """
    # ensure Path obj as input
    if isinstance(img_path, str):
        img_path = Path(img_path)
    # convert img to pdf and save as temporary file
    img = Image.open(img_path).convert("RGB")
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf", dir=DIR_TMP
    ) as tmp_file:
        pdf_path = Path(tmp_file.name)
        img.save(pdf_path, "PDF")
    return pdf_path


def count_pdf_pages(pdf: Path) -> int:
    """
    Returns the number of pages of the input pdf
    """
    pdf_reader: PdfReader = PdfReader(pdf)
    return len(pdf_reader.pages)


def add_one_to_counter(command_name: str) -> None:
    """
    Call this function at the end of a command_file.py to
    add +1 usage to the counter. This counter will save
    how many times we use that command
    """
    # load user's usage counts
    with FILE_COUNTER_JSON.open("r", encoding="utf-8") as jsonfile:
        usage_counter: dict[str, int] = json.load(jsonfile)

    # add +1 to the frequency dictionary
    usage_counter[command_name] = usage_counter.get(command_name, 0) + 1

    # save progress
    with FILE_COUNTER_JSON.open("w") as jsonfile:
        json.dump(usage_counter, jsonfile, indent=2)


def human_readable_size(size_bytes: int) -> str:
    """
    Examples
    --------
    >>> human_readable_size(2048)
        '2.00 KB'

    >>> human_readable_size(2_000_000)
        '1.91 MB'
    """
    for unit in ["B ", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def expand_input_paths(paths: list[Path]) -> list[Path]:
    """
    Examples
    --------
    >>> expand_input_paths([Path("*.pdf")])
        [Path("a.pdf"), Path("b.pdf")]
    """
    if os.name == "posix":
        return paths
    elif os.name == "nt":
        expanded: list[Path] = []
        for p in paths:
            if glob.has_magic(str(p)):
                expanded.extend(Path(f) for f in glob.glob(str(p)))
            else:
                expanded.append(p)

        return expanded


def human_readable_dimensions(width: int, height: int) -> str:
    # use unicode x to use proper rich print colors
    h_dimensions: str = f"{width}{SEP_DIM}{height}"
    return h_dimensions


def ratio(num: int, denom: int) -> tuple[int, int]:
    mcd: int = gcd(num, denom)
    if mcd == 0:
        return (0, 0)
    return (num // mcd, denom // mcd)


def human_readable_ratio(num: int, denom: int) -> str:
    a, b = ratio(num, denom)
    if (a, b) == (0, 0):
        return f"-{SEP_RATIO}-"
    return f"{a}{SEP_RATIO}{b}"


def human_readable_size_percentage(size: int, compressed_size: int) -> str:
    return f"{round(100 * compressed_size / size, 1)} %"


def human_readable_fps(fps: float, show_unit: bool = True) -> str:
    if show_unit:
        return f"{fps} fps"
    else:
        return f"{fps}"


def ffprobe_video_file(file: Path) -> tuple[int, int, int, float, float, int]:
    """
    Raises
    ------
    - `ValueError`: if input `file` is an image
    - `ffmpeg.Error`: if input `file` cannot be probed
    - `StopIteration`: if input `file` has no video streams

    Returns
    -------
    tuple[int, int, int, float, float, int]
        (size (bytes), width (px), height (px), fps, duration (s),
        bitrate (bits/s))
    """
    # if it is an image then skip because probe gives problems
    try:
        Image.open(file)
        raise ValueError("Cannot probe an Image")

    except UnidentifiedImageError:
        # then it is not an image and probe cannot get confused
        pass

    # probe file: raises ffmpeg.Error if it fails
    probe = ffmpeg.probe(file)

    size: int = os.path.getsize(file)

    # read metadata (raises StopIteration) if it fails
    video_stream = next(
        stream for stream in probe["streams"] if stream["codec_type"] == "video"
    )

    width: int = int(video_stream["width"])
    height: int = int(video_stream["height"])
    # calculate fps
    fps_str: str = video_stream["r_frame_rate"]  # e.g., "30000/1001"
    num, denom = fps_str.split("/")
    fps: float = round(float(num) / float(denom), 2)
    duration: float = (
        float(video_stream["duration"])
        if "duration" in video_stream
        else float(probe["format"]["duration"])
    )
    bitrate: int = int(probe["format"]["bit_rate"])  # bits/sec

    return (size, width, height, fps, duration, bitrate)


# old functions
def must_end_with_pdf(fname: str) -> str:
    """
    This function makes sure that input str `fname`
    ends or will be ending with ".pdf"
    """
    if not fname.endswith(".pdf"):
        return fname + ".pdf"
    return fname


def choose_out_pdf_name() -> str | NoReturn:
    """
    This function lets you choose a pdf output name.
    - If the name already exists then it asks you whether to overwrite it.
      If your choice is No then it restarts so you can choose another name
    - If you want to exit just throw an KeyboardInterrupt exception just
      press Ctrl+c on terminal

    ## Output
    `str` with a pdf name (that will end with '.pdf')

    """
    while True:
        try:
            input_pdf: str = input(
                "\nEnter output filename (it may or may not end with '.pdf')\n"
                "(press Ctrl+C (^C signal interrupt) to exit): "
            )
        except KeyboardInterrupt:
            print()
            sys.exit()

        pdf_name: str = must_end_with_pdf(input_pdf)

        # if the file already exists ask what to do
        if os.path.isfile(pdf_name):
            print(f"\nWarning: file '{pdf_name}' already exists,")
            overwrite_choice: str = input("do you want to overwrite it?\n[y,N]: ")
            # choice with No as default (because "" in "nN" is True)
            if overwrite_choice in "nN":
                pass
            elif overwrite_choice in "sSyY":
                return pdf_name

        else:
            return pdf_name
