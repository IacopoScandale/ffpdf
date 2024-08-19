from .data.utils import add_one_to_counter
from .data import strings
from argparse import ArgumentParser, Namespace
import os
import json


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description="Shows all PDF commands"
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  _ = get_arguments()

  here: str = os.path.dirname(os.path.abspath(__file__)) 
  full_path_counter_json: str = os.path.join(here, strings.COUNTER_JSON)

  # +1 to usage counter
  add_one_to_counter(strings.PACKAGE_NAME)

  # open counter json as dictionary
  with open(full_path_counter_json, "r") as jsonfile:
    usage_counter: dict[str,int] = json.load(jsonfile)

  # print all commands
  print("\nPDF Commands:\t\tTimes Used:")
  for command in strings.COMMANDS.keys():
    times_used = usage_counter.setdefault(command, 0)
    print(f"  · {command:<15} {times_used:>14}")

  print("\nType 'command_name -h' for more info")