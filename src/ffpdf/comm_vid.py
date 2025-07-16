import os
import time
from pathlib import Path

import ffmpeg
from PIL import Image, UnidentifiedImageError
from rich import print

from .data.strings import SUB_VID
from .data.utils import (
    add_one_to_counter,
    expand_input_paths,
    human_readable_dimensions,
    human_readable_size,
)


# TODO
def human_readable_bitrate(bitrate: int) -> str:
    """
    Examples
    --------
    """
    for unit in ["b/s ", "Kb/s"]:
        if bitrate < 1024:
            return f"{bitrate:.0f} {unit}"
        bitrate /= 1024
    return f"{bitrate:.0f} Mb/s"


# TODO 
def human_readable_duration(seconds: float) -> str:
    """
    Examples
    --------
    """
    seconds = int(round(seconds))
    if seconds < 3600:
        return time.strftime("%M:%S", time.gmtime(seconds))
    else:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))


def comm_vid(files: list[Path]) -> None:
    files: list[Path] = expand_input_paths(files)
    
    # print header
    if files:
        print(
            f"\n{'Size':>10}{' ' * 2}{'Dimensions':>13}{' ' * 2}{'Duration':>8}{' ' * 2}{'Framerate':>10}{' ' * 2}{'Bitrate':>10}{' ' * 2}{'Filename':<30}"
        )
        print("—" * 80)  # em dash line separator

    # print content
    total_size: int = 0
    total_files: int = len(files)
    total_duration: float = 0.0

    for file in files:
        if file.is_dir():
            total_files -= 1
            continue
        size: int = os.path.getsize(file)
        total_size += size
        h_size: str = human_readable_size(size)
        
        # if it is an image then skip because probe gives problems
        try:
            with Image.open(file) as img:
                width, height = img.size
            h_dim: str = human_readable_dimensions(width, height)
            print(
            f"{h_size:>10}{' ' * 2}{h_dim:>13}{' ' * 2}{' ':>8}{' ' * 2}{' ':>10}{' ' * 2}{' ':>10}{' ' * 2}{repr(file.name):<30}"
            )
            continue

        except UnidentifiedImageError:
            # then it is not an image and probe cannot get confused
            pass

        # probe file
        try:
            probe = ffmpeg.probe(file)
        except ffmpeg.Error:
            # TODO
            print(
            f"{h_size:>10}{' ' * 2}{' ':>13}{' ' * 2}{' ':>8}{' ' * 2}{' ':>10}{' ' * 2}{' ':>10}{' ' * 2}{repr(file.name):<30}"
            )
            continue

        # read metadata
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

        # print video content line
        total_duration += duration
        h_duration: str = human_readable_duration(duration)
        h_dim: str = human_readable_dimensions(width, height)
        h_bitrate: str = human_readable_bitrate(bitrate)
        h_fps: str = f"{fps} fps"

        print(
            f"{h_size:>10}{' ' * 2}{h_dim:>13}{' ' * 2}{h_duration:>8}{' ' * 2}{h_fps:>10}{' ' * 2}{h_bitrate:>10}{' ' * 2}{repr(file.name):<30}"
        )

    # print footer
    if files and total_files > 1:
        print("—" * 80)  # em dash line separator
        print(
            f"{human_readable_size(total_size):>10}{' ' * 17}{human_readable_duration(total_duration):>8}{' ' * 26}{f"'{total_files} files'":<30}"
        )

    # +1 to usage counter
    add_one_to_counter(SUB_VID)