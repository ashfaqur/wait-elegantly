from src.analyze_log import analyze_log_file


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
