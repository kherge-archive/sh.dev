#!/usr/bin/env python3
import argparse
import dev
import docker
import logging
import os
import sys

# Get the Docker client.
client = docker.from_env()

# Create the managers.
container = dev.container.Manager(client)
image = dev.image.Manager(client)
volume = dev.volume.Manager(client)

# Configure the logger.
logging.basicConfig(format="dev: %(message)s", level=logging.ERROR)

logger = logging.getLogger("dev")
logger.setLevel(logging.WARN)

# Configure the CLI arguments parser.
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument(
    "-h",
    "--help",
    action="store_true",
    dest="help"
)

parser.add_argument(
    "-V",
    "--version",
    action="version",
    dest="version",
    version="2.0.0"
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    dest="verbose"
)

# Configure the parser for subcommands.
subparser = parser.add_subparsers()

dev.container.Command(container).add(subparser)
dev.image.Command(image).add(subparser)
dev.volume.Command(volume).add(subparser)

# Parse the parguments.
args = parser.parse_args()

# Adjust the logging level if necessary.
if args.verbose >= 2:
    logger.setLevel(logging.DEBUG)
elif args.verbose == 1:
    logger.setLevel(logging.INFO)

# Display the help message.
if args.help and not hasattr(args, "func"):
    print(f"""Usage: {os.path.basename(sys.argv[0])} [OPTIONS] [COMMAND]
Manages the containerized development environment.

If the command is run without any arguments:

    - The volume is created.
    - The image is created.
    - The container is created.
    - The container is started.
    - Attach a shell to the running container.

If any of these already exist or started, a shell is simply attached.

OPTIONS

    -h,    --help     Displays this help message.
    -v[v], --verbose  Increases verbosity of commands.
    -V,    --version  Displays the version of this tool.

COMMAND

    container  Manage the container.
    image      Manage the image.
    volume     Manage the volume.
""")

    sys.exit(0)

# Invoke the command.
if hasattr(args, "func"):
    args.func(args)

# Setup and attach.
else:
    if not volume.exists():
        volume.create()

    if not image.exists():
        image.create()

    if not container.exists():
        container.create()

    if not container.is_running():
        container.start()

    container.shell()
