from data.strings import COUNTER_JSON_NAME
from typing import NoReturn
import os
import sys
import json

def help_and_error(
    help_message: str,
    argv: list, 
    argument_number: int = None, 
    min_arg_number: int = 0, 
    command_name: str = "command_name"
) -> None:
  """
  Input
  -----
    * `help_message`: multiline str containing --help message when you 
      type: "my_command --help"
    * `argv`: sys.argv list containing command arguments
    * `argument_number`: exact number of arguments (if None it does not 
      matter)
    * `min_arg_number`: minimum number of arguments
    * `command_name` : command name
  
  Output 
  ------
    * Prints help message and stops command execution when you type 
      'nome_comando --help'
    * Prints error message and stops command execution when 
      `argument_number` is wrong
  """
  # help
  if len(argv) > 1 and (argv[1] == "--help" or argv[1] == "-h"):
    print(help_message)
    sys.exit()
  # wrong arg number
  if argument_number is not None:
    if len(argv) != argument_number + 1:
      print(f"ERROR: Wrong Argument Number ",
            f"({len(argv)-1} instead of {argument_number})")
      print(f"type '{command_name} --help' for more info")
      sys.exit()
  # min arg number
  if not len(argv) - 1 >= min_arg_number:
    print(f"ERROR: Not Enough Arguments ", 
          f"(minimum argument number = {min_arg_number})")
    print(f"type '{command_name} --help' for more info")
    sys.exit()


def must_end_with_pdf(fname: str) -> str:
  """
  This function makes sure that input str `fname`
  ends or will be ending with ".pdf"
  """
  if not fname.endswith(".pdf"):
    return fname + ".pdf"
  return fname


def add_one_to_counter(command_name) -> None:
  """
  Call this function at the end of a command_file.py to
  add +1 usage to the counter. This counter will save
  how many times we use that command
  """
  # get the full path of this file
  this_file_full_path = os.path.abspath(__file__)
  # get full path of data folder
  main_folder_full_path = os.path.dirname(this_file_full_path)
  # counter file full_path
  full_path_counter_json = os.path.join(main_folder_full_path, 
                                        COUNTER_JSON_NAME)
  # create file if it does not exists
  if not os.path.exists(full_path_counter_json):
    print(f"Error: missing file {full_path_counter_json}")
    sys.exit()

  with open(full_path_counter_json, "r") as jsonfile:
    # load dictionary
    counter_json = json.load(jsonfile)
  # add +1 to the frequency dictionary
  if command_name not in counter_json:
    counter_json[command_name] = 1
  else:
    counter_json[command_name] += 1
  # save progress
  with open(full_path_counter_json, "w") as jsonfile:
    json.dump(counter_json, jsonfile, indent=2)


def choose_out_pdf_name() -> str | NoReturn:
  """
  This function lets you choose a pdf output name.
  - If the name already exists then it asks you whether to overvrite it.
    If your choice is No then it restarts so you can choose another name
  - If you want to exit just throw an KeyboardInterrupt exception just 
    press Ctrl+c on terminal

  ## Output
  `str` with a pdf name (that will end with '.pdf')

  """
  while True:
    try:
      input_pdf: str = input(
        "\nEnter output filename (it may or may not end with '.pdf')\n"
        "(press Ctrl+C (^C signal interrupt) to exit): "
      )
    except KeyboardInterrupt:
      print()
      sys.exit()

    pdf_name: str = must_end_with_pdf(input_pdf)

    # if the file already exists ask what to do
    if os.path.isfile(pdf_name):
      print(f"\nWarning: file '{pdf_name}' already exists,")
      overwrite_choice: str = input("do you want to overwrite it?\n[y,N]: ")
      # choice with No as default (because "" in "nN" is True)
      if overwrite_choice in "nN":
        pass
      elif overwrite_choice in "sSyY":
        return pdf_name
      
    else:
      return pdf_name