from pdf_commands.data.strings import *
from setuptools import setup, find_packages


def create_command(command_name: str, script_to_call: str) -> str:
  """
  Input:
  ------
  * `command_name`   name of the command 
  * `script_to_call` name of the script to be called with commands_name
    without .py extension

  Outupt
  ------
  command string for 'console_scripts' in setup entry_points
  """
  return f"{command_name}={PACKAGE_NAME}.{script_to_call}:main"


def get_requirements() -> list[str]:
  """
  reads requirements from requirements.txt file and return the
  `install_requires` list of setup() in setuptools
  """
  with open("requirements.txt", "r") as txt:
    lines: list[str] = txt.read().splitlines()
    
    # strip every line and remove commented ones:
    return [line.strip() for line in lines if not line.strip().startswith("#")]


setup(
  name=PACKAGE_NAME,
  version='0.1',
  packages=find_packages(),
  install_requires=get_requirements(),
  entry_points={
    'console_scripts': [
      create_command(name, file) for (name, file) in COMMANDS.items()
    ],
  },
)