from typing import List
from unittest.mock import patch

from src.progress import Progress


def test_progress_init_with_history() -> None:
    history: List[int] = [1, 2, 3]
    progress = Progress(history, False)
    assert progress.avg_time == 2
    assert progress.max_value == 3
    assert progress.min_value == 1


def test_progress_init_without_history() -> None:
    history: List[int] = []
    with patch("sys.stdout.write") as mock_stdout:
        Progress(history, False)
        mock_stdout.assert_called_with("\rIn Progress...")


def test_progress_update_with_bar() -> None:
    history: List[int] = [1, 2, 3]
    progress = Progress(history, False)
    with patch("time.sleep"):
        progress.update()
        assert progress.bar.value == 1


def test_progress_update_without_bar() -> None:
    history: List[int] = []
    progress = Progress(history, False)
    with patch("sys.stdout.write") as mock_stdout:
        with patch("time.sleep"):
            progress.update()
            mock_stdout.assert_called_with(".")


def test_progress_finish_with_bar() -> None:
    history: List[int] = [1, 2, 3]
    progress = Progress(history, False)
    with patch("progressbar.ProgressBar.finish") as mock_finish:
        progress.finish()
        mock_finish.assert_called_once()


def test_progress_finish_without_bar() -> None:
    history: List[int] = []
    progress = Progress(history, False)
    with patch("sys.stdout.write") as mock_stdout:
        progress.finish()
        mock_stdout.assert_called_with("\n")
