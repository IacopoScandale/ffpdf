import os
import sys
from pathlib import Path
from typing import NoReturn

from PIL import Image, UnidentifiedImageError
from rich import print

from .data.strings import SUB_IMG
from .data.utils import (
    add_one_to_counter,
    expand_input_paths,
    human_readable_dimensions,
    human_readable_ratio,
    human_readable_size,
)


def comm_img(files: list[Path]) -> None | NoReturn:
    files: list[Path] = expand_input_paths(files)

    # print header
    if files:
        print(
            f"\n{'Size':>10}{' ' * 2}{'Dimensions':>13}{' ' * 2}{'Ratio':>10}{' ' * 4}{'Filename':<30}"
        )
        print("—" * 70)  # em dash line separator

    # print content
    total_size: int = 0
    total_files: int = len(files)
    for file in files:
        if file.is_dir():
            total_files -= 1
            continue
        try:
            with Image.open(file) as img:
                width, height = img.size

            h_dim: str = human_readable_dimensions(width, height)
            h_ratio: str = human_readable_ratio(width, height)

            size: int = os.path.getsize(file)
            total_size += size
            h_size: str = human_readable_size(size)

            print(
                f"{h_size:>10}{' ' * 2}{h_dim:>13}{' ' * 2}{h_ratio:>10}{' ' * 4}{repr(file.name):<30}"
            )

        except UnidentifiedImageError:
            total_files -= 1
            print(
                f"{'':>10}{' ' * 2}{'':>13}{' ' * 2}{'':>10}{' ' * 4}{f"[bright_black]'{file.name}'[/bright_black]":<30}"
            )

        except KeyboardInterrupt:
            sys.exit(1)

    # print footer
    if files and total_files > 1:
        print("—" * 70)  # em dash line separator
        print(
            f"{human_readable_size(total_size):>10}{' ' * 2}{'':>13}{' ' * 2}{'':>10}{' ' * 4}{f"'{total_files} images'":<30}"
        )

    # +1 to usage counter
    add_one_to_counter(SUB_IMG)
