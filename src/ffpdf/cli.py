from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path

from .__main__ import show_infos
from .comm_compress_img import comm_compress_img
from .comm_compress_vid import comm_compress_vid
from .comm_convert import comm_convert
from .comm_count import comm_count
from .comm_dimensions import comm_dimensions
from .comm_extensions import comm_extensions
from .comm_format import comm_format
from .comm_img import comm_img
from .comm_merge import comm_merge
from .comm_slice import comm_slice
from .comm_vid import comm_vid
from .data.strings import (
    COMMAND,
    DESCRIPTION,
    SUB_COMPRESS,
    SUB_COMPRESS_IMG,
    SUB_COMPRESS_VID,
    SUB_CONVERT,
    SUB_COUNT,
    SUB_DIM,
    SUB_EXT,
    SUB_FORMAT,
    SUB_IMG,
    SUB_MERGE,
    SUB_SLICE,
    SUB_VID,
)


def quality_type(value: str) -> int | str:
    if value == "keep":
        return value
    try:
        int_value = int(value)
    except ValueError:
        raise ArgumentTypeError("Value must be an integer between 0 and 100.")
    if not (0 <= int_value <= 100):
        raise ArgumentTypeError(f"Value '{value}' must be between 0 and 100.")
    return int_value


def new_dim_type(value: str) -> tuple[int, int]:
    """
    Examples
    --------
    >>> new_size_type("1280x720")
        (1280, 720)
    >>> new_size_type("1280x-1")  # -1 (auto value)
        (1280, -1)
    """
    separators: tuple[str, str] = ("x", ":")
    for separator in separators:
        if separator in value:
            w, h = map(int, value.split(separator))

            if w == 0 or h == 0:
                raise ArgumentTypeError("Value must not contain zeros")

            if w == -1 and h == -1:
                raise ArgumentTypeError(
                    "Value must not contain two '-1', only one is accepted"
                )
            return (w, h)
    raise ArgumentTypeError(f"Value must contain one of these separators: {separators}")


def ratio_type(value: str | None) -> str | None:
    if not value:
        return None

    separator: str = ":"
    if separator not in value:
        raise ArgumentTypeError(f"Value must contain '{separator}' as separator")

    w, h = map(int, value.split(separator))

    if w <= 0 or h <= 0:
        raise ArgumentTypeError("Value must not contain zeros or negative numbers")

    return f"{w}{separator}{h}"


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
    parser_format: ArgumentParser = subparsers.add_parser(
        SUB_FORMAT,
        description=(
            "Add, remove or replace prefixes and suffixes from filenames, or move "
            + "them to the beginning or end of the filename"
        ),
    )
    parser_format.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input file(s)",
    )
    parser_format.add_argument(
        "-p",
        "--prefix",
        type=str,
        help=(
            "· String to put at the beginning of the file name e.g., 'ffpdf' "
            "(if present at the end it will removed)\n"
            "· String containing '->' in the format: 'old_prefix->new_prefix' "
            + "to replace the old prefix with the new one"
        ),
    )
    parser_format.add_argument(
        "-s",
        "--suffix",
        type=str,
        help=(
            "· String to put at the end of the file name e.g., 'ffpdf' "
            "(if present at the beginning it will removed)\n"
            "· String containing '->' in the format: 'old_suffix->new_suffix' "
            + "to replace the old suffix with the new one"
        ),
    )

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
        description=("Convert input files in the specified format (image or pdf)"),
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
        metavar="EXT",
    )

    # subcommand `img`
    parser_img: ArgumentParser = subparsers.add_parser(
        SUB_IMG, description="Show relevant image infos for the input files"
    )
    parser_img.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input file(s)",
    )

    # subcommand `vid`
    parser_vid: ArgumentParser = subparsers.add_parser(
        SUB_VID, description="Show relevant video infos for the input files"
    )
    parser_vid.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input file(s)",
    )

    # subcommand `compress`
    parser_compress: ArgumentParser = subparsers.add_parser(
        SUB_COMPRESS, description="Compress input images or videos"
    )

    subparsers_compress = parser_compress.add_subparsers(dest="subparser_compress")

    # subsubcommand `compress img`
    subparser_compress_img: ArgumentParser = subparsers_compress.add_parser(
        SUB_COMPRESS_IMG, description="Compress images"
    )
    subparser_compress_img.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input file(s)",
    )
    subparser_compress_img.add_argument(
        "-s",
        "--size",
        "--dimensions",
        type=new_dim_type,
        default=None,
        help="New image dimensions e.g., '1280x720' or '1280x-1'",
        metavar="WxH",
    )
    subparser_compress_img.add_argument(
        "-q",
        "--quality",
        type=quality_type,
        default="keep",
        help=(
            "New image quality as PIL quality: 0 (worse) to 95 (best). "
            + "Default keeps original image quality."
        ),
    )
    subparser_compress_img.add_argument(
        "-r",
        "--resize-ratio",
        type=ratio_type,
        default=None,
        help=(
            "Filter input images to resize by ratio i.e. resize images only "
            + "if they match this specific ratio"
        ),
    )

    # subsubcommand `compress vid`
    subparser_compress_vid: ArgumentParser = subparsers_compress.add_parser(
        SUB_COMPRESS_VID,
        description=(
            "Apply the --ffmpeg inner command to all video files, skipping "
            + f"any others. (Ignore files starting with '{COMMAND}_') "
            + "to avoid loops"
        ),
    )
    subparser_compress_vid.add_argument(
        "in_files",
        nargs="+",
        type=Path,
        help="Input file(s)",
    )
    subparser_compress_vid.add_argument(
        "-f",
        "--ffmpeg",
        required=True,
        type=str,
        help="inner ffmpeg arguments to use for each input file",
    )
    subparser_compress_vid.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="remove input files during processing",
    )

    # subcommand `dimensions`
    subparser_dimensions: ArgumentParser = subparsers.add_parser(
        SUB_DIM, description="Show perfect dimensions according to input image ratio"
    )
    subparser_dimensions.add_argument(
        "ratio", type=ratio_type, help="input ratio e.g., '4:3', '16:9', ..."
    )
    subparser_dimensions.add_argument(
        "-w", "--width", type=int, help="input width e.g., '1257', '1920', ..."
    )
    subparser_dimensions.add_argument(
        "--height", type=int, help="input height e.g., '1257', '1920', ..."
    )
    subparser_dimensions.add_argument(
        "-n",
        type=int,
        default=5,
        help=(
            "number of dimensions shown that are smaller or bigger than the "
            + "input dim (default=5)"
        ),
    )

    # subcommand `ext`
    subparser_extensions: ArgumentParser = subparsers.add_parser(
        SUB_EXT, description="List the frequency of file extensions"
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
    elif args.subcommand == SUB_IMG:
        comm_img(args.in_files)
    elif args.subcommand == SUB_VID:
        comm_vid(args.in_files)
    elif args.subcommand == SUB_COMPRESS:
        if args.subparser_compress == SUB_COMPRESS_IMG:
            comm_compress_img(args.in_files, args.quality, args.size, args.resize_ratio)
        elif args.subparser_compress == SUB_COMPRESS_VID:
            comm_compress_vid(args.in_files, args.ffmpeg, args.delete)
    elif args.subcommand == SUB_FORMAT:
        comm_format(args.in_files, args.prefix, args.suffix)
    elif args.subcommand == SUB_DIM:
        comm_dimensions(args.ratio, args.width, args.height, args.n)
    elif args.subcommand == SUB_EXT:
        comm_extensions()
    else:
        show_infos()
