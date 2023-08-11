import pytest

from src.analyze_log import analyze_log_file, check_valid_file, load_logs, load_triages


def test_analysis_empty() -> None:
    result = analyze_log_file(
        "tests/assets/sample_log_file_with_no_error.txt",
        "tests/assets/sample_triage_file.json",
    )
    assert result == ("", "")


def test_analysis_found_error() -> None:
    result = analyze_log_file(
        "tests/assets/sample_log_file_with_error.txt",
        "tests/assets/sample_triage_file.json",
    )
    assert result == (
        "[ERROR] Ohh an error happened. Wonder what is it.",
        "No worries. Here is a workaround!",
    )


def test_check_valid_file() -> None:
    with pytest.raises(ValueError):
        check_valid_file("invalid/file/path")


def test_load_logs() -> None:
    logs = load_logs("tests/assets/sample_log_file_with_no_error.txt")
    assert len(logs) == 2
    assert logs[0] == "[INFO] Here is some sample logs."
    assert logs[1] == "[INFO] Some more trivial logs."


def test_load_triages() -> None:
    triages = load_triages("tests/assets/sample_triage_file.json")
    assert len(triages) == 1
    assert (
        triages["[ERROR] Ohh an error happened"] == "No worries. Here is a workaround!"
    )
