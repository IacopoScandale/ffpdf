# from data.utils import windows_alias_command_line
from data import strings
import os, sys


# create virtual environment
if not os.path.exists("venv"):
  print("Creating Virtual Environment 'venv'")
  os.system(f"{sys.executable} -m venv venv")  
  print("Done!\n")


# install from requirements.txt
print("Installing dependencies:")
if os.name == "nt": # windows
  os.system(f"{strings.PIP_VENV_WIN} install -r requirements.txt")
  print("Done!\n")
elif os.name == "posix": # linux
  os.system("")
  print("Done!\n")
else: # other os
  raise OSError(f"Your os {os.name} not supported")


# create .bat and .sh aliases files
# Windows Setup
python_venv_full_path = os.path.join(os.getcwd(), strings.PYTHON_VENV_WIN)

def windows_alias_command_line(command_name:str, filename_py:str, args:str="") -> str:
  """
  Create windows command line for file comands.bat
  Input:
  - `filename_py:str` name of the python file to call
  - `command_name:str` name of the alias
  - `args:str=""` insert other default arguments (separated by a space) if needed
  """
  command_file_path = os.path.join(os.getcwd(), filename_py)
  return f'doskey {command_name} = "{python_venv_full_path}" "{command_file_path}" {args} $*\n'


if os.name == "nt":
  # windows echo off
  commands = "@echo off\n\n"
  # fname_format command
  commands += windows_alias_command_line(strings.FNAME_FORMAT_COMM, "comm_filename_format.py")
  

  
  # Write commands on commands.bat file
  with open(strings.COMMANDS_BAT, "w") as txtfile:
    txtfile.write(commands)


  # Regedit Part
  # path is inside \"...\" because in this way paths containing spaces are supported
  commands_bat_full_path_str = f'\\"{os.path.join(os.getcwd(), strings.COMMANDS_BAT)}\\"'

  # add automatically commands.bat file to regedit AutoRun Value in Command Processor
  tmp_file_path = "tmp.txt"
  try:
    os.system(f'reg query "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun > "{tmp_file_path}"')
  except:
    print("Error: you must run this script as administrator")
    sys.exit()

  # read tmpfile and get all paths in AutoRun
  with open(tmp_file_path, "r") as txtfile:
    lines = txtfile.readlines()
  # delete the tmp file
  os.remove(tmp_file_path)
  # find existing paths
  for line in lines:
    if "AutoRun" in line:
      # get the list of all paths in value "AutoRun"
      paths_in_line = line[21:].strip()
      if paths_in_line == "": # case: no paths
        paths = []
      elif "&" in paths_in_line: # case: more than a path
        paths = paths_in_line.split("&")
      else: # case: a single path
        paths = [paths_in_line]
      
  # if a path starts and ends with ", we must add \ in front of "
  for i, path in enumerate(paths):
    # strip every path: it could contain spaces because we are splitting with "&"
    # but each path could be separated with " & "
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
      # add \ in front of each "
      paths[i] = f'\\"{path[1:-1]}\\"'

  # add commands.bat file full path to the values
  if commands_bat_full_path_str not in paths:
    paths.append(commands_bat_full_path_str)

  # join all paths separated by &
  concatenated_paths = " & ".join(paths)
  # print(concatenated_paths)
  os.system(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun /t REG_SZ /d "{concatenated_paths}" /f')




# linux and (i hope :) macOS Setup
elif os.name == "posix":
  # TODO
  pass





  # TODO add automatically file to current shell.rc

else:
  raise OSError(f"Your os {os.name} is not supported")






