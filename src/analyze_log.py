import argparse
import logging
import os

logger = logging.getLogger(__name__)


def analyze_log_file(log_file_path: str, triage_file_path: str) -> None:
    logging.info(f"Given log file path: {log_file_path}")
    check_valid_file(log_file_path)
    logging.info(f"Given triage file path: {triage_file_path}")
    check_valid_file(triage_file_path)


def check_valid_file(given_file_path: str) -> None:
    if not os.path.isfile(given_file_path):
        raise ValueError(
            f"{given_file_path} is not a valid file path or the file does not exist on disk"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze log file")
    parser.add_argument("path", type=str, help="Path to a log file")
    parser.add_argument("triage_file_path", type=str, help="a path to another file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )

    args = parser.parse_args()
    log_level = logging.WARNING
    # Set the log level
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    log_file: str = args.path
    triage_file: str = args.triage_file_path
    analyze_log_file(log_file, triage_file)
