from sys import stdout
from typing import List

from progressbar import ProgressBar, Percentage, Bar, GranularBar, ETA

SHOW_PROGRESS_BAR_FROM = 2  # seconds
PROGRESS_DOT_CHAR_COUNT = 50


class Progress:
    def __init__(self, history: List[int], granular: bool):
        self.avg_time: int = -1
        self.max_time: int = -1
        self.min_time: int = -1
        self.counter: int = 0
        self.bar = None

        if history:
            self.avg_time = round(sum(history) / len(history))
            self.max_value = max(history)
            self.min_value = min(history)

        if self.avg_time > SHOW_PROGRESS_BAR_FROM:
            if granular:
                widgets = [
                    Percentage(),
                    " ",
                    GranularBar(),
                    " ",
                    ETA(),
                ]
            else:
                widgets = [
                    Percentage(),
                    " ",
                    Bar(),
                    " ",
                    ETA(),
                ]
            self.bar = ProgressBar(
                widgets=widgets,
                max_value=self.avg_time,
            )
            self.bar.start()
        else:
            stdout.write("\rIn Progress...")

    def update(self) -> None:
        self.counter = self.counter + 1
        if self.bar:
            if self.bar.value < self.bar.max_value:
                self.bar.update(self.bar.value + 1)
        else:
            stdout.write(".")
            stdout.flush()
            if self.counter % PROGRESS_DOT_CHAR_COUNT == 0:
                stdout.write("\n\rIn Progress...")
                stdout.flush()

    def finish(self) -> None:
        if self.bar:
            self.bar.finish()
        else:
            stdout.write("\n")
            stdout.flush()

    def expected_time(self) -> int:
        return self.avg_time
