import argparse
import docker
import logging
import os
import sys

class Manager:
    """Manages the volume shared by the development containers."""

    def __init__(self,
        client: docker.DockerClient,
        logger: logging.Logger = logging.getLogger("dev.volume.Manager"),
        name: str = "dev"
    ):
        """Initializes the new volume manager.

        ```
        @param client  "The Docker client."
        @param logger  "The logger."
        @param name    "The name of the volume."
        ```
        """
        self._client = client
        self._logger = logger
        self._name = name

    def create(self):
        """Creates the volume."""
        self._logger.debug("creating the volume...")

        self._client.volumes.create(self._name)

    def destroy(self):
        """Deletes the volume."""
        self._logger.debug("deleting the volume...")

        self._find().remove()

    def exists(self):
        self._logger.debug("checking if volume exists...")

        try:
            self._find()
            self._logger.debug("volume exists")

            return True
        except docker.errors.NotFound:
            self._logger.debug("volume does not exist")

            return False

    def _find(self):
        """Finds the volume and returns it."""
        self._logger.debug("retrieving the volume...")

        return self._client.volumes.get(self._name)

class Command:
    """Processes command line arguments for managing the shared volume."""

    _manager: Manager

    def __init__(
        self,
        manager: Manager,
        logger: logging.Logger = logging.getLogger("dev.volume.Command")
    ):
        self._logger = logger,
        self._manager = manager

    def add(self, subparser: argparse.ArgumentParser):
        """Adds a subparser to the argument parser."""

        parser = subparser.add_parser("volume", add_help=False)
        parser.set_defaults(func=self.help)
        parser.add_argument(
            "-h",
            "--help",
            action="store_true",
            dest="help"
        )

        nested = parser.add_subparsers()

        def sub(name, func):
            """Creates a subcommand."""

            command = nested.add_parser(name, add_help=False)
            command.add_argument("-h", "--help", action="store_true", dest="help")
            command.set_defaults(func=func)

        sub("create", self.create)
        sub("destroy", self.destroy)
        sub("status", self.status)

    def create(self, args: argparse.Namespace):
        if not self._manager.exists():
            self._manager.create()
        else:
            self._logger.info("volume already exists")

    def destroy(self, args: argparse.Namespace):
        if self._manager.exists():
            self._manager.destroy()
        else:
            self._logger.info("volume does not exist")

    def help(self, args: argparse.Namespace):
        print(f"""Usage: {os.path.basename(sys.argv[0])} volume [OPTIONS] COMMAND
Manages the volume.

OPTIONS

    -h, --help  Displays this help message.

COMMAND

    create   Creates the volume, if it does not exist.
    destroy  Destroys the volume, if it exists.
    status   Prints the status of the volume.
""")

    def status(self, args: argparse.Namespace):
        if self._manager.exists():
            print("The volume exists.")
        else:
            print("The volume does not exist.")

def register(client: docker.DockerClient, subparser: argparse.ArgumentParser):
    Command(Manager(client)).add(subparser)
