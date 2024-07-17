import sys

def help_and_error(help_message:str, argv:list, argument_number:int=None) -> None:
  """
  Input
  -----
    * `help_message`: multiline str containing --help message when you type: "my_command --help"
    * `argv`: sys.argv list containing command arguments
    * `argument_number`: exact number of arguments (if None it does not matter)
  
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
      print("type 'command_name --help' for more info")
      sys.exit()




