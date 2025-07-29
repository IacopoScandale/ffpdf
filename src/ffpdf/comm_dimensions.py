"""
Use to print dimensions of perfect ratios
"""

from rich import print

from .data.strings import SEP_RATIO, SUB_DIM
from .data.utils import add_one_to_counter


def comm_dimensions(
    in_ratio: str, in_width: int | None = None, in_height: int | None = None, n: int = 5
) -> None:
    """
    Print the closes perfect dimensions according to input ratio
    `in_ratio` and one of the input width `in_width` or height
    `in_weight`

    Parameters
    ----------
    in_ratio : str
        Input ratio string e.g., "4:3", "16:9", ...
    in_width : int
        The width value in pixels around to find the perfect ratios
    in_height : int
        The height value in pixels around to find the perfect ratios
    n : int
        the number of dimensions to print around an input `in_width` or
        `height`
    """

    w, h = map(int, in_ratio.split(":"))

    if in_width:
        # integer s.t. w * closest_k = in_width
        closest_k: int = in_width // w

    elif in_height:
        # integer s.t. h * closest_k = in_height
        closest_k: int = in_height // h

    else:
        # default values
        closest_k: int = 400
        n: int = 49

    # print dimensions
    lo, hi = max(1, closest_k - n), max(1, closest_k + n)

    col_number: int = 7
    line: str = ""
    for i, k in enumerate(range(lo, hi), 1):
        cur_ratio: str = f"{w * k}{SEP_RATIO}{h * k}"

        line = line + f"  {cur_ratio:<11}"

        if i % col_number == 0:
            print(line)
            line: str = ""

    if line:
        print(line)

    # +1 to usage counter
    add_one_to_counter(SUB_DIM)
