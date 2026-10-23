import os
from pathlib import Path

from PyPDF2.errors import EmptyFileError, FileNotDecryptedError

from ffpdf.data.strings import SUB_COUNT
from ffpdf.data.utils import (
    add_one_to_counter,
    count_pdf_pages,
    expand_input_paths,
    human_readable_size,
    text_error,
    text_muted,
)


def comm_count(pdfs: list[Path]) -> None:
    pdfs = expand_input_paths(pdfs)

    # print header
    if pdfs:
        print(f"\n{'Pages':>5}{' ' * 4}{'Size':>10}{' ' * 4}{'Filename':<40}")
        print("—" * 70)  # em dash line separator

    # print content
    total_size: int = 0
    total_pages: int = 0
    total_files: int = 0
    for pdf in pdfs:
        # skip directories
        if pdf.is_dir():
            continue

        # skip non-PDFs
        if pdf.suffix.lower() != ".pdf":
            print(f"{' ':>5}{' ' * 4}{' ':>10}{' ' * 4}{text_muted(pdf.name):<40}")
            continue

        h_size = ""
        try:
            page_number: int = count_pdf_pages(pdf)
            total_pages += page_number

            total_files += 1

            size: int = os.path.getsize(pdf)
            total_size += size
            h_size: str = human_readable_size(size)
            print(
                f"{page_number:>5}{' ' * 4}{h_size:>10}{' ' * 4}{f"'{pdf.name}'":<40}"
            )
        except EmptyFileError:
            print(
                f"{text_error(f'{"0":>5}')}{' ' * 4}{h_size:>10}{' ' * 4}'{pdf.name}' {text_muted('(empty file)')}"
            )
        except FileNotDecryptedError:
            print(
                f"{text_error(f'{"?":>5}')}{' ' * 4}{h_size:>10}{' ' * 4} '{pdf.name}' {text_muted('(encrypted file)')}"
            )
        except Exception as e:
            print(
                f"{text_error(f'{"x":>5}')}{' ' * 4}{h_size:>10}{' ' * 4} {text_error('Error')} with '{pdf.name}' {e!r}"
            )

    # print footer
    if pdfs and total_files > 1:
        print("—" * 70)  # em dash line separator
        print(
            f"{total_pages:>5}{' ' * 4}{human_readable_size(total_size):>10}{' ' * 4}{f"'{total_files} PDFs'":<30}"
        )

    # +1 to usage counter
    add_one_to_counter(SUB_COUNT)
