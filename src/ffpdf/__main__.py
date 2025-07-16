import json

from rich import print

from .data.strings import (
    COMMAND,
    DESCRIPTION,
    FILE_COUNTER_JSON,
    PACKAGE_NAME,
    SUBCOMMANDS,
)
from .data.utils import add_one_to_counter


def load_usage_counter() -> dict[str, int]:
    """
    Load data from `FILE_USAGE_COUNTER_JSON` if exists, otherwise
    return an empty dict
    """
    # `FILE_COUNTER_JSON` always exists
    with FILE_COUNTER_JSON.open("r", encoding="utf-8") as jsonfile:
        usage_counter: dict[str, int] = json.load(jsonfile)
    return usage_counter


def show_infos() -> None:
    """
    TODO
    """
    # load user usage-counter dict and show package infos
    usage_counter: list[str, int] = load_usage_counter()

    print(f'{PACKAGE_NAME} python package: "{DESCRIPTION}"')
    print(f"\n[bold]Commands:[/bold]{' ' * 14}[bold]Times Used:[/bold]")
    print("—" * 38)
    total: int = 0
    for i, command in enumerate(SUBCOMMANDS, 1):
        times_used: int = usage_counter.setdefault(command, 0)
        total += times_used
        print(f"{i:>4}. {command:<20} {times_used:>7}")
    print("—" * 38)
    print(f"      [bold]Total:{' ' * 15}{total:>7}[/bold]\n")

    # +1 to usage counter
    add_one_to_counter(COMMAND)


if __name__ == "__main__":
    show_infos()
