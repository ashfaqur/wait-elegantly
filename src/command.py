import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import List, Dict

from analyze_log import analyze_log_file
from progress import Progress

COMMANDS_KEY = "commands"
COMMAND_NAME = "name"
COMMAND_ID = "id"
COMMAND_VALUES = "values"

logger = logging.getLogger(__name__)

root: Path = Path(__file__).parent.parent


class Command:
    def __init__(self, command: Dict[str, Any]):
        self.name: str = command[COMMAND_NAME]
        self.id: str = command[COMMAND_ID]
        self.values: List[str] = command[COMMAND_VALUES]

    def run(self, triage_file: str) -> None:
        history_file: Path = root / Path(f"build/history/{self.id}.txt")
        history_times: List[int] = get_history_times(history_file)

        avg_time: int = 0

        if history_times:
            avg_time = round(sum(history_times) / len(history_times))
            logger.debug(f"Average time to complete: {avg_time}s")

        log_file_path: Path = get_log_file_path(self.id)
        logger.info(f"Running command '{self.name}' with log: {log_file_path}")

        with open(log_file_path, "w") as log_file:
            start_time = time.time()
            process = subprocess.Popen(
                self.values, stdout=log_file, stderr=log_file, universal_newlines=True
            )
            progress = Progress(history_times, False)
            while process.poll() is None:
                time.sleep(1)
                progress.update()
            total_time = round(time.time() - start_time)
            progress.finish()

            if process.returncode != 0:
                logger.error(f"Command '{self.name}' FAILED")
                if triage_file:
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


def get_log_file_path(command_id: str) -> Path:
    log_dir: Path = root / Path("build/log")
    log_dir.mkdir(parents=True, exist_ok=True)
    formatted_timestamp: str = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    log_file_name: str = f"{command_id}_{formatted_timestamp}.txt"
    log_file_path: Path = log_dir / log_file_name
    return log_file_path


def get_history(path: Path) -> Path:
    history = Path(path)
    history.parent.mkdir(parents=True, exist_ok=True)
    history.touch()
    return history


def get_history_times(path: Path) -> List[int]:
    history: Path = get_history(path)
    with open(history, "r") as f:
        numbers: List[int] = [int(line.strip()) for line in f]
        return numbers


def add_history_time(path: Path, total_time: int) -> None:
    history: Path = get_history(path)
    with history.open("a") as f:
        f.write(f"{total_time}\n")
