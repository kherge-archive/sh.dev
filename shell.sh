#!sh
################################################################################
# Containerized Shell Manager                                                  #
#
# This script will create a new image, create a new container, and then attach #
# a terminal to the running container. If the image already exists, an image   #
# is not created. If a container already exists, a new container will not be   #
# created.                                                                     #
#                                                                              #
# - Images are versioned by MD5 hash.                                          #
# - Exited containers will be restarted.                                       #
################################################################################

# The name of the container.
CONTAINER=dev

# The path to this directory.
HERE="$(dirname "$(readlink "$0")")"

# The name of the image.
IMAGE=dev

# The current version of the image.
VERSION=$(md5 -q "$HERE/Dockerfile")

###
# Destrosy the image and associated containers.
##
function cmd_destroy
{
    debug "Processing destroy command..."

    if image_exists; then
        read -p "Are you read to lose your development environment? [y/N] "

        if [ "$REPLY" = "y" ]; then
            read -p "Are you sure? [y/N] "

            if [ "$REPLY" = "y" ]; then
                image_delete
            fi
        fi
    else
        debug "The image does not exist."
    fi
}

###
# Shells into the container.
##
function cmd_shell
{
    debug "Processing shell command..."

    cmd_start

    docker exec --interactive --tty --user dev --workdir /home/dev "$CONTAINER" bash
}

###
# Starts the container.
##
function cmd_start
{
    debug "Processing start command..."

    if ! image_exists; then
        image_create
    fi

    if ! container_exists; then
        container_create
    fi

    if ! container_running; then
        container_start
    fi
}

###
# Prints the status of the container.
##
function cmd_status
{
    local STATUS="$(container_status)"
    
    case "$STATUS" in
        running) echo "Running" ;;
        exited) echo "Stopped" ;;
        *) echo "Unknown: $STATUS" ;;
    esac
}

###
# Stops the container.
##
function cmd_stop
{
    if container_running; then
        container_stop
    fi
}

###
# Creates a new container.
##
function container_create
{
    must docker container create "--name=$CONTAINER" "$IMAGE:$VERSION" > /dev/null
}

###
# Checks if the container exists.
##
function container_exists
{
    if [ "$(container_status)" = "" ]; then
        debug "The container does not exist."

        return 1
    fi

    debug "The container exists."

    return 0
}

###
# Checks if the container is running.
##
function container_running
{
    if [ "$(container_status)" = "running" ]; then
        debug "The container is running..."

        return 0
    fi

    debug "The container is not running..."

    return 1
}

###
# Starts the existing container.
##
function container_start
{
    debug "Starting the container..."

    must docker start "$CONTAINER" > /dev/null
}

###
# Retrieves the status of the container.
##
function container_status
{
    must docker ps --all --filter "name=$CONTAINER" --format "{{.State}}"
}

###
# Stops the running container.
##
function container_stop
{
    debug "Stopping the container..."

    must docker container stop "$CONTAINER" > /dev/null
}

###
# Prints the message if debugging is enabled.
##
function debug
{
    if [ "$DEBUG" = "1" ]; then
        echo "$@"
    fi
}

###
# Creates a new image for the environment.
##
function image_create
{
    debug "Creating the image..."

    must docker build --tag "$IMAGE:$VERSION" "$HERE"
}

###
# Deletes an existing image.
##
function image_delete
{
    debug "Deleting the image..."

    must docker rmi -f "$IMAGE:$VERSION"
}

###
# Checks if the image exists.
##
function image_exists
{
    docker image inspect "$IMAGE:$VERSION" &> /dev/null

    return $?
}

###
# Requires that a command successfully execute.
##
function must
{
    "$@"

    local STATUS=$?

    if [ $STATUS != 0 ]; then
        exit $STATUS
    fi
}

# Runs the requested command.
case "$1" in
    ""|shell) cmd_shell ;;
    destroy) cmd_destroy ;;
    start) cmd_start ;;
    status) cmd_status ;;
    stop) cmd_stop ;;
esac
