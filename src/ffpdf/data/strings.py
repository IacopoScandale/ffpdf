from pathlib import Path


# strings
PACKAGE_NAME: str = "ffpdf"
AUTHOR: str = "Iacopo Scandale"
DESCRIPTION: str = "Fast PDF and Image Files Operations"

# commands
COMMAND: str = "ffpdf"

# subcommands
SUBCOMMANDS: list[str] = [
    SUB_MERGE := "merge",
    SUB_SLICE := "slice",
    SUB_COUNT := "count",
    SUB_CONVERT := "convert",
    SUB_IMG := "img",
    # SUB_FORMAT := "format",
    # SUB_RAW := "raw",
]

# folders
DIR_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
DIR_SCRIPTS: Path = DIR_ROOT / "src" / "ffpdf"
DIR_DATA: Path = DIR_SCRIPTS / "data"
DIR_TMP: Path = DIR_DATA / "tmp"
DIR_TMP.mkdir(exist_ok=True)

# files
FILE_COUNTER_JSON: Path = DIR_DATA / "usage_counter.json"
if not FILE_COUNTER_JSON.exists():
    FILE_COUNTER_JSON.write_text("{}")
