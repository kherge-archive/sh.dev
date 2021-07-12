from os import environ, path
from pathlib import Path
from typing import Final

__all__ = ["cli", "command"]

# The path to the build directory.
DOCKER_DIR: Final[Path] = path.normpath(path.join(
    path.dirname(__file__),
    "..",
    "docker"
))

# The path to the configuration directory.
CONFIG_DIR: Final[Path] = Path(path.normpath(path.join(
    environ.get("XDG_CONFIG_HOME") or path.join(Path.home(), ".config"),
    "dev"
)))

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir(mode=0o755, parents = True)
