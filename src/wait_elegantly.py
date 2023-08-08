import argparse
import logging

import yaml

from command import COMMANDS_KEY
from command import Command


def wait_elegantly(config: str) -> None:
    with open(config, "r") as f:
        data = yaml.safe_load(f)

    commands = [Command(command) for command in data[COMMANDS_KEY]]
    print(commands)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wait Elegantly while commands executes"
    )
    parser.add_argument("path", type=str, help="Path to a config yaml file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )

    args = parser.parse_args()
    log_level = logging.INFO
    # Set the log level
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    config_file: str = args.path

    wait_elegantly(config_file)
