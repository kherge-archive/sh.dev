from .utils import LABEL_NAME, get_label
from typing import Optional

import docker
import logging

logger = logging.getLogger(__name__)

def create(name: str, client: Optional[docker.DockerClient] = None):
    """Creates a volume with the appropriate label."""
    logger.debug(f"creating {name}")

    client = docker.from_env() if client is None else client

    labels = dict()
    labels[LABEL_NAME] = get_label(with_name=False)

    client.volumes.create(name=name, labels=labels)

def listing(client: Optional[docker.DockerClient] = None):
    """Lists the name of all volumes with the appropriate label."""
    logger.debug(f"listing any labeled with {get_label(with_name=False)}")

    client = docker.from_env() if client is None else client

    return list(map(
        lambda volume: volume.name,
        client.volumes.list(filters={"label": get_label()})
    ))

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
        logger.info(f"{name} does not exist")
