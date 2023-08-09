import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import List, Dict

import progressbar

from analyze_log import analyze_log_file

COMMANDS_KEY = "commands"
COMMAND_NAME = "name"
COMMAND_ID = "id"
COMMAND_VALUES = "values"

logger = logging.getLogger(__name__)


class Command:
    def __init__(self, command: Dict[str, Any]):
        self.name: str = command[COMMAND_NAME]
        self.id: str = command[COMMAND_ID]
        self.values: List[str] = command[COMMAND_VALUES]

    def run(self, triage_file: str) -> None:
        log_dir = Path("build/log")
        log_dir.mkdir(parents=True, exist_ok=True)

        history_file: str = f"build/history/{self.id}.txt"
        history_times: List[int] = get_history_times(history_file)

        avg_time: int = 0

        if history_times:
            avg_time = round(sum(history_times) / len(history_times))
            logger.debug(f"Average time to complete: {avg_time}s")

        now = datetime.now()
        formatted_timestamp = now.strftime("%H-%M-%S_%d-%m-%Y")
        log_file_name = f"{self.id}_{formatted_timestamp}.txt"
        log_file_path = log_dir / log_file_name

        logger.info(f"Running command: {self.name}")
        logger.info(f"Log file located in: {log_file_path}")

        with open(log_file_path, "w") as log_file:
            start_time = time.time()
            process = subprocess.Popen(
                self.values, stdout=log_file, stderr=log_file, universal_newlines=True
            )

            bar = progressbar.ProgressBar(
                widgets=[
                    progressbar.Percentage(),
                    " ",
                    progressbar.GranularBar(),
                    " ",
                    progressbar.ETA(),
                ],
                max_value=avg_time,
            )
            bar.start()
            while process.poll() is None:
                time.sleep(1)
                if bar.value < bar.max_value:
                    bar.update(bar.value + 1)
            total_time = round(time.time() - start_time)
            bar.finish()

            if process.returncode != 0:
                logger.error(f"Process '{self.name}' FAILED")
                analyze_log_file(log_file_path, triage_file)
            else:
                result: str = get_time_diff_result(total_time, avg_time)
                logger.info(f"Command '{self.name}' SUCCESSFUL {result}")
                logger.debug(f"Time saved in: {history_file}")
                add_history_time(history_file, total_time)

            logger.debug("----- COMMAND FINISHED -----")


def get_time_diff_result(total_time: int, expected_time: int) -> str:
    difference: int = total_time - expected_time
    if difference > 0:
        return f"in {total_time}s. Took {abs(difference)}s MORE than expected."
    else:
        return f"in {total_time}s. Took {abs(difference)}s less than expected."


def get_history(path: str) -> Path:
    history = Path(path)
    history.parent.mkdir(parents=True, exist_ok=True)
    history.touch()
    return history


def get_history_times(path: str) -> List[int]:
    history: Path = get_history(path)
    with open(history, "r") as f:
        numbers: List[int] = [int(line.strip()) for line in f]
        return numbers


def add_history_time(path: str, total_time: int) -> None:
    history: Path = get_history(path)
    with history.open("a") as f:
        f.write(f"{total_time}\n")
