import os
import sys
from pathlib import Path
from typing import Any, NoReturn

from PIL import Image, UnidentifiedImageError
from rich import print

from ffpdf.data.strings import COMMAND, SUB_COMPRESS
from ffpdf.data.utils import (
    add_one_to_counter,
    expand_input_paths,
    human_readable_dimensions,
    human_readable_ratio,
    human_readable_size,
    human_readable_size_percentage,
    ratio,
)


def print_content_line(
    size: str = "",
    new_size: str = "",
    dim_ratio: str = "",
    dim: str = "",
    new_dim: str = "",
    size_ratio: str = "",
    filename: str = "",
    black: bool = False,
) -> None:
    """
    print this command output line
    """
    sep: str = " " * 2
    arrow_size: str = "—>" if size and new_size else ""
    arrow_dim: str = "—>" if dim and new_dim else ""

    line: str = (
        f"{size:>10}{arrow_size:^4}{new_size:<10}{sep}"
        + f"{size_ratio:>10}{sep}"
        + f"{dim_ratio:>10}{sep}"
        + f"{dim:>10}{arrow_dim:^4}{new_dim:<10}{sep}"
        + f"{filename:<30}"
    )

    if black:
        line: str = "[bright_black]" + line + "[/bright_black]"

    print(line)


def comm_compress_img(
    files: list[Path],
    quality: int | str = "keep",
    new_dimensions: tuple[int, int] | None = None,
    resize_ratio: str | None = None,
) -> None | NoReturn:
    """
    Parameters
    ----------
    quality : int | None | str = "keep"
        The image quality, on a scale from `0` (worst) to `95` (best),
        or the string `"keep"`. Values above 95 should be avoided; `100`
        disables portions of the JPEG compression algorithm, and results
        in large files with hardly any gain in image quality. The value
        `"keep"` is only valid for JPEG files and will retain the
        original image quality level, subsampling, and qtables [...]
        (https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

    new_dimensions : str | None = None
        New dimensions of the output images e.g., "1280x720"

    resize_ratio : str | None = None
        Filter resize by image ratio e.g. `'4:3'` means that if
        `new_dimensions` is present, it will be applied only on 4:3
        images.
    """
    files: list[Path] = expand_input_paths(files)

    # print header
    if files:
        print()
        print_content_line(
            size="Size",
            new_size="New Size",
            dim_ratio="Ratio",
            dim="Dim",
            new_dim="New Dim",
            size_ratio="Size %",
            filename="Filename",
        )
        print("—" * 80)  # em dash line separator

    # print content
    total_size: int = 0
    total_compressed_size: int = 0
    total_files: int = len(files)

    if new_dimensions:
        adapt_ratio: bool = -1 in new_dimensions
        new_ratio: tuple[int, int] = ratio(*new_dimensions)

    for file in files:
        # skip directories
        if file.is_dir():
            total_files -= 1
            continue

        # skip files starting with `ffpdf_`
        if file.name.startswith(f"{COMMAND}_"):
            print_content_line(
                filename=f"'{file.name}'",
                black=True,
            )
            total_files -= 1
            continue

        try:
            with Image.open(file) as img:
                width, height = img.size
                h_ratio: str = human_readable_ratio(width, height)
                h_dim: str = human_readable_dimensions(width, height)
                h_new_dim: str = human_readable_dimensions(width, height)

                # filter out images with different ratio
                if resize_ratio and resize_ratio != h_ratio:
                    total_files -= 1
                    print_content_line(
                        dim_ratio=h_ratio,
                        filename=f"'{file.name}'",
                        black=True,
                    )
                    continue

                img_ratio: tuple[int, int] = ratio(width, height)

                new_file: Path = file.with_name(f"{COMMAND}_{file.name}")

                # resize img without stretch, and only if resize ratio
                # filter is correct
                if new_dimensions and new_dimensions < (width, height):
                    h_new_dim: str = human_readable_dimensions(*new_dimensions)
                    if resize_ratio and resize_ratio == h_ratio:
                        if adapt_ratio:
                            # respectively -1 value index and other value index
                            i, j = (0, 1) if new_dimensions[0] == -1 else (1, 0)

                            adapted_dim: list[int] = [0, 0]
                            adapted_dim[i] = int(
                                round(new_dimensions[j] * img_ratio[i] / img_ratio[j])
                            )
                            adapted_dim[j] = new_dimensions[j]

                            if tuple(adapted_dim) < (width, height):
                                img = img.resize(adapted_dim)

                                h_new_dim: str = human_readable_dimensions(*adapted_dim)

                        elif img_ratio == new_ratio and new_dimensions < (
                            width,
                            height,
                        ):
                            img = img.resize(new_dimensions)

                            h_new_dim: str = human_readable_dimensions(*new_dimensions)

                params: dict[str, Any] = dict()

                # copy metadata by default
                exif = img.info.get("exif")
                if exif:
                    params["exif"] = exif

                # quality can be "keep" only for JPEG format
                if not (quality == "keep" and img.format != "JPEG"):
                    params["quality"] = quality

                img.save(new_file, optimize=True, **params)

        except UnidentifiedImageError:
            total_files -= 1
            print_content_line(
                filename=f"'{file.name}'",
                black=True,
            )
            continue

        except KeyboardInterrupt:
            sys.exit()

        size: int = os.path.getsize(file)
        total_size += size

        compressed_size: int = os.path.getsize(new_file)
        total_compressed_size += compressed_size

        print_content_line(
            size=human_readable_size(size),
            new_size=human_readable_size(compressed_size),
            dim_ratio=h_ratio,
            dim=h_dim,
            new_dim=h_new_dim,
            size_ratio=human_readable_size_percentage(size, compressed_size),
            filename=f"'{file.name}'",
        )

    # print footer
    if files and total_files > 1:
        print("—" * 80)  # em dash line separator
        print_content_line(
            size=human_readable_size(total_size),
            new_size=human_readable_size(total_compressed_size),
            dim_ratio="",
            dim="",
            new_dim="",
            size_ratio=human_readable_size_percentage(
                total_size, total_compressed_size
            ),
            filename=f"'{total_files} files compressed'",
        )

    # +1 to usage counter
    add_one_to_counter(SUB_COMPRESS)
