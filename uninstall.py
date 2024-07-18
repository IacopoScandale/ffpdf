from data.strings import COMMANDS_BAT, COMMANDS_SH
import os

# title
print("=================================")
print("||   UNINSTALL PDF COMMANDS    ||")
print("=================================",end="\n\n")

# info
print("This uninstaller is going only to un-do 'setup.py' (except deleting venv)")
print("Then just delete this folder for completely remove PDF Commands")


# get the full path of this file
this_file_full_path = os.path.abspath(__file__)
# get full path of project folder
main_folder_full_path = os.path.dirname(this_file_full_path)
# move to that directory
os.chdir(main_folder_full_path)


# windows
if os.name == "nt": 
  # commands.bat full path
  # add one " for being sure that paths that contain spaces will be supported (in regedit it will write exactly "path" with one ")
  commands_bat_full_path_str = f'\\"{os.path.join(os.getcwd(), COMMANDS_BAT)}\\"'

  # get regedit AutoRun paths Values in Command Processor
  tmp_file_path = "tmp.txt"
  os.system(f'reg query "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun > "{tmp_file_path}"')

  # read tmpfile and get all paths in AutoRun
  with open(tmp_file_path, "r") as txtfile:
    lines = txtfile.readlines()
  # delete the tmp file
  os.remove(tmp_file_path)
  # find existing paths
  for line in lines:
    if "AutoRun" in line:
      # get the list of all paths in value "AutoRun"
      paths = line[21:].strip().split("&")


  # if a path starts and ends with ", we must add \ in front of "
  for i, path in enumerate(paths):
    # strip every path: it could contain spaces because we are splitting with "&"
    # but each path could be separated with " & "
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
      # add \ in front of each "
      path = f'\\"{path[1:-1]}\\"'
    # refresh path in paths list
    paths[i] = path

      
  # remove commands.bat file full path from the values
  if paths != [""]:
    paths.remove(commands_bat_full_path_str)

  # join all paths separated by &
  concatenated_paths = " & ".join(paths)
  # print(concatenated_paths)
  os.system(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun /t REG_SZ /d "{concatenated_paths}" /f')

  # delete `commands.bat`
  if os.path.exists(COMMANDS_BAT):
    os.remove(COMMANDS_BAT)






# linux
elif os.name == "posix":











  # delete `commands.bat`
  os.remove(COMMANDS_BAT)
  # TODO



else:
  raise OSError(f"Your os {os.name} is not supported")