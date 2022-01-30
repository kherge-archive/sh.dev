#!/bin/sh
################################################################################
# Containerized Development Environment Manager                                #
#                                                                              #
# This POSIX-compliant shell script uses the Docker CLI to create and manage   #
# an individual containerized environment, including a volume that is used to  #
# persist a home directory across container rebuilds.                          #
################################################################################

# Exit if a command fails.
set -e

# Command line client.
CLIENT=docker
#CLIENT=podman

# The name of the container.
CONTAINER=dev

# The name of the container host.
HOSTNAME=dev

# The container image tag.
IMAGE="kherge/dev:latest"

# The shell executable.
SHELL=bash

# The username.
USERNAME=dev

# The name of the volume.
VOLUME=dev

# Utilities ####################################################################

###
# Prints the given arguments if DEBUG is set to 1 (one).
#
# @param $@ The arguments to print.
##
debug()
{
    if [ "$DEBUG" = '1' ]; then
        echo "$@" >&2
    fi
}

# Management ###################################################################

###
# Creates the new container.
##
container_create()
{
    "$CLIENT" container create \
        --hostname="$HOSTNAME" \
        --init \
        --name="$CONTAINER" \
        --volume="$VOLUME:/home/dev" \
        "$IMAGE" > /dev/null
}

###
# Checks if the container exists.
#
# @return 0|1 If it exists, 0 (zero) is returned. Otherwise, 1 (one) is returned.
##
container_exists()
{
    if "$CLIENT" container inspect "$CONTAINER" > /dev/null 2> /dev/null; then
        return 0
    fi

    return 1
}

###
# Checks if the container is running.
#
# @return 0|1 If it is running, 0 (zero) is returned. Otherwise, 1 (one) is returned.
##
container_is_running()
{
    STATUS="$(container_status)"

    if [ "$STATUS" = 'running' ]; then
        return 0
    fi

    return 1
}

###
# Removes the existing container.
##
container_remove()
{
    "$CLIENT" container rm "$CONTAINER" > /dev/null
}

###
# Executes a shell inside the running container.
##
container_shell()
{
    "$CLIENT" container exec \
        --interactive \
        --tty \
        --user="$USERNAME" \
        --workdir="/home/$USERNAME" \
        "$CONTAINER" "$SHELL"
}

###
# Starts the stopped or exited container.
##
container_start()
{
    "$CLIENT" container start "$CONTAINER" > /dev/null
}

###
# Prints the status of the container.
#
# @stdout The status of the container.
##
container_status()
{
    local FIELD

    case "$CLIENT" in
        docker) FIELD=".State";;
        podman) FIELD=".Status";;
        *)
            echo "$CLIENT: client not supported" >&2
            return 1
    esac

    STATUS="$("$CLIENT" ps --all --filter "name=$CONTAINER" --format "{{$FIELD}}")"

    debug "Container status: $STATUS"

    echo "$STATUS"
}

###
# Stops the running container.
##
container_stop()
{
    "$CLIENT" container stop "$CONTAINER" > /dev/null
}

###
# Creates the new volume.
##
volume_create()
{
    "$CLIENT" volume create "$VOLUME" > /dev/null
}

###
# Checks if the volume exists.
#
# @return 0|1 If it exists, 0 (zero) is returned. Otherwise, 1 (one) is returned.
##
volume_exists()
{
    if "$CLIENT" volume inspect "$VOLUME" > /dev/null 2> /dev/null; then
        return 0
    fi

    return 1
}

###
# Removes the existing volume.
##
volume_remove()
{
    "$CLIENT" volume rm "$VOLUME" > /dev/null
}

# Commands #####################################################################

###
# Routes the container command to a subcommand.
#
# @param $@ The command line arguments.
##
cmd_container()
{
    COMMAND="$1"

    if [ "$COMMAND" = '' ]; then
        COMMAND='help 0'
    else
        shift

        if ! type "cmd_container_$COMMAND" > /dev/null; then
            COMMAND='help 3'
        fi
    fi

    cmd_container_$COMMAND "$@"
}

###
# Creates the container if it does not already exist.
##
cmd_container_create()
{
    if ! container_exists; then
        debug "Container does not existing, creating..."

        container_create
    fi
}

###
# Displays a help message for managing the container.
##
cmd_container_help()
{
    CODE=$1

    cat - >&2 <<USAGE
Usage: $(basename "$0") container COMMAND
Manages the container for the environment.

COMMAND

    create  Creates the container.
    help    Displays this help message.
    remove  Removes the container.
    shell   Runs a shell in the container.
    start   Starts the container.
    stop    Stops the container.
USAGE

    exit $CODE
}

###
# Removes the container if it still exists.
##
cmd_container_remove()
{
    if container_exists; then
        debug "Container exists, removing..."

        container_remove
    fi
}

###
# Executes a shell inside the container.
#
# - If the volume does not exist, it is created.
# - If the container does not exist, it is created.
##
cmd_container_shell()
{
    cmd_volume_create
    cmd_container_start

    container_shell
}

###
# Starts the container if it is not already running.
##
cmd_container_start()
{
    cmd_container_create

    if ! container_is_running; then
        debug "Container is not running, starting..."

        container_start
    fi
}

###
# Stops the container if it is running.
##
cmd_container_stop()
{
    if container_exists && container_is_running; then
        debug "Container is running, stopping..."

        container_stop
    fi
}

###
# Displays a help message for managing the utility.
##
cmd_help()
{
    CODE=$1

    cat - >&2 <<USAGE
Usage: $(basename "$0") COMMAND
Manages a containerized development environment.

COMMAND

    container  Manages the container.
    help       Displays this help message.
    volume     Manages the volume.
USAGE

    exit $CODE
}

###
# Routes the volume command to a subcommand.
#
# @param $@ The command line arguments.
##
cmd_volume()
{
    COMMAND="$1"

    if [ "$COMMAND" = '' ]; then
        COMMAND='help 0'
    else
        shift

        if ! type "cmd_volume_$COMMAND" > /dev/null; then
            COMMAND='help 3'
        fi
    fi

    cmd_volume_$COMMAND "$@"
}

###
# Creates the volume if it does not exist.
##
cmd_volume_create()
{
    if ! volume_exists; then
        debug "Volume does not existing, creating..."

        volume_create
    fi
}

###
# Displays a help message for managing the volume.
##
cmd_volume_help()
{
    CODE=$1

    cat - >&2 <<USAGE
Usage: $(basename "$0") volume COMMAND
Manages the volume for the environment.

COMMAND

    create  Creates the volume.
    help    Displays this help message.
    remove  Removes the volume.
USAGE

    exit $CODE
}

###
# Removes the volume if it still exists.
##
cmd_volume_remove()
{
    if volume_exists; then
        debug "Volume exists, removing..."

        volume_remove
    fi
}

# CLI ##########################################################################

# Get the command specified.
COMMAND="$1"

# Default to running "./dev.sh container shell".
if [ "$COMMAND" = '' ]; then
    COMMAND=container_shell
else
    shift

    # Default to running "./dev.sh help" with error exit status.
    if ! type "cmd_$COMMAND" > /dev/null; then
        COMMAND='help 3'
    fi
fi

# Run the command.
cmd_$COMMAND "$@"
