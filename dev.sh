#!/bin/sh
################################################################################
# Containerized Development Environment Manager                                #
#                                                                              #
# This POSIX-compliant shell script uses the Docker CLI to create, manage, and #
# remove volumes, images, and containers that are used to run containerized    #
# development environments.                                                    #
################################################################################

# The name of the container.
CONTAINER=dev

# The name of the image.
IMAGE=kherge/dev:latest

# The name of the volume.
VOLUME=dev

# Utilities ####################################################################

###
# Requires that a command successfully execute.
#
# @param $@ The command line arguments.
#
# @stderr   The output of the command.
# @stdout   The output of the command.
#
# @exit     The same status as the command if not 0 (zero).
##
must()
{
    "$@"

    STATUS=$?

    if [ $STATUS -ne 0 ]; then
        exit $STATUS
    fi
}

# Management ###################################################################

###
# Attaches a shell to a running container.
##
container_attach()
{
    docker exec \
        --interactive \
        --tty \
        --user dev \
        --workdir /home/dev \
        "$CONTAINER" bash

    exit $?
}

###
# Creates a container, if one does not already exist.
#
# @must
##
container_create()
{
    if ! volume_exists; then
        volume_create
    fi

    must docker container create \
        "--name=$CONTAINER" \
        "--volume=$VOLUME:/home/$USER" \
        "$IMAGE" > /dev/null
}

###
# Checks if a container exists.
#
# @return Returns `0` if it exists, or `1` if not.
##
container_exists()
{
    if ! STATUS="$(container_status)"; then
        exit 1
    elif [ "$STATUS" = '' ]; then
        return 1
    fi

    return 0
}

###
# Checks if a container is running.
#
# @return Returns `0` if running, or `1` if not.
#
# @exit   Exits with `1` if `container_status` failed.
##
container_is_running()
{
    if ! STATUS="$(container_status)"; then
        exit 1
    elif [ "$STATUS" = 'running' ]; then
        return 0
    fi

    return 1
}

###
# Starts a container.
##
container_start()
{
    must docker start "$CONTAINER" > /dev/null
}

###
# Prints the status of the container.
#
# @stdout The container status.
#
# @must
##
container_status()
{
    must docker ps --all --filter "name=$CONTAINER" --format '{{.State}}'
}

###
# Stops a container.
##
container_stop()
{
    must docker container stop "$CONTAINER" > /dev/null
}

###
# Creates a volume.
##
volume_create()
{
    debug "Creating the volume..."

    must docker volume create "$VOLUME" > /dev/null
}

###
# Checks if a volume exists.
#
# @return Returns `0` if it exists, or `1` if not.
##
volume_exists()
{
    debug "Checking if the volume exists..."

    docker volume inspect "$VOLUME" > /dev/null 2>&1

    return $?
}

# CLI ##########################################################################

if [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
    cat - >&2 <<HELP
Usage: $(basename "$0") [OPTIONS]
Manages a containerized development environment.

This script will perform a series of steps:

- Check if the container is not running.
    - If the volume does not exist, create it.
    - If the container does not exist, create it.
    - Start the container.
- Attach a shell to the container.

The final step is always, unconditionally performed.

OPTIONS

    -h, --help  Displays this help message.
HELP

    exit 0
fi

if ! container_is_running; then
    if ! volume_exists; then
        volume_create
    fi

    if ! container_exists; then
        container_create
    fi

    container_start
fi

container_attach
