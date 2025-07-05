import sys
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter
from rich import print

from .data.strings import SUB_SLICE
from .data.utils import add_one_to_counter


# TODO: fn written a while ago. It works, but it could be improved...
def slice_to_list(slice_: str) -> list[int]:
    """
    This function converts a str `slice_` into the list with all
    "page numbers"
    """

    def buck_interval_error(buck):
        print(
            f"'{buck}' in '{slice_}' is not correct. "
            "Expected 'a-b' with a,b positive numbers, a<=b"
        )
        sys.exit(1)

    def buck_error(buck):
        print(f"'{buck}' in '{slice_}' is not correct. Expected a natural number")
        sys.exit(1)

    if "," not in slice_:
        if "-" in slice_:
            two_nums = slice_.split("-")

            if len(two_nums) == 2:
                a = two_nums[0]
                b = two_nums[1]
                if a.isnumeric() and b.isnumeric() and int(a) <= int(b):
                    return list(range(int(a), int(b) + 1))
                else:
                    buck_interval_error(slice_)
            else:
                buck_interval_error(slice_)

        elif slice_.isnumeric():
            return [int(slice_)]
        else:
            raise ValueError(f"'{slice_}' is not a correct slice")

    res = []
    bucks = slice_.split(",")

    for buck in bucks:
        if "-" in buck:
            two_nums: list[str] = buck.split("-")

            if len(two_nums) == 2:
                a = two_nums[0]
                b = two_nums[1]
                if a.isnumeric() and b.isnumeric() and int(a) <= int(b):
                    res.extend(list(range(int(a), int(b) + 1)))
                else:
                    buck_interval_error(buck)
            else:
                buck_interval_error(buck)

        elif buck.isnumeric():
            res.append(int(buck))
        else:
            buck_error(buck)

    return res


def comm_slice(in_pdf: Path, slice_: str, out_pdf: Path) -> None:
    reader: PdfReader = PdfReader(in_pdf)
    writer: PdfWriter = PdfWriter()

    page_numbers: list[int] = slice_to_list(slice_)
    for page_number in page_numbers:
        if 1 <= page_number <= len(reader.pages):
            writer.add_page(reader.pages[page_number - 1])

    writer.write(out_pdf)

    # +1 to usage counter
    add_one_to_counter(SUB_SLICE)
