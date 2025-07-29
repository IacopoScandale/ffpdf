import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

import ffmpeg
from rich import print, progress

from ffpdf.data.strings import COMMAND, FILE_LAST_FFMPEG_OUT, SUB_COMPRESS, SUB_VID
from ffpdf.data.utils import (
    add_one_to_counter,
    expand_input_paths,
    ffprobe_video_file,
    human_readable_dimensions,
    human_readable_fps,
    human_readable_ratio,
    human_readable_size,
    human_readable_size_percentage,
)


# TODO new print content: two rows for each video and also new filename,
# new ratio and old and new bitrate
def print_content_line(
    size: str = "",
    new_size: str = "",
    size_ratio: str = "",
    dim_ratio: str = "",
    dim: str = "",
    new_dim: str = "",
    fps: str = "",
    new_fps: str = "",
    filename: str = "",
    error: str = "",
) -> None:
    """
    print this command output line
    """
    if error:
        print(f"    [bright_black]{error:<83}{filename:<30}[/bright_black]")
    else:
        sep: str = " " * 2
        arrow_size: str = "—>" if size and new_size else ""
        arrow_dim: str = "—>" if dim and new_dim else ""
        arrow_fps: str = "—>" if fps and new_fps else ""
        print(
            f"{size:>10}{arrow_size:^4}{new_size:<10}{sep}"
            + f"{size_ratio:>6}{sep}"
            + f"{dim_ratio:>5}{sep}"
            + f"{dim:>10}{arrow_dim:^4}{new_dim:<10}{sep}"
            + f"{fps:>5}{arrow_fps:^4}{new_fps:<9}{sep}"
            + f"{filename:<30}"
        )


def comm_compress_vid(
    files: list[Path],
    ffmpeg_command: str,
    delete_inputs: bool = False,
) -> None | NoReturn:
    """
    Apply `ffmpeg_command` to the input videos only, skipping images and
    other files, and on output each filename is mapped
    'filename' -> 'ffpdf_filename'

    Parameters
    ----------
    ffmpeg_command : str
        ffmpeg command string without `-i` inputs or outputs. There is
        no need to map metadata because `-map_metadata 0` there is by default

    delete_inputs : bool = False
        If set to True, the input files will be progressively deleted
        during processing. As a result, only the new files will remain
        at the end.
    """
    files: list[Path] = expand_input_paths(files)

    # print header
    if files:
        print(
            f"[bright_black]See ffmpeg output log at '{FILE_LAST_FFMPEG_OUT}'[/bright_black]\n"
        )
        print_content_line(
            size="Size",
            new_size="New Size",
            size_ratio="Size %",
            dim_ratio="Ratio",
            dim="Dim",
            new_dim="New Dim",
            fps="FPS",
            new_fps="New FPS",
            filename="Filename",
        )
        print("—" * 95)  # em dash line separator

    # print content
    total_size: int = 0
    total_compressed_size: int = 0
    total_files: int = 0

    # clear last ffmpeg log file:
    with FILE_LAST_FFMPEG_OUT.open("w", encoding="utf-8") as _:
        pass

    with progress.Progress(
        progress.TextColumn("[progress.description]{task.description}"),
        progress.BarColumn(bar_width=40, complete_style="green"),
        progress.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        progress.TimeElapsedColumn(),
        progress.TimeRemainingColumn(),
    ) as p:
        task = p.add_task("Processing files...", total=len(files))

        for file in files:
            p.update(
                task, description=f"Processing [green]'{file.name}'[/green]", advance=1
            )

            # skip directories
            if file.is_dir():
                continue

            # skip files starting with 'ffpdf_'
            if file.name.startswith(f"{COMMAND}_"):
                print_content_line(
                    error=f"Skipped (file starts with {COMMAND}_)",
                    filename=f"[bright_black]'{file.name}'[/bright_black]",
                )
                continue

            # get input file info to print or skip if it is not a video
            try:
                size_in, width_in, height_in, fps_in, *_ = ffprobe_video_file(file)
            except (ValueError, ffmpeg.Error, StopIteration):
                print_content_line(
                    filename=f"[bright_black]'{file.name}'[/bright_black]"
                )
                continue
            except KeyboardInterrupt:
                sys.exit()

            # do not use ffmpeg api to accept cli command arguments
            new_file: Path = file.with_name(f"{COMMAND}_{file.name}")
            ffmpeg_cmd: list[str] = (
                ["ffmpeg", "-i", file, "-y", "-hide_banner", "-map_metadata", "0"]
                + shlex.split(ffmpeg_command)
                + [new_file]
            )

            # run ffmpeg and append log to FILE_LAST_FFMPEG_OUT file
            with FILE_LAST_FFMPEG_OUT.open("a", encoding="utf-8") as ffmpeg_log:
                try:
                    subprocess.run(
                        ffmpeg_cmd,
                        check=True,  # raise subprocess.CalledProcessError
                        stdout=ffmpeg_log,
                        stderr=subprocess.STDOUT,
                    )
                except subprocess.CalledProcessError:
                    # print(f"Skipped file '{file.name}': {repr(e)}")
                    # FIXME
                    print_content_line(
                        error="Error in --ffmpeg command (see out log)",
                        filename=f"[bright_black]'{file.name}'[/bright_black]",
                    )
                    continue
                except KeyboardInterrupt:
                    sys.exit()

            # get output file info to print or skip if it is not a video
            try:
                size_out, width_out, height_out, fps_out, *_ = ffprobe_video_file(
                    new_file
                )
            except (ValueError, ffmpeg.Error, StopIteration):
                print_content_line(
                    filename=f"[bright_black]'{file.name}'[/bright_black]"
                )
                continue
            except KeyboardInterrupt:
                sys.exit()

            total_files += 1
            total_size += size_in
            total_compressed_size += size_out

            print_content_line(
                size=human_readable_size(size_in),
                new_size=human_readable_size(size_out),
                size_ratio=human_readable_size_percentage(size_in, size_out),
                dim_ratio=human_readable_ratio(width_in, height_in),
                dim=human_readable_dimensions(width_in, height_in),
                new_dim=human_readable_dimensions(width_out, height_out),
                fps=human_readable_fps(fps_in, show_unit=False),
                new_fps=human_readable_fps(fps_out),
                filename=f"'{file.name}'",
            )

            # delete input files
            if delete_inputs:
                os.remove(file)

    # print footer
    if files and total_files > 1:
        print("—" * 95)  # em dash line separator
        print_content_line(
            size=human_readable_size(total_size),
            new_size=human_readable_size(total_compressed_size),
            size_ratio=human_readable_size_percentage(
                total_size, total_compressed_size
            ),
            filename=f"'{total_files} files'",
        )
    print("\n  Notes:")
    print(
        f"  · run '{COMMAND} {SUB_VID} *.mp4' or '{COMMAND} {SUB_VID} *' to see results"
    )
    print(f"  · See ffmpeg output log at '{FILE_LAST_FFMPEG_OUT}'")

    # +1 to usage counter
    add_one_to_counter(SUB_COMPRESS)
