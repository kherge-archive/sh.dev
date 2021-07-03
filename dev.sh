#!/bin/sh
################################################################################
# Containerized Development Environment Manager                                #
################################################################################

# The name of the container.
CONTAINER=dev

# The name of this script.
EXE="$(basename "$0")"

# The path to here.
HERE="$(dirname "$(readlink "$0")")"

# The name of the image.
IMAGE=dev

# The current user's container password.
PASSWORD=dev

# The path to the preferred shell in the container.
PREFERRED_SHELL=/bin/bash

# The version of the image.
VERSION="1.3"

# The name of the volume.
VOLUME=dev

################################################################################
# Utilities                                                                    #
################################################################################

###
# Prints a message to STDERR if DEBUG=1.
#
# @param $@ The message to print.
##
debug()
{
    if [ "$DEBUG" = '1' ]; then
        echo "$@" >&2
    fi
}

###
# Requires that a command successfully execute.
#
# @param $@ The command line arguments.
# @stderr   The output of the command.
# @stdout   The output of the command.
# @exit     The same status as the command if not 0 (zero).
##
must()
{
    "$@"

    STATUS=$?

    debug "exited [$STATUS]: $*"

    if [ $STATUS -ne 0 ]; then
        debug "Command failed, exiting."

        exit $STATUS
    fi
}

################################################################################
# Container, Image, and Volume Management                                      #
################################################################################

###
# Attaches a shell to the running container.
#
# @exit The same status as Docker CLI exit status.
##
container_attach()
{
    debug "Attaching shell to container, $CONTAINER..."

    docker exec \
        --interactive \
        --tty \
        --user "$USER" \
        --workdir "/home/$USER" \
        "$CONTAINER" "$PREFERRED_SHELL"

    exit $?
}

###
# Creates the container.
##
container_create()
{
    debug "Creating the container, $CONTAINER..."

    must docker container create \
        "--name=$CONTAINER" \
        "--volume=$VOLUME:/home/$USER" \
        "$IMAGE:$VERSION" > /dev/null
}

###
# Destroys the container if it exists.
##
container_destroy()
{
    debug "Destroying the container, $CONTAINER..."

    must docker container rm "$CONTAINER" > /dev/null
}

###
# Checks if the container exists.
#
# @return Returns 0 (zero) if it exists, or 1 (one) if not.
##
container_exists()
{
    debug "Checking if the container, $CONTAINER, exists..."

    if ! STATUS="$(container_status)"; then
        exit 1
    elif [ "$STATUS" = '' ]; then
        debug "The container does not exist."

        return 1
    fi

    debug "The container exists."

    return 0
}

###
# Checks if the container is running.
#
# @return Returns 0 (zero) if it is running, or 1 (one) if not.
##
container_is_running()
{
    debug "Checking of the container, $CONTAINER, is running..."

    if ! STATUS="$(container_status)"; then
        exit 1
    elif [ "$STATUS" = 'running' ]; then
        debug "The container is running."

        return 0
    fi

    debug "The container is not running."

    return 1
}

###
# Starts the container if it is not running.
##
container_start()
{
    debug "Starting the container, $CONTAINER..."

    must docker start "$CONTAINER" > /dev/null
}

###
# Fetches the status of the container.
##
container_status()
{
    debug "Getting the status of the container, $CONTAINER..."

    must docker ps --all --filter "name=$CONTAINER" --format "{{.State}}"
}

###
# Stops the container if it is running.
##
container_stop()
{
    debug "Stopping the container, $CONTAINER..."

    must docker container stop "$CONTAINER" > /dev/null
}

###
# Creates a new image, replacing an existing version if necessary.
##
image_create()
{
    debug "Creating the image, $IMAGE:$VERSION..."

    must docker build \
        --build-arg GROUP_ID=$(id -g) \
        --build-arg GROUP_NAME="$(grep -F ":$(id -g):" < /etc/group | cut -d: -f1)" \
        --build-arg PASSWORD="$PASSWORD" \
        --build-arg USER_ID=$(id -u) \
        --build-arg USER_NAME="$USER" \
        --tag "$IMAGE:$VERSION" \
        "$HERE"

    # Because we're piping, we need to handle the subshell.
    STATUS=$?

    if [ $STATUS != 0 ]; then
        exit $STATUS
    fi
}

###
# Destroys the image (current version tag) if it exists.
##
image_destroy()
{
    debug "Destroying the image, $IMAGE:$VERSION..."

    must docker image rm "$IMAGE:$VERSION" > /dev/null
}

###
# Checks if the image exists.
#
# @return Returns 0 (zero) if it exists, or 1 (one) if not.
##
image_exists()
{
    debug "Checking if the image, $IMAGE:$VERSION, exists..."

    docker image inspect "$IMAGE:$VERSION" > /dev/null 2>&1

    return $?
}

