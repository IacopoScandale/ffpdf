import os
from pathlib import Path

from PyPDF2.errors import EmptyFileError, FileNotDecryptedError
from rich import print

from .data.strings import SUB_COUNT
from .data.utils import (
    add_one_to_counter,
    count_pdf_pages,
    expand_input_paths,
    human_readable_size,
)


def comm_count(pdfs: list[Path]) -> None:
    pdfs: list[Path] = expand_input_paths(pdfs)

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
            print(
                f"{' ':>5}{' ' * 4}{' ':>10}{' ' * 4}{f"[bright_black]'{pdf.name}'[/bright_black]":<40}"
            )
            continue

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
                f"[red]{'0':>5}[/red]{' ' * 4}{h_size:>10}{' ' * 4}'{pdf.name}' [bright_black](empty file)[/bright_black]"
            )
        except FileNotDecryptedError:
            print(
                f"[red]{'?':>5}[/red]{' ' * 4}{h_size:>10}{' ' * 4} '{pdf.name}' [bright_black](encrypted file)[/bright_black]"
            )
        except Exception as e:
            print(
                f"[red]{'x':>5}[/red]{' ' * 4}{h_size:>10}{' ' * 4} [red]Error[/red] with '{pdf.name}' {repr(e)}"
            )

    # print footer
    if pdfs and total_files > 1:
        print("—" * 70)  # em dash line separator
        print(
            f"{total_pages:>5}{' ' * 4}{human_readable_size(total_size):>10}{' ' * 4}{f"'{total_files} PDFs'":<30}"
        )

    # +1 to usage counter
    add_one_to_counter(SUB_COUNT)
