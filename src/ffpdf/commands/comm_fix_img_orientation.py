from pathlib import Path

from PIL import Image, ImageOps
from rich import print

from ffpdf.data.strings import SUB_FIX_IMG_ROT
from ffpdf.data.utils import add_one_to_counter, expand_input_paths


def comm_fix_img_orientation(in_files: list[Path]) -> None:
    in_files = expand_input_paths(in_files)

    for file in in_files:
        new_filename: Path = file.with_stem(file.stem + "__fixed")
        try:
            img = Image.open(file)
            fixed_img = ImageOps.exif_transpose(img)

            fixed_img.save(new_filename)
            print(f"Fixed Orientation at '{new_filename}'")
        except Exception as e:
            print(f"Skipped '{new_filename}':")
            print(repr(e))

    # +1 to usage counter
    add_one_to_counter(SUB_FIX_IMG_ROT)
