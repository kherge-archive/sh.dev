from .. import CONFIG_DIR
from pathlib import Path

import json
import logging
import os

logger = logging.getLogger(__name__)

def get(name: str):
    """Reads the value of the configuration setting."""
    path = _toPath(name)

    if path.exists():
        logger.debug(f"reading {name} from {path}")

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

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

        path.unlink()
    else:
        logger.debug(f"writing {name} to {path}")

        with path.open("w", encoding="utf-8") as file:
            json.dump(value, file)

def default(name: str, value):
    """Sets the default value for a configuration setting if not already set."""
    if not exists(name):
        set(name, value)

def _toPath(name: str) -> Path:
    return Path(os.path.join(CONFIG_DIR, name + ".json"))
