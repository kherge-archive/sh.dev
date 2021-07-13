from . import config

from typing import Final

# The name of the label used to segregate workspaces.
LABEL_NAME: Final[str] = "io.github.kherge.sh-dev.workspace"

def get_label(with_name=True):
    """Returns the label used for all managed objects."""
    return (f"{LABEL_NAME}=" if with_name else "") + config.get("core.label")
