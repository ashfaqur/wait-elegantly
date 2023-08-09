import argparse
import logging

import yaml

from command import COMMANDS_KEY
from command import Command

logger = logging.getLogger("Wait_Elegantly")


def wait_elegantly(config: str, triage_file_path: str) -> None:
    logger.info(f"Loading yaml configuration file {config}")
    with open(config, "r") as f:
        data = yaml.safe_load(f)

    [Command(command).run(triage_file_path) for command in data[COMMANDS_KEY]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wait Elegantly while commands executes"
    )
    parser.add_argument("path", type=str, help="Path to a config yaml file")
    parser.add_argument("triage", type=str, help="Path to a triage error json file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    config_file: str = args.path
    triage_file: str = args.triage

    logger.info("------ Wait Elegantly --------s")
    wait_elegantly(config_file, triage_file)
