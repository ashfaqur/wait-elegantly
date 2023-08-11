import logging
from sys import stdout
from typing import List

from progressbar import ProgressBar, Percentage, Bar, GranularBar, ETA

PROGRESS_DOT_CHAR_COUNT = 50

logger = logging.getLogger(__name__)


class Progress:
    def __init__(self, history: List[int], granular: bool):
        """
        Initializes a Progress object.

        :param history: A list of integers representing the history times.
        :type history: List[int]
        :param granular: Whether to use a granular progress bar.
        :type granular: bool
        """
        self.avg_time: int = -1
        self.max_time: int = -1
        self.min_time: int = -1
        self.counter: int = 0
        self.bar: ProgressBar = None

        if history:
            self.avg_time = round(sum(history) / len(history))
            self.max_value = max(history)
            self.min_value = min(history)

        if self.avg_time >= 0:
            widgets = [
                Percentage(),
                " ",
                GranularBar() if granular else Bar(),
                " ",
                ETA(),
            ]
            self.bar = ProgressBar(
                widgets=widgets,
                max_value=self.avg_time,
            )
            self.bar.start()
        else:
            logger.debug("ETA unavailable first time the command runs")
            stdout.write("\rIn Progress...")

    def update(self) -> None:
        """
        Updates the progress bar.
        """
        if self.bar:
            if self.bar.value < self.bar.max_value:
                self.bar.update(self.bar.value + 1)
        else:
            self.counter = self.counter + 1
            stdout.write(".")
            stdout.flush()
            if self.counter % PROGRESS_DOT_CHAR_COUNT == 0:
                stdout.write("\n\rIn Progress...")
                stdout.flush()

    def finish(self) -> None:
        """
        Finishes the progress bar.
        """
        if self.bar:
            self.bar.finish()
        else:
            stdout.write("\n")
            stdout.flush()

    def expected_time(self) -> int:
        """
        Returns the expected time for the command to complete.

        :return: The expected time for the command to complete.
        :rtype: int
        """
        return self.avg_time
