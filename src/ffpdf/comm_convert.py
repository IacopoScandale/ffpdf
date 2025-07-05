from pathlib import Path

from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
from PIL import Image, UnidentifiedImageError
from rich import print

from .data.strings import SUB_CONVERT
from .data.utils import add_one_to_counter


def new_ext_filename(file: Path, ext: str) -> Path:
    """
    Example
    -------
    >>> get_new_ext_filename("img.png", ".jpg")
        "img.png.jpg"  # or "img.png(1).jpg etc if file already exists
    """
    # first attempt
    new_filepath: Path = file.with_name(file.name + ext)
    if not new_filepath.exists():
        return new_filepath

    # next attempts
    i: int = 1
    while True:
        new_filepath = file.with_name(f"{file.name}({i}){ext}")
        if not new_filepath.exists():
            return new_filepath
        i += 1


def comm_convert(
    in_files: list[Path],
    ext: str,
) -> None:
    # make sure ext is lowercase and starts with a dot
    ext = ext.lower()
    if not ext.startswith("."):
        ext = f".{ext}"

    for file in in_files:
        new_filename: Path = new_ext_filename(file, ext)

        # case: no conversion needed
        if file.suffix.lower() == ext:
            print(f"[yellow]Skipped  [/yellow] '{file}' [black](no conversion is needed)[/black]")
            continue

        # convert pdf to image
        if file.suffix.lower() == ".pdf":
            try:
                images: list[Image.Image] = convert_from_path(file)
            except PDFPageCountError as e:
                print(f"[red]Error[/red] with '{file}': {repr(e)}")
                continue

            # just for style (e.g., 123 -> 3 chars, 89 -> 2 chars ...)
            num_chars: int = len(str(len(images)))
            try:
                for i, img in enumerate(images, 1):
                    cur_file: str = f"{file.name}_page_{i:{num_chars}d}{ext}"
                    img.save(new_filename.with_name(cur_file))
                print(f"Converted '{file}' ({i} pages) to '{ext}'")
            except ValueError as e:
                print(f"[red]Error[/red] with '{file}': {repr(e)}")

        # convert image to image or image to pdf
        else:
            try:
                img = Image.open(file)
                img.save(new_filename)
                print(f"Converted '{file}' to '{new_filename}'")
            except ValueError as e:
                print(f"[red]Error[/red] with '{file}': {repr(e)}")
            except UnidentifiedImageError as e:
                print(f"[red]Error[/red] with '{file}': {repr(e)}")

    # +1 to usage counter
    add_one_to_counter(SUB_CONVERT)
