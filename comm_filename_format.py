from data.utils import help_and_error
from data.strings import FNAME_FORMAT_COMM
import os, sys

help_message = f"""
This program when run in a folder by terminal, asks if it can rename all files as it follows:
1. all letters --> lowercase letter
2. all spaces  --> underscores

USAGE: {FNAME_FORMAT_COMM}
 
oss)
In linux is possible to call two files for example "Ciao.txt" and "CiAo.txt".
In this case the program renames the first file and not the second (because it
will overwrite the other) and prints an error message.
In windows this is not possible.

oss)
This program prints always a message and explains what it is doing.
"""

help_and_error(help_message, sys.argv, 0, command_name=FNAME_FORMAT_COMM)


def format(fname: str) -> str:
  """
  retunrs formatted `fname` to lower case with "_" on spaces
  """
  s = ""
  for char in str(fname):
    if char == " ":
      s = s + "_"

    elif char.isalpha():
      s = s + char.lower()

    else:
      s = s + char
  return s



no_action = True

# print what is it going to do
files_to_rename = 0
for i, fname in enumerate(os.listdir()):
  if os.path.isfile(fname) and fname != format(fname):
    files_to_rename += 1
    print(f"  {files_to_rename}. '{fname}'  ——→  '{format(fname)}'")

# case no filenames to format
if files_to_rename == 0:
  print("All files are well formatted: 0 files renamed")
  sys.exit()

# choose to rename or not
choice = input(f"\nRename this {files_to_rename} files?\n [Y,n]: ")
if choice in "sSyY":
  # rename files
  for i, fname in enumerate(os.listdir()):
    if os.path.isfile(fname) and fname != format(fname):
      # destination file already exists (cfr linux in `help_message`)
      if format(fname) in os.listdir():
        print(f"x. not renamed '{fname}': '{format(fname)}' already exists")
      else: # rename the file and print result
        no_action = False
        os.rename(fname, format(fname))
        print(f"{i+1}. renamed '{fname}'  ——→  '{format(fname)}'")

  # linux case if all files counted as to rename, have the same name
  # and cannot be renamed (otherwise they will be overwrited)
  if no_action:
    print("0 files renamed")