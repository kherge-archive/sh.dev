FROM ubuntu:21.04

# Disable interactivity during build.
ARG DEBIAN_FRONTEND=noninteractive
ARG GROUP_ID
ARG GROUP_NAME
ARG PASSWORD
ARG USER_ID
ARG USER_NAME

# Update base installation.
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get autoclean && \
    apt-get autoremove

# Unminimize.
RUN yes | unminimize && \
    apt-get install -y locales man systemctl && \
    locale-gen en_US.UTF-8

# Install tools.
RUN apt-get install -y \
    build-essential libssl-dev pkg-config \
    curl git gnupg2 sudo unzip vim zip \
    htop

# Fix groups.
COPY fix-groups.sh /tmp/fix-groups.sh
RUN chmod 755 /tmp/fix-groups.sh && \
    /tmp/fix-groups.sh && \
    rm /tmp/fix-groups.sh

# Create a user with a matching UID & GID.
RUN adduser --uid $USER_ID --gid $GROUP_ID "$USER_NAME" && \
    usermod --append --groups sudo "$USER_NAME" && \
    (echo "$USER_NAME:$PASSWORD" | chpasswd)

# Change to the dev user.
   USER $USER_NAME
WORKDIR /home/$USER_NAME

# Install sh.env.
RUN git clone https://github.com/kherge/sh.env.git ~/.local/opt/sh.env && \
    echo >> ~/.bashrc && \
    echo 'export ENV_DIR="$HOME/.local/opt/sh.env"' >> ~/.bashrc && \
    echo '. "$ENV_DIR/env.sh"' >> ~/.bashrc

# Run forever.
CMD ["sleep", "infinity"]
