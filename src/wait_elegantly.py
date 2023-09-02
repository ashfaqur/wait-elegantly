import logging
import time
from argparse import ArgumentParser
from datetime import timedelta

import yaml

from command import COMMANDS_KEY
from command import Command

logger = logging.getLogger(__name__)


def wait_elegantly(config: str, triage: str, granular: bool) -> None:
    """
    Executes a series of commands specified in a configuration file and reports progress.

    :param config: The path to the configuration file in YAML format.
    :type config: str
    :param triage: The path to the triage file containing error resolutions.
    :type triage: str
    :param granular: Whether to use a granular progress bar.
    :type granular: bool
    """
    logger.debug(f"Loading yaml configuration file: {config}")
    if triage:
        logger.debug(f"Using triage file: {triage}")
    else:
        logger.debug("No triage file given")
    with open(config, "r") as f:
        data = yaml.safe_load(f)
    start_time = time.time()
    [Command(command).run(triage, granular) for command in data[COMMANDS_KEY]]

    total_time = str(timedelta(seconds=round(time.time() - start_time)))

    logger.info(f"Total time: {total_time}")


def args_parser() -> ArgumentParser:
    """
    Parses command line arguments.

    :return: An ArgumentParser object containing parsed command line arguments.
    :rtype: ArgumentParser
    """
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
    arg_parser.add_argument(
        "-g", "--granular", action="store_true", help="Set progress bar to granular"
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
    granular_bar: bool = args.granular
    wait_elegantly(config_file, triage_file, granular_bar)
