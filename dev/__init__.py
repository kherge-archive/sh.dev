from os import path
from typing import Final

__all__ = ["cli", "command"]

# The path to the build directory.
DOCKER_DIR: Final[Path] = path.normpath(path.join(
    path.dirname(__file__),
    "..",
    "docker"
))
