FROM ubuntu:21.04

# Disable interactivity during build.
ARG DEBIAN_FRONTEND=noninteractive
ARG GROUP_ID
ARG GROUP_NAME
ARG PASSWORD
ARG USER_ID
ARG USER_NAME

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
RUN /bin/bash -c '[ "$(grep -F :20: < /etc/group)" != "" ] || \\
    addgroup --gid $GROUP_ID "$GROUP_NAME"'

# Create a user with a matching UID & GID.
RUN adduser --uid $USER_ID --gid $GROUP_ID "$USER_NAME" && \\
    usermod --append --groups sudo "$USER_NAME" && \\
    (echo "$USER_NAME:$PASSWORD" | chpasswd)

# Install user setup service.
COPY setup-user.service /etc/systemd/system/setup-user.service
COPY setup-user.sh /etc/systemd/system/setup-user.sh

RUN chmod 644 /etc/systemd/system/setup-user.service && \
    chmod 755 /etc/systemd/system/setup-user.sh && \
    systemctl daemon-reload && \
    systemctl enable setup-user.service

# Change to the dev user.
   USER $USER_NAME
WORKDIR /home/$USER_NAME

# Run forever.
CMD ["sleep", "infinity"]