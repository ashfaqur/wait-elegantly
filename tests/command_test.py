from unittest.mock import patch

import pytest

from src.command import Command, get_cmd_name, get_cmd_id, get_log_file_path


def test_get_cmd_name() -> None:
    command = {"name": "test_command"}
    assert get_cmd_name(command) == "test_command"

    with pytest.raises(ValueError):
        command = {"name": "test_command_é"}
        get_cmd_name(command)

    with pytest.raises(ValueError):
        command = {"name": "test_command" * 100}
        get_cmd_name(command)


def test_get_cmd_id() -> None:
    command = {"id": "test_command"}
    assert get_cmd_id(command) == "test_command"

    with pytest.raises(ValueError):
        command = {"id": "test_command!"}
        get_cmd_id(command)

    with pytest.raises(ValueError):
        command = {"id": "test_command" * 100}
        get_cmd_id(command)


def test_run_command_success() -> None:
    command = {
        "name": "test_command",
        "id": "test_command",
        "values": ["echo", "hello"],
    }
    cmd = Command(command)
    log_file_path = get_log_file_path("test_run_command_success.txt")
    with patch("subprocess.Popen"):
        process = cmd.run_command(log_file_path)
        process.wait()
        assert process.returncode == 0


def test_run_command_failure() -> None:
    command = {
        "name": "test_command",
        "id": "test_command",
        "values": ["ls", "/invalid/path"],
    }
    cmd = Command(command)
    log_file_path = get_log_file_path("test_run_command_failure.txt")
    with patch("subprocess.Popen"):
        process = cmd.run_command(log_file_path)
        process.wait()
        assert process.returncode != 0
