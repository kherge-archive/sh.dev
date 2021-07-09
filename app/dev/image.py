from typing import Generator
from dev import utils

import argparse
import docker
import json
import logging
import os
import sys

class Manager:
    """Manages the development image used to create new containers."""

    def __init__(self,
        client: docker.DockerClient,
        logger: logging.Logger = logging.getLogger("dev.image.Manager"),
        name: str = "dev",
        version: str = "latest"
    ):
        """Initializes the new image manager.

        ```
        @param client  "The Docker client."
        @param logger  "The logger."
        @param name    "The name of the image."
        @param version "The version of the image."
        ```
        """
        self._client = client
        self._logger = logger
        self._name = name
        self._version = version

    def create(
        self,
        groupId: str = utils.get_group_id(),
        groupName: str = utils.get_group_name(),
        password: str = "dev",
        userId: str = utils.get_user_id(),
        userName: str = utils.get_user_name()
    ):
        """Creates a new development image.

        ```
        @param groupId   "The ID of the user group."
        @param groupName "The name of the user group."
        @param password  "The password for the user."
        @param userId    "The ID of the user."
        @param userName  "The name of the user."
        ```
        """
        self._logger.debug("creating the image...")

        self._stream_status(
            self._client.api.build(
                buildargs={
                    "GROUP_ID": str(groupId),
                    "GROUP_NAME": groupName,
                    "PASSWORD": password,
                    "USER_ID": str(userId),
                    "USER_NAME": userName
                },
                path=self._find_path(),
                rm=True,
                tag=f"{self._name}:{self._version}"
            ),
            echo=self._logger.isEnabledFor(logging.INFO)
        )

    def destroy(self, prune: bool = False):
        """Deletes the development image."""
        self._logger.debug("deleting the image...")

        self._client.images.remove(self._name, noprune=not prune)

    def exists(self):
        """Checks if the development image exists."""
        self._logger.debug("checking if image exists...")

        try:
            self._find()
            self._logger.debug("image exists")

            return True
        except docker.errors.ImageNotFound:
            self._logger.debug("image does not exist")

            return False

    @utils.memoize
    def _find(self):
        """Find the development image and returns it."""
        self._logger.debug("retrieving the image...")

        return self._client.images.get(self._name)

    @utils.memoize
    def _find_path(self):
        """Finds the path to the development image Dockerfile directory."""
        self._logger.debug("finding Dockerfile directory path...")

        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "..",
            "image"
        )

    def _stream_status(self, stream: Generator, echo: bool = False):
        for output in stream:
            output = output.decode("utf-8")

            if echo:
                for line in output.split("\r\n"):
                    if line.strip() != "":
                        line = json.loads(line)

                        if "stream" in line:
                            sys.stderr.write(line["stream"])
                        else:
                            print(line, file=sys.stderr, flush=True)

class Command:
    """Processes command line arguments for managing development images."""

    _manager: Manager

    def __init__(
        self,
        manager: Manager,
        logger: logging.Logger = logging.getLogger("dev.image.Command")
    ):
        self._logger = logger
        self._manager = manager

    def add(self, subparser: argparse.ArgumentParser):
        """Adds a subparser to the argument parser."""

        parser = subparser.add_parser("image", add_help=False)
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
            self._logger.info("image already exists")

    def destroy(self, args: argparse.Namespace):
        if self._manager.exists():
            self._manager.destroy()
        else:
            self._logger.info("image does not exist")

    def help(self, args: argparse.Namespace):
        print(f"""Usage: {os.path.basename(sys.argv[0])} image [OPTIONS] COMMAND
Manages the image.

OPTIONS

    -h, --help  Displays this help message.

COMMAND

    create   Creates the image, if it does not exist.
    destroy  Destroys the image, if it exists.
    status   Prints the status of the image.
""")

    def status(self, args: argparse.Namespace):
        if self._manager.exists():
            print("The image exists.")
        else:
            print("The image does not exist.")

def register(client: docker.DockerClient, subparser: argparse.ArgumentParser):
    Command(Manager(client)).add(subparser)
