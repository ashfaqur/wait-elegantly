import logging
import time
from datetime import datetime
from pathlib import Path
from subprocess import Popen
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
        """
        Initializes a Command object.

        :param command: A dictionary containing the command's name, id, and values.
        :type command: Dict[str, Any]
        """
        self.name: str = get_cmd_name(command)
        self.id: str = get_cmd_id(command)
        self.values: List[str] = command[COMMAND_VALUES]

    def run(self, triage_file: str, granular: bool) -> None:
        """
        Runs the command and reports progress.

        :param triage_file: The path to the triage file containing error resolutions.
        :type triage_file: str
        :param granular: Whether to use a granular progress bar.
        :type granular: bool
        """
        history_file: Path = root / Path(f"build/history/{self.id}.txt")
        history_times: List[int] = get_history_times(history_file)

        log_file_path: Path = get_log_file_path(self.id)
        logger.info(f"Running command '{self.name}' with log:\n{log_file_path}")

        start_time = time.time()
        process: Popen[Any] = self.run_command(log_file_path)
        progress: Progress = Progress(history_times, granular)
        update_progress(process, progress)
        total_time = round(time.time() - start_time)
        progress.finish()

        if process.returncode != 0:
            if triage_file:
                analyze_log_file(str(log_file_path), triage_file)
            raise RuntimeError(f"Command '{self.id}' FAILED")
        else:
            result: str = get_time_diff_result(total_time, progress.expected_time())
            logger.info(f"Command '{self.name}' SUCCESSFUL {result}")
            logger.debug(f"Time saved in: {history_file}")
            add_history_time(history_file, total_time)

            logger.debug("----- COMMAND FINISHED -----")

    def run_command(self, log: Path) -> Popen[Any]:
        """
        Runs the command and returns the process object.

        :param log: The path to the log file.
        :type log: Path
        :return: The process object representing the running command.
        :rtype: subprocess.Popen
        """
        with open(log, "w") as file:
            cmd_process = Popen(
                self.values, stdout=file, stderr=file, universal_newlines=True
            )
            return cmd_process


def update_progress(cmd_process: Popen[Any], cmd_progress: Progress) -> None:
    """
    Updates the progress of the running command.

    :param cmd_process: The process object representing the running command.
    :type cmd_process: subprocess.Popen
    :param cmd_progress: The Progress object representing the progress of the command.
    :type cmd_progress: Progress
    """
    while cmd_process.poll() is None:
        time.sleep(1)
        cmd_progress.update()


def get_cmd_name(command: Dict[str, Any]) -> str:
    """
    Returns the name of the command.

    :param command: A dictionary containing the command's name.
    :type command: Dict[str, Any]
    :return: The name of the command.
    :rtype: str
    :raises ValueError: If the name contains non-ASCII characters or if it is too long.
    """
    name: str = command[COMMAND_NAME]
    if not all(ord(c) < 128 for c in name):
        raise ValueError("Name contains non-ASCII characters")
    if len(name) >= 500:
        raise ValueError("Name is too long")
    return name


def get_cmd_id(command: Dict[str, Any]) -> str:
    """
    Returns the id of the command.

    :param command: A dictionary containing the command's id.
    :type command: Dict[str, Any]
    :return: The id of the command.
    :rtype: str
    :raises ValueError: If the id contains invalid characters or if it is too long.
    """
    cmd_id: str = command[COMMAND_ID]
    if not all(c.isalnum() or c in ("-", "_") for c in cmd_id):
        raise ValueError("ID must only contain alphanumeric with dash or underscores")
    if len(cmd_id) >= 100:
        raise ValueError("ID is too long, more than 100 characters")
    return cmd_id


def get_time_diff_result(total_time: int, expected_time: int) -> str:
    """
    Returns a string representation of the difference between the total time and expected time.

    :param total_time: The total time taken by the command.
    :type total_time: int
    :param expected_time: The expected time for the command to complete.
    :type expected_time: int
    :return: A string representation of the difference between the total time and expected time.
    :rtype: str
    """
    time_taken: str = f"in {total_time}s"
    difference_time: str = ""
    if expected_time > 0:
        difference: int = total_time - expected_time
        if difference > 0:
            difference_time = f"Took {abs(difference)}s MORE than expected."
        else:
            difference_time = f"Took {abs(difference)}s less than expected."

    return f"{time_taken}. {difference_time}"


def get_log_file_path(command_id: str) -> Path:
    """
    Returns the path to the log file for the given command id.

    :param command_id: The id of the command.
    :type command_id: str
    :return: The path to the log file for the given command id.
    :rtype: Path
    """
    log_dir: Path = root / Path("build/log")
    log_dir.mkdir(parents=True, exist_ok=True)
    formatted_timestamp: str = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    log_file_name: str = f"{command_id}_{formatted_timestamp}.txt"
    log_file_path: Path = log_dir / log_file_name
    return log_file_path


def get_history(path: Path) -> Path:
    """
    Returns a Path object representing the history file at the given path.

    :param path: The path to the history file.
    :type path: Path
    :return: A Path object representing the history file at the given path.
    :rtype: Path
    """
    history = Path(path)
    history.parent.mkdir(parents=True, exist_ok=True)
    history.touch()
    return history


def get_history_times(path: Path) -> List[int]:
    """
    Returns a list of integers representing the history times stored in the history file at the given path.

    :param path: The path to the history file.
    :type path: Path
    :return: A list of integers representing the history times stored in the history file at the given path.
    :rtype: List[int]
    """
    history: Path = get_history(path)
    with open(history, "r") as f:
        numbers: List[int] = [int(line.strip()) for line in f]
        return numbers


def add_history_time(path: Path, total_time: int) -> None:
    """
    Adds the given total time to the history file at the given path.

    :param path: The path to the history file.
    :type path: Path
    :param total_time: The total time to add to the history file.
    :type total_time: int
    """
    history: Path = get_history(path)
    with history.open("a") as f:
        f.write(f"{total_time}\n")
