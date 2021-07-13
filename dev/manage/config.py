from .. import CONFIG_DIR
from pathlib import Path

import functools
import json
import logging
import os

logger = logging.getLogger("dev.manage.config")

class ConfigError(Exception):
    """An error for configuration related issues."""

    # The error message.
    message: str

    # The name of the configuration setting.
    name: str

    # The previous error.
    previous: BaseException

    def __init__(self, name: str, message: str, previous: BaseException = None):
        self.message = message
        self.name = name
        self.previous = previous

@functools.cache
def get(name: str):
    """Reads the value of the configuration setting."""
    path = _toPath(name)

    if path.exists():
        logger.debug(f"reading {name} from {path}")

        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except BaseException as previous:
            raise ConfigError(name, "could not be read", previous)

    logger.debug(f"{name} is not set, using None")

    return None

def exists(name: str):
    """Checks if the file exists for the configuration setting."""
    path = _toPath(name)

    logger.debug(f"checking if {name} exists as {path}")

    exists = path.exists()

    logger.debug(name + ("exists" if exists else "does not exist"))

    return exists

def set(name: str, value):
    """Writes the value of the configuration setting."""
    path = _toPath(name)

    if value == None or value == "":
        logger.debug(f"deleting {name} from {path}")

        try:
            path.unlink()
        except BaseException as previous:
            raise ConfigError(name, "could not delete", previous)
    else:
        logger.debug(f"writing {name} to {path}")

        try:
            with path.open("w", encoding="utf-8") as file:
                json.dump(value, file)
        except BaseException as previous:
            raise ConfigError(name, "could not be written", previous)

def _toPath(name: str) -> Path:
    return Path(os.path.join(CONFIG_DIR, name + ".json"))
