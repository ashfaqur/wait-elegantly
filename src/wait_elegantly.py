import logging
import time
from argparse import ArgumentParser

import yaml

from command import COMMANDS_KEY
from command import Command

logger = logging.getLogger(__name__)


def wait_elegantly(config: str, triage: str) -> None:
    logger.debug(f"Loading yaml configuration file: {config}")
    if triage:
        logger.debug(f"Using triage file: {triage}")
    else:
        logger.debug("No triage file given")
    with open(config, "r") as f:
        data = yaml.safe_load(f)
    start_time = time.time()
    [Command(command).run(triage) for command in data[COMMANDS_KEY]]
    logger.info(f"Total time: {round(time.time() - start_time)}s")


def args_parser() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(
        description="Wait elegantly while commands executes"
    )
    arg_parser.add_argument("config", type=str, help="Path to a config yaml file")
    arg_parser.add_argument(
        "-t", "--triage", type=str, help="Path to a triage error json file"
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )
    return arg_parser


if __name__ == "__main__":
    parser: ArgumentParser = args_parser()
    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=log_level,
        datefmt="%H:%M:%S",
    )
    config_file: str = args.config
    triage_file: str = args.triage
    wait_elegantly(config_file, triage_file)
