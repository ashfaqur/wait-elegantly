import argparse
import logging
import time

import yaml

from command import COMMANDS_KEY
from command import Command

logger = logging.getLogger(__name__)


def wait_elegantly(config: str, triage_file_path: str) -> None:
    logger.debug(f"Loading yaml configuration: {config}")
    with open(config, "r") as f:
        data = yaml.safe_load(f)

    start_time = time.time()
    [Command(command).run(triage_file_path) for command in data[COMMANDS_KEY]]
    logger.info(f"Total time: {round(time.time() - start_time)}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wait elegantly while commands executes"
    )
    parser.add_argument("config", type=str, help="Path to a config yaml file")
    parser.add_argument("triage", type=str, help="Path to a triage error json file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )

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

    logger.debug("------ Wait Elegantly --------")
    wait_elegantly(config_file, triage_file)
