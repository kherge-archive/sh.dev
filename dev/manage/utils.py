from . import config

from typing import Final

# The label name.
LABEL_NAME: Final[str] = "io.github.kherge.sh-dev"

def get_label(with_name=True):
    """Returns the label used for all managed objects."""
    return (f"{LABEL_NAME}=" if with_name else "") + config.get("core.label")
