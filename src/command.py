from typing import Any

COMMANDS_KEY = "commands"
COMMAND_NAME = "name"
COMMAND_ID = "id"
COMMAND_VALUES = "values"


class Command:
    def __init__(self, command: dict[str, Any]):
        self.name: str = command[COMMAND_NAME]
        self.id: str = command[COMMAND_ID]
        self.values: list[str] = command[COMMAND_VALUES]
        print(self.name)
        print(self.id)
        print(self.values)
