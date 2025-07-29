from pathlib import Path

# strings
PACKAGE_NAME: str = "ffpdf"
AUTHOR: str = "Iacopo Scandale"
DESCRIPTION: str = "Fast PDF, Image and Video File Operations"

# commands and subcommands
SUBCOMMANDS: list[str] = [
    COMMAND := "ffpdf",
    SUB_MERGE := "merge",
    SUB_SLICE := "slice",
    SUB_COUNT := "count",
    SUB_CONVERT := "convert",
    SUB_IMG := "img",
    SUB_VID := "vid",
    SUB_COMPRESS := "compress",
    SUB_FORMAT := "format",
    SUB_DIM := "dim",
    SUB_EXT := "ext",
    # SUB_RAW := "raw",
]
SUB_COMPRESS_IMG: str = "img"
SUB_COMPRESS_VID: str = "vid"

# separators
SEP_RATIO: str = ":"
SEP_DIM: str = "×"

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
FILE_LAST_FFMPEG_OUT: Path = DIR_TMP / "ffmpeg_compress_log.txt"
