import sys

def help_and_error(help_message:str, argv:list, argument_number:int=None, min_arg_number:int=0, command_name:str="command_name") -> None:
  """
  Input
  -----
    * `help_message`: multiline str containing --help message when you type: "my_command --help"
    * `argv`: sys.argv list containing command arguments
    * `argument_number`: exact number of arguments (if None it does not matter)
    * `min_arg_number`: minimum number of arguments
    * `command_name` : command name
  
  Output 
  ------
    * Prints help message and stops command execution when you type 'nome_comando --help'
    * Prints error message and stops command execution when `argument_number` is wrong
  """
  # help
  if len(argv) > 1 and (argv[1] == "--help" or argv[1] == "-h"):
    print(help_message)
    sys.exit()
  # wrong arg number
  if argument_number is not None:
    if len(argv) != argument_number + 1:
      print(f"ERROR: Wrong Argument Number ({len(argv)-1} instead of {argument_number})")
      print(f"type '{command_name} --help' for more info")
      sys.exit()
  # min arg number
  if not len(argv) - 1 >= min_arg_number:
    print(f"ERROR: Not Enough Arguments (minimum argument number = {min_arg_number})")
    print(f"type '{command_name} --help' for more info")
    sys.exit()


def must_end_with_pdf(fname: str) -> str:
  """
  This function makes sure that input str 'fname'
  ends or will be ending with ".pdf"
  """
  if not fname.endswith(".pdf"):
    return fname + ".pdf"
  return fname