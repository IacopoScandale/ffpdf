import os

DATA_FOLDER = "data"

PIP_VENV_WIN = "venv\\Scripts\\pip3.exe"
# PIP_VENV_LINUX = "venv/bin/"

PYTHON_VENV_WIN = "venv\\Scripts\\python.exe"
# PYTHON_VENV_LINUX = "venv/bin/python3"

COMMANDS_BAT = os.path.join(DATA_FOLDER, "commands.bat")
COMMANDS_SH = os.path.join(DATA_FOLDER, "commands.sh")

COUNTER_JSON_NAME = "usage_counter.json"
COUNTER_JSON = os.path.join(DATA_FOLDER, COUNTER_JSON_NAME)

# command aliases names
PDF_COMMANDS = "pdf_commands"
FNAME_FORMAT_COMM = "fname_format"
MERGE_PDF_COMM = "merge_pdf"
SLICE_PDF_COMM = "slice_pdf"

COMMAND_LIST = [PDF_COMMANDS, FNAME_FORMAT_COMM, MERGE_PDF_COMM, SLICE_PDF_COMM]