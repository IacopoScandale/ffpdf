import os

DATA_FOLDER: str = "data"

PIP_VENV_WIN: str = "venv\\Scripts\\pip3.exe"
# PIP_VENV_LINUX: str = "venv/bin/"

PYTHON_VENV_WIN: str = "venv\\Scripts\\python.exe"
# PYTHON_VENV_LINUX: str = "venv/bin/python3"

COMMANDS_BAT: str = os.path.join(DATA_FOLDER, "commands.bat")
COMMANDS_SH: str = os.path.join(DATA_FOLDER, "commands.sh")

COUNTER_JSON_NAME: str = "usage_counter.json"
COUNTER_JSON: str = os.path.join(DATA_FOLDER, COUNTER_JSON_NAME)

# command aliases names
PDF_COMMANDS: str = "pdf_commands"
FNAME_FORMAT_COMM: str = "fname_format"
MERGE_PDF_COMM: str = "merge_pdf"
SLICE_PDF_COMM: str = "slice_pdf"

COMMAND_LIST: list[str] = [
  PDF_COMMANDS, 
  FNAME_FORMAT_COMM, 
  MERGE_PDF_COMM, 
  SLICE_PDF_COMM,
]