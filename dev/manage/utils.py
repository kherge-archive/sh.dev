from . import config
from docker.models.containers import Container
from docker.models.images import Image
from typing import Final, Union

import grp
import os
import pwd

# The name of the label used to segregate workspaces.
LABEL_NAME: Final[str] = "io.github.kherge.sh-dev.workspace"

def get_group_id():
    """Returns the user's group ID."""
    return os.getgid()

def get_group_name():
    """Returns the user's group name."""
    return grp.getgrgid(os.getgid()).gr_name

def get_label(with_name=True):
    """Returns the label used for all managed objects."""
    return (f"{LABEL_NAME}=" if with_name else "") + config.get("core.label")

def get_user_id():
    """Returns the user's ID."""
    return os.getuid()

def get_user_name():
    """Returns the user's name."""
    return pwd.getpwuid(os.getuid()).pw_name

def is_managed(object: Union[Image, Container]):
    return (
        hasattr(object, "labels")
        and LABEL_NAME in object.labels
        and object.labels[LABEL_NAME] == config.get("core.label")
    )
