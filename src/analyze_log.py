import json
import logging
import os
from argparse import ArgumentParser
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


def analyze_log_file(log_file_path: str, triage_file_path: str) -> Tuple[str, str]:
    logger.debug(f"Given log file path: {log_file_path}")
    check_valid_file(log_file_path)
    logger.debug(f"Given triage file path: {triage_file_path}")
    check_valid_file(triage_file_path)
    logs: List[str] = load_logs(log_file_path)
    triages: Dict[str, str] = load_triages(triage_file_path)
    analysis: Tuple[str, str] = look_for_error(logs, triages)
    return analysis


def look_for_error(logs: List[str], triages: Dict[str, str]) -> Tuple[str, str]:
    for line in logs:
        for k, v in triages.items():
            if k in line:
                logger.info("------------------------------------------------")
                logger.info(f"ERROR FOUND:   {line.strip()}")
                logger.info(f"RESOLUTION:    {v}")
                logger.info("------------------------------------------------")
                return line, v
    logger.debug("Unknown Error")
    return "", ""


def check_valid_file(given_file_path: str) -> None:
    if not os.path.isfile(given_file_path):
        raise ValueError(
            f"{given_file_path} is not a valid file path or the file does not exist on disk"
        )


def load_logs(log_file_path: str) -> List[str]:
    with open(log_file_path, "r") as f:
        lines: List[str] = [line.rstrip() for line in f]
        return lines


def load_triages(triage_file_path: str) -> Dict[str, str]:
    try:
        with open(triage_file_path, "r") as f:
            triages: Dict[str, str] = json.load(f)
            return triages
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON file: {e}")


def args_parser() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(description="Analyze log file")
    arg_parser.add_argument("path", type=str, help="Path to a log file")
    arg_parser.add_argument("triage_file_path", type=str, help="a path to another file")
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
    log_file: str = args.path
    triage_file: str = args.triage_file_path
    analyze_log_file(log_file, triage_file)
