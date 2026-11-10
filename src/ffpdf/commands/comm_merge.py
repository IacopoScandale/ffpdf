import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError, PdfStreamError

from ffpdf.data.strings import SUB_MERGE
from ffpdf.data.utils import (
    add_one_to_counter,
    choose_out_pdf_name,
    convert_image_to_pdf,
    expand_input_paths,
    flush_tmp_dir,
    is_image,
    open_result_in_default_app,
    text_error,
    text_muted,
)


def comm_merge(
    files: list[Path],
    out_pdf: Path | None = None,
    preview: bool = False,
    outline: bool = False,
) -> None:
    """
    Args:
        files: ordered list of the files to merge
        out_pdf: name of the merged output PDF file. If None then it is
            asked in a prompt
        preview: open the output pdf with the OS default application,
            without writing it into disk (write in the OS temporary dir)
        outline: if true, populate the PDF document outline with the
            names of the files used in the merge process
    """
    files = expand_input_paths(files)
    total: int = len(files)
    width: int = len(str(total))
    # print(files)

    # writer object to write pages
    writer = PdfWriter()
    readers = []

    current_page = 0
    outline_nodes = {}  # keep track of created dir nodes

    for i, file in enumerate(files, start=1):
        print(text_muted(f"[{i:>{width}}/{total}] adding {file}"))
        orig_file = file

        # convert images found in pdf tmp files
        if is_image(file):
            file = convert_image_to_pdf(file)

        # read every pdf page and add it to the writer
        try:
            reader = PdfReader(file)
        except (PdfReadError, PdfStreamError):
            print(f"{text_error('Error:')} cannot read file '{file.name}'")
            continue

        # save in memory to avoid overwriting it due to lazy loading
        readers.append(reader)

        # current file start page number in the output PDF numbering
        start_page = current_page
        for page in reader.pages:
            writer.add_page(page)
            current_page += 1

        # create table of contents from the input files
        if outline and len(reader.pages) > 0:
            parts = orig_file.parts
            parent = None

            # add hierarchical parent folders if any
            for depth in range(1, len(parts)):
                sub_path = parts[:depth]
                if sub_path not in outline_nodes:
                    folder_name = parts[depth - 1]
                    outline_nodes[sub_path] = writer.add_outline_item(
                        title=folder_name,
                        page_number=start_page,
                        parent=parent,
                    )
                parent = outline_nodes[sub_path]

            # add current file to the document outline
            file_name = parts[-1]
            writer.add_outline_item(
                title=file_name,
                page_number=start_page,
                parent=parent,
            )

    if preview:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            preview_path = Path(tmp_file.name)
            writer.write(tmp_file)

        open_result_in_default_app(preview_path)
    else:
        if not out_pdf:
            out_pdf = Path(choose_out_pdf_name())

        # save merged pdf
        writer.write(out_pdf)

    # remove all tmp pdf files previously created
    flush_tmp_dir()

    # +1 to usage counter
    add_one_to_counter(SUB_MERGE)
