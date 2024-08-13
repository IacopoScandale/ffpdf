from data.utils import help_and_error, add_one_to_counter
from data import strings
import os
import sys
import json


help_message = f"""
Shows all PDF Commands

Usage: {strings.PDF_COMMANDS}
"""


help_and_error(help_message, sys.argv, 0, command_name=strings.PDF_COMMANDS)

# get the full path of this file
this_file_full_path: str = os.path.abspath(__file__)
# get full path of data folder
main_folder_full_path: str = os.path.dirname(this_file_full_path)
# counter file full_path
full_path_counter_json: str = os.path.join(main_folder_full_path, 
                                           strings.COUNTER_JSON)
# +1 to usage counter
add_one_to_counter(strings.PDF_COMMANDS)

# open counter json as dictionary
with open(full_path_counter_json, "r") as jsonfile:
  usage_counter: dict[str,int] = json.load(jsonfile)

# print all commands
print("\nPDF Commands:\t\tTimes Used:")
for command in strings.COMMAND_LIST:
  times_used = usage_counter.setdefault(command, 0)
  print(f"  · {command:<15} {times_used:>14}")

print("\nType 'command_name -h' for more info")