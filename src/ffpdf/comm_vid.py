import sys
import time
from pathlib import Path

import ffmpeg
from rich import print

from .data.strings import SUB_VID
from .data.utils import (
    add_one_to_counter,
    expand_input_paths,
    ffprobe_video_file,
    human_readable_dimensions,
    human_readable_ratio,
    human_readable_size,
)


def human_readable_bitrate(bitrate: int) -> str:
    """
    Examples
    --------
    >>> human_readable_bitrate(12345)
        '12 Kb/s'
    >>> human_readable_bitrate(4194304)
        '4 Mb/s'
    """
    for unit in ["b/s ", "Kb/s"]:
        if bitrate < 1024:
            return f"{bitrate:.0f} {unit}"
        bitrate /= 1024
    return f"{bitrate:.0f} Mb/s"


def human_readable_duration(seconds: float) -> str:
    """
    Examples
    --------
    >>> human_readable_duration(24)
        '00:24'
    >>> human_readable_duration(120)
        '02:00'
    >>> human_readable_duration(123456)
        '10:17:36'
    """
    seconds = int(round(seconds))
    if seconds < 3600:
        return time.strftime("%M:%S", time.gmtime(seconds))
    else:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))


def print_content_line(
    size: str = "",
    ratio: str = "",
    dim: str = "",
    duration: str = "",
    fps: str = "",
    bitrate: str = "",
    filename: str = "",
) -> None:
    sep: str = " " * 2
    print(
        f"{size:>10}{sep}{ratio:>8}{sep}{dim:>13}{sep}{duration:>8}{sep}"
        + f"{fps:>10}{sep}{bitrate:>10}{sep}{filename:<30}"
    )


def comm_vid(files: list[Path]) -> None:
    files: list[Path] = expand_input_paths(files)

    # print header
    if files:
        print()
        print_content_line(
            "Size",
            "Ratio",
            "Dimensions",
            "Duration",
            "Framerate",
            "Bitrate",
            "Filename",
        )
        print("—" * 80)  # em dash line separator

    # print content
    total_size: int = 0
    total_files: int = 0
    total_duration: float = 0.0

    for file in files:
        if file.is_dir():
            continue

        try:
            size, width, height, fps, duration, bitrate = ffprobe_video_file(file)
        except (ValueError, ffmpeg.Error, StopIteration):
            print_content_line(filename=f"[bright_black]'{file.name}'[/bright_black]")
            continue
        except KeyboardInterrupt:
            sys.exit()

        # print video content line
        total_files += 1
        total_size += size
        total_duration += duration

        h_size: str = human_readable_size(size)
        h_ratio: str = human_readable_ratio(width, height)
        h_dim: str = human_readable_dimensions(width, height)
        h_duration: str = human_readable_duration(duration)
        h_fps: str = f"{fps} fps"
        h_bitrate: str = human_readable_bitrate(bitrate)

        print_content_line(
            h_size, h_ratio, h_dim, h_duration, h_fps, h_bitrate, f"'{file.name}'"
        )

    # print footer
    if files and total_files > 1:
        print("—" * 80)  # em dash line separator
        print_content_line(
            size=human_readable_size(total_size),
            duration=human_readable_duration(total_duration),
            filename=f"'{total_files} videos'",
        )

    # +1 to usage counter
    add_one_to_counter(SUB_VID)
