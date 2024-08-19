import os

PACKAGE_NAME: str = "pdf_commands"
COMMANDS_COPY_FOLDER: str = "Commands"
DATA_FOLDER: str = "data"
INFO_FOLDER: str = f"{PACKAGE_NAME}.egg-info"
VENV_FOLDER: str = "venv"

VENV_SCRIPTS_FOLDER_WIN: str = os.path.join(VENV_FOLDER, "Scripts")
VENV_SCRIPTS_FOLDER_LINUX: str = os.path.join(VENV_FOLDER, "bin")


COUNTER_JSON_NAME: str = "usage_counter.json"
COUNTER_JSON: str = os.path.join(DATA_FOLDER, COUNTER_JSON_NAME)


# command aliases names
FNAME_FORMAT_COMM: str = "fname_format"
MERGE_PDF_COMM: str = "merge_pdf"
SLICE_PDF_COMM: str = "slice_pdf"

COMMANDS: dict[str,str] = {
  PACKAGE_NAME: "comm_pdf_commands", 
  FNAME_FORMAT_COMM: "comm_filename_format", 
  MERGE_PDF_COMM: "comm_pdf_merge", 
  SLICE_PDF_COMM: "comm_pdf_slicer",
}
"""
Maps command name to the name of the python file it executes
"""