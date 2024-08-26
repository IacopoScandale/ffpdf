from .data.utils import add_one_to_counter
from .data.strings import FNAME_FORMAT_COMM
from argparse import ArgumentParser, Namespace
import os
import sys


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "This program when run in a folder by terminal, asks if it can "
      "reformat all filenames in lower case with '_' instead of "
      "spaces. Oss: In linux is possible to call two different files "
      "e.g.: 'Ciao.txt' and 'CiAo.txt'. In this case the program "
      "renames the first file and not the second one (because it will "
      "overwrite the other) and prints an error message. In windows "
      "this is not possible."
    )
  )
  args: Namespace = parser.parse_args()
  return args


def format_filename(filename: str) -> str:
  """
  Returns lowercase `filename` string with "_" instead of spaces.
  Then if the string contains this pattern "_-_", it will be replaced
  only with "_".
  """
  formatted_filename: str = filename.replace(" ", "_")
  formatted_filename = formatted_filename.lower()
  formatted_filename = formatted_filename.replace("_-_","_")
  return formatted_filename

def main() -> None:
  # treat command as command
  _ = get_arguments()  
  
  # only for linux special case
  no_action = True

  files_to_rename: list[str] = [
    f for f in os.listdir() if not os.path.isdir(f) and f != format_filename(f)
  ]

  # print what is it going to do
  for i, fname in enumerate(files_to_rename, 1):
    print(f"{i:>4}. {fname:<50}  ——→  {format_filename(fname):<50}")

  # case no filenames to format
  if len(files_to_rename) == 0:
    print("All files are well formatted: 0 files renamed")
    sys.exit()

  # choose to rename or not
  choice = input(f"\nRename this {len(files_to_rename)} files?\n [Y,n]: ")
  if choice in "sSyY":
    # rename files
    for i, fname in enumerate(files_to_rename, 1):
      # destination file already exists (cfr linux in `help_message`)
      if format_filename(fname) in os.listdir():
        print(
          f"   x. NOT renamed '{fname}': '{format_filename(fname)}' already exists"
        )
      else:  # rename the file and print result
        no_action = False
        os.rename(fname, format_filename(fname))
        print(
          f"{i:>4}. renamed {fname:<50}  ——→  {format_filename(fname):<50}"
        )

    # linux case if all files counted as to rename, have the same name
    # and cannot be renamed (otherwise they will be overwrited)
    if no_action:
      print("0 files renamed")

  # +1 to usage counter
  add_one_to_counter(FNAME_FORMAT_COMM)