###
# Creates the volume.
##
volume_create()
{
    debug "Creating the volume..."

    must docker volume create "$VOLUME" > /dev/null
}

###
# Destroys the volume.
##
volume_destroy()
{
    debug "Destroying the volume..."

    must docker volume rm "$VOLUME" > /dev/null
}

###
# Checks if the volume exists.
#
# @return Returns 0 (zero) if it exists, or 1 (one) if not.
##
volume_exists()
{
    debug "Checking if the volume exists..."

    docker volume inspect "$VOLUME" > /dev/null 2>&1

    return $?
}

################################################################################
# Commands                                                                     #
################################################################################

###
# Tears down the environment.
#
# @param $@ The command line arguments.
##
do_clean()
{
    # Process arguments.
    DELETE_CONTAINER=0
    DELETE_IMAGE=0
    DELETE_VOLUME=0

    shift
    while getopts :civ OPTION; do
        case "$OPTION" in
            c) DELETE_CONTAINER=1;;
            i) DELETE_IMAGE=1;;
            v) DELETE_VOLUME=1;;
            *)
                echo "$EXE: $OPTARG: invalid option" >&2
                echo >&2

                do_usage
        esac
    done

    # Make sure work is specified.
    if [ $DELETE_CONTAINER -eq 0 ] && \
       [ $DELETE_IMAGE -eq 0 ] && \
       [ $DELETE_VOLUME -eq 0 ]; then
        echo "No work to be done."

        return
    fi

    # Confirm.
    printf "The process is irreversible. Are you sure? [y/N] "
    read -r REPLY

    if [ "$REPLY" != 'y' ]; then
        return
    fi

    # Start nuking.
    if [ $DELETE_CONTAINER -eq 1 ]; then
        echo "Deleting the container..."

        if container_exists; then
            if container_is_running; then
                container_stop
            fi

            container_destroy
        fi
    fi

    if [ $DELETE_VOLUME -eq 1 ]; then
        echo "Deleting the volume..."

        if volume_exists; then
            if container_is_running; then
                echo "The container must be stopped first." >&2
                exit 1
            fi

            volume_destroy
        fi
    fi

    if [ $DELETE_IMAGE -eq 1 ]; then
        echo "Deleting the image..."

        if image_exists; then
            if container_exists; then
                echo "The container must be deleted too." >&2
                exit 1
            fi

            image_destroy
        fi
    fi
}

###
# Copies files or folders from the container.
##
do_from()
{
    shift

    if ! container_is_running; then
        echo "Container is not running." >&2
        exit 1
    fi

    docker cp "$CONTAINER:$1" "$2"

    return $?
}

###
# Displays the usage guide.
##
do_usage()
{
    echo "Usage: $EXE COMMAND [OPTIONS]"
    echo "Manages a containerized development environment."
    echo
    echo "COMMAND"
    echo
    echo "  clean  Tears down the environment."
    echo "  from   Copies files or folders from the container."
    echo "  help   Displays this help message."
    echo "  shell  Starts the container and attaches a shell."
    echo "  start  Starts the container."
    echo "  stop   Stops the container."
    echo "  to     Copies files or folders to the container."
    echo
    echo "OPTIONS"
    echo
    echo "  clean"
    echo
    echo "    -c  Deletes the container."
    echo "    -i  Deletes the image."
    echo "    -v  Deletes the volume."
    echo

    exit 3
}

###
# Starts the container and attaches a shell.
##
do_shell()
{
    SILENT=1 do_start

    container_attach
}

###
# Starts the container.
##
do_start()
{
    if ! volume_exists; then
        volume_create
    fi

    if ! image_exists; then
        image_create
    fi

    if ! container_exists; then
        container_create
    fi

    if container_is_running && [ "$SILENT" != '1' ]; then
        echo "Container is already running."
    else
        container_start
    fi
}

###
# Stops the container.
##
do_stop()
{
    if container_is_running; then
        container_stop
    else
        echo "Container is already stopped."
    fi
}

###
# Copies files or folders to the container.
##
do_to()
{
    shift

    if ! container_is_running; then
        echo "Container is not running." >&2
        exit 1
    fi

    docker cp "$1" "$CONTAINER:$2"

    return $?
}

################################################################################
# Interface                                                                    #
################################################################################

if ! command -v docker > /dev/null; then
    echo "$EXE: docker is required" >&2
    exit 1
fi

case "$1" in
    ""|help) do_usage;;
    clean) do_clean "$@";;
    from) do_from "$@";;
    shell) do_shell;;
    start) do_start;;
    stop) do_stop;;
    to) do_to "$@";;
    *)
        echo "$EXE: $1: invalid command" >&2
        exit 1
esac
