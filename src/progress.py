import sys
from typing import List

from progressbar import ProgressBar, Percentage, Bar, GranularBar, ETA

SHOW_PROGRESS_BAR_FROM = 2  # seconds


class Progress:
    def __init__(self, history: List[int], granular: bool):
        self.avg_time: int = -1
        self.max_time: int = -1
        self.min_time: int = -1
        self.animation: list[str] = [".", "..", "..."]
        self.animation_index = 0
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
            pass

    def update(self) -> None:
        if self.bar:
            if self.bar.value < self.bar.max_value:
                self.bar.update(self.bar.value + 1)
        else:
            sys.stdout.write(f"\rWorking {self.animation[self.animation_index]}")
            sys.stdout.flush()
            self.animation_index = self.animation_index + 1
            if self.animation_index > len(self.animation):
                self.animation_index = 0

    def finish(self) -> None:
        if self.bar:
            self.bar.finish()
