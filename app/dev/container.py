from dev import utils

import argparse
import docker
import logging
import os
import sys

class Manager:
    """Manages the container used for the development environment."""

    def __init__(self,
        client: docker.DockerClient,
        logger: logging.Logger = logging.getLogger("dev.container.Manager"),
        name: str = "dev"
    ):
        """Initializes the new container manager.

        ```
        @param client "The Docker client."
        @param logger "The logger."
        @param name   "The name of the container."
        ```
        """
        self._client = client
        self._logger = logger
        self._name = name

    def create(
        self,
        image_name: str = "dev",
        image_version: str = "latest",
        user_name: str = utils.get_user_name(),
        volume: str = "dev"
    ):
        """Creates the development container using the development image."""
        self._logger.debug("creating the container...")

        self._client.containers.create(
            f"{image_name}:{image_version}",
            auto_remove=False,
            hostname=self._name,
            name=self._name,
            volumes=[f"{volume}:/home/{user_name}"]
        )

    def delete(self, force=False):
        """Deletes the development container.

        ```
        @param force "Use SIGKILL to force kill the container?"
        ```
        """
        self._logger.debug("deleting the container...")

        self._find().remove(force=force, v=False)

    def exists(self) -> bool:
        """Checks if the development container exists.

        ```
        @return "Returns true if it exists, or false if not."
        ```
        """
        self._logger.debug("checking if the container exists...")

        try:
            self._find()
            self._logger.debug("container exists")

            return True
        except docker.errors.NotFound:
            self._logger.debug("container does not exist")

            return False

    def is_running(self) -> bool:
        """Checks if the development container is running.

        ```
        @return "Returns true if it is running, or false if not."
        ```
        """
        self._logger.debug("checking if the container is running...")

        status = self.status()

        self._logger.debug(f"container is: {status}")

        return status == "running"

    def shell(
        self,
        shell: str = "/bin/bash",
        user: str = utils.get_user_name()
    ):
        """Attaches a shell to the container.

        ```
        @param user  "The container user name to login as."
        @param shell "The path to the shell inside the container."
        ```
        """
        self._logger.debug("creating a shell...")

        os.system(f"docker exec \
            --interactive \
            --tty \
            --user '{user}' \
            --workdir '/home/{user}' \
            '{self._name}' \
            '{shell}'")

    def start(self):
        """Starts the development container."""
        self._logger.debug("starting the container...")

        self._find().start()

    def status(self):
        """Retrieves the status of the container.

        ```
        @return "The status of the container."
        ```
        """
        self._logger.debug("retrieving container status...")

        return self._find().status

    def stop(self, timeout=10):
        """Stops the development container.

        ```
        @param timeout "How long to wait before sending SIGKILL."
        ```
        """
        self._logger.debug("stopping the container...")

        self._find().stop(timeout=timeout)

    @utils.memoize
    def _find(self):
        """Finds the development container and returns it.

        ```
        @return "The container."
        ```
        """
        self._logger.debug("retrieving the container...")

        return self._client.containers.get(self._name)

class Command:
    """Processes command line arguments for managing development containers."""

    _manager: Manager

    def __init__(
        self,
        manager: Manager,
        logger: logging.Logger = logging.getLogger("dev.container.Command")
    ):
        self._logger = logger
        self._manager = manager

    def add(self, subparser: argparse.ArgumentParser):
        """Adds a subparser to the argument parser."""

        parser = subparser.add_parser("container", add_help=False)
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
        sub("shell", self.shell)
        sub("start", self.start)
        sub("status", self.status)
        sub("stop", self.stop)

    def create(self, args: argparse.Namespace):
        if not self._manager.exists():
            self._manager.create()
        else:
            self._logger.info("container already exists")

    def destroy(self, args: argparse.Namespace):
        if self._manager.exists():
            self._manager.delete()
        else:
            self._logger.info("container does not exist")

    def help(self, args: argparse.Namespace):
        print(f"""Usage: {os.path.basename(sys.argv[0])} container [OPTIONS] COMMAND
Manages the container.

OPTIONS

    -h, --help  Displays this help message.

COMMAND

    create   Creates the container, if it does not exist.
    destroy  Destroys the container, if it exists.
    shell    Attaches a shell to the container, if it is running.
    start    Starts the container, if it is not running.
    status   Prints the status of the container.
    stop     Stops the container, if it is running.
""")

    def shell(self, args: argparse.Namespace):
        if self._manager.exists():
            if self._manager.is_running():
                self._manager.shell()
            else:
                self._logger.error("container is not running")
        else:
            self._logger.error("container does not exist")

    def start(self, args: argparse.Namespace):
        if self._manager.exists():
            if not self._manager.is_running():
                self._manager.start()
            else:
                self._logger.info("container is already running")
        else:
            self._logger.error("container does not exist")

    def status(self, args: argparse.Namespace):
        if self._manager.exists():
            print(self._manager.status())
        else:
            print("The container does not exist.")

    def stop(self, args: argparse.Namespace):
        if self._manager.exists():
            if self._manager.is_running():
                self._manager.stop()
            else:
                self._logger.info("container is not running")
        else:
            self._logger.error("container does not exist")

def register(client: docker.DockerClient, subparser: argparse.ArgumentParser):
    Command(Manager(client)).add(subparser)
