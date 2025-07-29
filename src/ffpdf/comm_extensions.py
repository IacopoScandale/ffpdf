from collections import Counter
from pathlib import Path

from rich import print

from .data.strings import SUB_EXT
from .data.utils import add_one_to_counter


def print_content_line(
    ext: str = "",
    count: int | str = "",
    color: str | None = None,
) -> None:
    sep: str = " " * 4
    line: str = f"{ext:>9}{sep}{count:<5}"
    if color:
        line: str = f"[{color}]" + line + f"[/{color}]"
    print(line)


def comm_extensions() -> None:
    # print header
    print()
    print_content_line("Extension", "Count")
    print("—" * 30)

    ext_freq: Counter = Counter(
        file.suffix for file in Path(".").iterdir() if file.is_file()
    )

    # print content
    total_count: int = 0
    for ext, count in sorted(ext_freq.items()):
        if ext == "":
            ext = "(no ext)"
        total_count += count
        print_content_line(ext=ext, count=count)

    # print footer
    print("—" * 30)
    print_content_line(
        ext=f"{len(ext_freq)} ext", count=f"{total_count} files", color="green"
    )

    # +1 to usage counter
    add_one_to_counter(SUB_EXT)
