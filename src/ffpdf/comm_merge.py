from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

from .data.strings import SUB_MERGE
from .data.utils import (
    add_one_to_counter,
    choose_out_pdf_name,
    convert_image_to_pdf,
    expand_input_paths,
    flush_tmp_dir,
    is_image,
)


def comm_merge(files: list[str], out_pdf: Path | None = None) -> None:
    files: list[Path] = expand_input_paths(files)

    if not out_pdf:
        out_pdf: Path = Path(choose_out_pdf_name())

    # writer object to write pages
    writer = PdfWriter()

    for file in files:
        # convert images found in pdf tmp files
        if is_image(file):
            file = convert_image_to_pdf(file)

        # read every pdf page and add it to the writer
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    # save merged pdf
    writer.write(out_pdf)

    # remove all tmp pdf files previously created
    flush_tmp_dir()

    # +1 to usage counter
    add_one_to_counter(SUB_MERGE)
