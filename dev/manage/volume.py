from .utils import LABEL_NAME, get_label
from typing import Optional

import docker
import logging

logger = logging.getLogger(__name__)

class VolumeError(Exception):
    """An error for volume related issues."""

    # The error message.
    message: str

    # The name of the volume setting.
    name: Optional[str]

    # The previous error.
    previous: BaseException

    def __init__(
        self,
        name: str,
        message: str,
        previous: Optional[BaseException] = None
    ):
        self.message = message
        self.name = name
        self.previous = previous

def create(name: str, client: Optional[docker.DockerClient] = None):
    """Creates a volume with the appropriate label."""
    logger.debug(f"creating {name}")

    client = docker.from_env() if client is None else client

    labels = dict()
    labels[LABEL_NAME] = get_label(with_name=False)

    try:
        client.volumes.create(name=name, labels=labels)
    except BaseException as previous:
        raise VolumeError(name, "could not create volume", previous)

def exists(name: str, client: Optional[docker.DockerClient] = None):
    """Checks if a volume with the given name and appropriate label exists."""
    logger.debug(f"checking if {name} exists")

    client = docker.from_env() if client is None else client

    try:
        volume = client.volumes.get(name)

        if (
            volume.attrs["Labels"]
            and LABEL_NAME in volume.attrs["Labels"]
            and volume.attrs["Labels"][LABEL_NAME] == get_label(with_name=False)
        ):
           return True
        else:
            logger.info(f"{name} exists but is not labeled with {get_label()}")
    except docker.errors.NotFound:
        pass
    except BaseException as previous:
        raise VolumeError(name, "could not remove volume", previous)

    return False

def listing(client: Optional[docker.DockerClient] = None):
    """Lists the name of all volumes with the appropriate label."""
    logger.debug(f"listing any labeled with {get_label(with_name=False)}")

    client = docker.from_env() if client is None else client

    try:
        return list(map(
            lambda volume: volume.name,
            client.volumes.list(filters={"label": get_label()})
        ))
    except BaseException as previous:
        raise VolumeError(None, "could not list volumes", previous)

def remove(name: str, client: Optional[docker.DockerClient] = None):
    """Removes a volume with the given name and appropriate label."""
    logger.debug(f"removing {name}")

    client = docker.from_env() if client is None else client

    try:
        volume = client.volumes.get(name)

        if (
            volume.attrs["Labels"]
            and LABEL_NAME in volume.attrs["Labels"]
            and volume.attrs["Labels"][LABEL_NAME] == get_label(with_name=False)
        ):
           volume.remove()
        else:
            logger.info(f"{name} exists but is not labeled with {get_label()}")
    except docker.errors.NotFound:
        pass
    except BaseException as previous:
        raise VolumeError(name, "could not remove volume", previous)
