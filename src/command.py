import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import progressbar

from analyze_log import analyze_log_file

COMMANDS_KEY = "commands"
COMMAND_NAME = "name"
COMMAND_ID = "id"
COMMAND_VALUES = "values"

logger = logging.getLogger(__name__)


class Command:
    def __init__(self, command: dict[str, Any]):
        self.name: str = command[COMMAND_NAME]
        self.id: str = command[COMMAND_ID]
        self.values: list[str] = command[COMMAND_VALUES]

    def run(self, triage_file: str) -> None:
        log_dir = Path("build/log")
        log_dir.mkdir(parents=True, exist_ok=True)

        history = Path(f"build/history/{self.id}.txt")
        history.parent.mkdir(parents=True, exist_ok=True)
        history.touch()

        with open(history, "r") as f:
            numbers: list[int] = [int(line.strip()) for line in f]

        logger.info(f"Running command: {self.name}")

        if numbers:
            expected_time = sum(numbers) / len(numbers)
            logger.info(f"Average time to complete: {expected_time}s")
        else:
            expected_time = 0

        now = datetime.now()
        formatted_timestamp = now.strftime("%H-%M-%S_%d-%m-%Y")
        log_file_name = f"{self.id}_{formatted_timestamp}.txt"
        log_file_path = log_dir / log_file_name
        logger.error(f"Log file located in {log_file_path}")

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
                max_value=expected_time,
            )
            bar.start()
            while process.poll() is None:
                time.sleep(1)
                if bar.value < bar.max_value:
                    bar.update(1)
            total_time = round(time.time() - start_time)
            bar.finish()

            difference = round(total_time - expected_time)
            if difference > 0:
                logger.info(
                    f"Total {total_time}s. Took {abs(difference)}s MORE than expected."
                )
            else:
                logger.info(
                    f"Total {total_time}s. Took {abs(difference)}s less than expected."
                )

            if process.returncode != 0:
                logger.error(f"Process '{self.name}' FAILED")
                analyze_log_file(log_file_path, triage_file)
            else:
                logger.info(
                    f"Process '{self.name}' SUCCESSFUL. Time saved in file {history}"
                )
                with history.open("a") as f:
                    f.write(f"{total_time}\n")

            logger.info("-------------------------------------------------------")
