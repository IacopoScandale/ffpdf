from data.utils import help_and_error, add_one_to_counter
from data import strings
import os, sys, json


help_message = f"""
Shows all PDF Commands

Usage: {strings.PDF_COMMANDS}
"""


help_and_error(help_message, sys.argv, 0, command_name=strings.PDF_COMMANDS)


# get the full path of this file
this_file_full_path = os.path.abspath(__file__)
# get full path of data folder
main_folder_full_path = os.path.dirname(this_file_full_path)
# counter file full_path
full_path_counter_json = os.path.join(main_folder_full_path, strings.COUNTER_JSON)

# +1 to usage counter
add_one_to_counter(strings.PDF_COMMANDS)

# open counter json as dictionary
with open(full_path_counter_json, "r") as jsonfile:
  usage_counter = json.load(jsonfile)


print("\nPDF Commands:\t\tTimes Used:")
print(f"  · {strings.PDF_COMMANDS}\t{usage_counter[strings.PDF_COMMANDS]}")
print(f"  · {strings.MERGE_PDF_COMM}\t\t{usage_counter[strings.MERGE_PDF_COMM]}")
print(f"  · {strings.SLICE_PDF_COMM}\t\t{usage_counter[strings.SLICE_PDF_COMM]}")
print(f"  · {strings.FNAME_FORMAT_COMM}\t{usage_counter[strings.FNAME_FORMAT_COMM]}")

print("\nType 'command_name -h' for more info")


