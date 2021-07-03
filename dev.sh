#!/bin/sh
################################################################################
# Containerized Development Environment Manager                                #
################################################################################

# The path to the configuration folder.
CONFIG="$XDG_CONFIG_HOME"

if [ "$CONFIG" = '' ]; then
    CONFIG="$HOME/.config"
fi

CONFIG="$CONFIG/dev"

if [ ! -d "$CONFIG" ]; then
    if ! mkdir -p "$CONFIG"; then
        exit 1
    fi
fi

# The name of the container.
CONTAINER=dev

# The path to the data folder.
DATA="$XDG_DATA_HOME"

if [ "$DATA" = '' ]; then
    DATA="$HOME/.local/share"
fi

DATA="$DATA/dev"

if [ ! -d "$DATA" ]; then
    if ! mkdir -p "$DATA"; then
        exit 1
    fi
fi

# The name of this script.
EXE="$(basename "$0")"

# The name of the image.
IMAGE=dev

# The path to the preferred shell in the container.
PREFERRED_SHELL=/bin/bash

################################################################################
# Dockerfile                                                                   #
################################################################################

# The current user's group ID.
GROUP_ID=$(id -g)

# The current user's group name.
GROUP_NAME="$(grep -F ":$(id -g):" < /etc/group | cut -d: -f1)"

# The current user's container password.
PASSWORD=dev

# The current user's ID.
USER_ID=$(id -u)

# The current user's name.
USER_NAME="$USER"

# The setup service.
SERVICE="
[Unit]
Description=Sets up the new Docker volume.

[Service]
ExecStart=/etc/systemd/user/user-setup.sh
Type=oneshot

[Install]
WantedBy=multi-user.target
"

# The setup script.
SCRIPT="#!/bin/bash
set -e

if [ -f \"/home/$USER_NAME/.config/dev/done\" ]; then
    exit 0
fi

TARGET=\"/home/$USER_NAME\"

# Rebuild skeleton.
shopt -s dotglob
cp /etc/skel/* \"\$TARGET\"
shopt -u dotglob

# Install sh.env.
git clone https://github.com/kherge/sh.env.git \"\$TARGET/.local/share/sh.env\"
echo >> \"\$TARGET/.bashrc\"
echo '# loading sh.env' >> \"\$TARGET/.bashrc\"
echo 'ENV_DIR=\"\$HOME/.local/share/sh.env\"' >> \"\$TARGET/.bashrc\"
echo '. \"\$ENV_DIR/env.sh\"' >> \"\$TARGET/.bashrc\"

# Fix ownership.
chown -R \"$USER_ID:$GROUP_ID\" \"\$TARGET\"
"

# The Dockerfile for the container.
DOCKERFILE="
FROM ubuntu:21.04

# Disable interactivity during build.
ARG DEBIAN_FRONTEND=noninteractive

# Update base installation.
RUN apt-get update && \\
    apt-get dist-upgrade -y && \\
    apt-get autoclean && \\
    apt-get autoremove

# Unminimize.
RUN yes | unminimize && \\
    apt-get install -y locales man systemctl && \\
    locale-gen en_US.UTF-8

# Install tools.
RUN apt-get install -y \\
    build-essential libssl-dev pkg-config \\
    curl git gnupg2 sudo unzip vim zip \\
    htop

# Create a matching group, if necessary.
RUN /bin/bash -c '[ \"\$(grep -F :20: < /etc/group)\" != \"\" ] || \\
    addgroup --gid $GROUP_ID \"$GROUP_NAME\"'

# Create a user with a matching UID & GID.
RUN adduser --uid $USER_ID --gid $GROUP_ID \"$USER_NAME\" && \\
    usermod --append --groups sudo \"$USER_NAME\" && \\
    (echo \"$USER_NAME:$PASSWORD\" | chpasswd)

# Install startup script. This allows us to make changes to the attached volume
# instead of the directory the volume replaces. Wish we could mount volumes in
# builds.
RUN echo '$SCRIPT' > /etc/systemd/user/user-setup.sh && \\
    echo '$SERVICE' > /etc/systemd/user/user-setup.service && \\
    chmod 755 /etc/systemd/user/user-setup.sh && \\
    chmod 644 /etc/systemd/user/user-setup.service && \\
    systemctl daemon-reload && \\
    systemctl enable user-setup.service

# Change to the dev user.
   USER $USER_NAME
WORKDIR /home/$USER_NAME

# Run forever.
CMD [\"sleep\", \"infinity\"]
"

# The versino of the Dockerfile above.
VERSION='1.2'

################################################################################
# Utilities                                                                    #
################################################################################

###
# Retrieves the value of a configuration setting.
#
# @param  $1 The name of the setting.
# @stderr    If the setting could not be read.
# @stdout    The value of the setting.
# @return    `0` if there is a value, or `1` if not.
##
config_get()
{
    FILE="$CONFIG/$1"

    if [ -f "$FILE" ]; then
        if ! cat "$FILE"; then
            echo "$FILE: could not be read" >&2
            exit 1
        fi

        return 0
    fi

    return 1
}

###
# Sets the value of a configuration setting.
#
# @param  $1 The name of the setting.
# @param  $2 The value of the setting.
# @stderr    If the setting could not be written.
##
config_set()
{
    FILE="$CONFIG/$1"
    VALUE="$2"

    if ! echo "$VALUE" > "$FILE"; then
        echo "$FILE: could not be written" >&2
        exit 1
    fi
}

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
        --user "$USER_NAME" \
        --workdir "/home/$USER_NAME" \
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
        "--volume=$DATA:/home/$USER_NAME" \
        "$IMAGE:$VERSION" > /dev/null
}

###
# Destroys the container if it exists.
##
container_destroy()
{
    debug "Destroying the container, $CONTAINER..."

    must docker container rm "$CONTAINER"
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

    echo "$DOCKERFILE" | must docker build --tag "$IMAGE:$VERSION" -

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

    must docker image rm "$IMAGE:$VERSION"
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
# Destroys the volume if it exists.
##
volume_destroy()
{
    debug "Destroying the volume, $DATA..."

    if [ -d "$DATA" ]; then
        must rm -Rf "$DATA"
    fi
}

###
# Checks if the volume exists.
#
# @return Returns 0 (zero) if it exists, or 1 (one) if not.
##
volume_exists()
{
    debug "Checking if the image, $IMAGE:$VERSION, exists..."

    if [ -d "$DATA" ]; then
        return 0
    fi

    return 1
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
    echo "  help   Displays this help message."
    echo "  shell  Starts the container and attaches a shell."
    echo "  start  Starts the container."
    echo "  stop   Stops the container."
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
    shell) do_shell;;
    start) do_start;;
    stop) do_stop;;
    *)
        echo "$EXE: $1: invalid command" >&2
        exit 1
esac
