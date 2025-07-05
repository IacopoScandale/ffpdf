from pathlib import Path

from PyPDF2.errors import EmptyFileError, FileNotDecryptedError
from rich import print

from .data.strings import SUB_COUNT
from .data.utils import add_one_to_counter, count_pdf_pages


def comm_count(pdfs: list[Path]) -> None:
    print(f"\n{'[bold]Pages[/bold]':>5}{' ' * 4}{'[bold]Filename[/bold]':<40}")
    print("—" * 50)  # em dash line separator

    for pdf in pdfs:
        if pdf.suffix.lower() != ".pdf":
            print(f"{'·':>5}{' ' * 4}{f'\'{pdf.name}\'':<40}")
            continue
        try:
            page_number: int = count_pdf_pages(pdf)
            print(f"{page_number:>5}{' ' * 4}{f'\'{pdf.name}\'':<40}")
        except EmptyFileError:
            print(f"[red]{'0':>5}[/red]{' ' * 4}'{pdf.name}' [black](empty file)[/black]")
        except FileNotDecryptedError:
            print(f"[red]{'?':>5}[/red]{' ' * 4} '{pdf.name}' [black](encrypted file)[/black]")
        except Exception as e:
            print(f"[red]{'x':>5}[/red]{' ' * 4} [red]Error[/red] with '{pdf.name}' {repr(e)}")

    # +1 to usage counter
    add_one_to_counter(SUB_COUNT)
