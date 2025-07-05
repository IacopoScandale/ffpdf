from argparse import ArgumentParser, Namespace
from pathlib import Path

from .__main__ import show_infos
from .comm_merge import comm_merge
from .comm_slice import comm_slice
from .comm_count import comm_count
from .comm_convert import comm_convert
from .data.strings import (
    DESCRIPTION,
    SUB_CONVERT,
    SUB_MERGE,
    SUB_SLICE,
    SUB_COUNT,
)


def parse_arguments() -> Namespace:
    """
    get ffpdf command arguments
    """
    # main command
    parser = ArgumentParser(description=DESCRIPTION)

    # subcommands
    subparsers = parser.add_subparsers(dest="subcommand")

    # subcommand `merge`
    parser_merge: ArgumentParser = subparsers.add_parser(
        SUB_MERGE,
        description="Concats all files in a pdf",
        usage="ffpdf merge 1.pdf 1.png 1.jpg ... n.pdf",
    )
    parser_merge.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Input pdf or img file(s)",
    )
    parser_merge.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output filename",
        metavar="FILE",
    )

    # TODO
    # subcommand `slice`
    parser_slice: ArgumentParser = subparsers.add_parser(
        SUB_SLICE,
        description="Select the pages you want to keep in a pdf",
        # usage="ffpdf slice in.pdf 3,5-9,11- out.pdf"
    )
    parser_slice.add_argument("in_pdf", type=Path, help="input pdf name")
    parser_slice.add_argument(
        "slice",
        type=str,
        help="e.g.: '1-5,7' will select pages 1 to 5 and page 7",
    )
    parser_slice.add_argument("out_pdf", type=Path, help="output pdf name")

    # TODO
    # subcommand `format`

    # subcommand `count`
    parser_count: ArgumentParser = subparsers.add_parser(
        SUB_COUNT,
        description="Counts the number of pages in the input pdf(s)",
    )
    parser_count.add_argument(
        "in_pdfs",
        nargs="+",
        type=Path,
        help="Input pdf or img file(s)",
    )

    # # TODO
    # # subcommand `raw` to activate ffmpeg-style cli
    # parser_raw: ArgumentParser = subparsers.add_parser(
    #     SUB_RAW,
    # )
    # parser_raw.add_argument(
    #     "-i", "--input", help="Input file(s)", action="append"
    # )
    # parser_raw.add_argument("output", help="Output file")
    
    
    # subcommand `convert`
    parser_convert: ArgumentParser = subparsers.add_parser(
        SUB_CONVERT,
        description=(
            "Convert input files in the specified format (image or pdf)"
        )
    )
    parser_convert.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input pdf or img file(s)",
    )
    parser_convert.add_argument(
        "-e",
        "--extension",
        type=str,
        default=None,
        help="Output extension e.g., 'jpg', '.pdf', ...",
        metavar="FILE",
    )


    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """
    ffpdf line command
    """
    args: Namespace = parse_arguments()

    # Execute appropriate function based on the command
    if args.subcommand == SUB_MERGE:
        comm_merge(args.files, args.output)
    elif args.subcommand == SUB_SLICE:
        comm_slice(args.in_pdf, args.slice, args.out_pdf)
    elif args.subcommand == SUB_COUNT:
        comm_count(args.in_pdfs)
    # elif args.subcommand == SUB_RAW:
    #     comm_raw(in_files=args.input, out_file=args.output)
    elif args.subcommand == SUB_CONVERT:
        comm_convert(args.in_files, args.extension)
    else:
        show_infos()
