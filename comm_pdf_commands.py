from data.utils import help_and_error
from data import strings
import sys


help_message = f"""
Shows all PDF Commands

Usage: {strings.PDF_COMMANDS}
"""


help_and_error(help_message, sys.argv, 0, command_name=strings.PDF_COMMANDS)

print("\nPDF Commands:")
print(f"  · {strings.PDF_COMMANDS}")
print(f"  · {strings.MERGE_PDF_COMM}")
print(f"  · {strings.SLICE_PDF_COMM}")
print(f"  · {strings.FNAME_FORMAT_COMM}")

print("\nType 'command_name -h' for more info")