FROM ubuntu:21.10

# Disable interactivity during build.
ARG DEBIAN_FRONTEND=noninteractive

# Update base installation.
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get autoclean && \
    apt-get autoremove

# Install tools.
RUN apt-get install -y build-essential curl git gnupg2 htop libssl-dev pkg-config sudo unzip vim zip

# Create a new user.
RUN adduser dev && \
    chown -R dev:dev /home/dev && \
    usermod --append --groups sudo dev && \
    (echo dev:dev | chpasswd)

# Change to the dev user.
   USER dev
WORKDIR /home/dev

# Install starship.
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --no-modify-path -y && \
    .cargo/bin/cargo install starship

# Install SDKMAN.
RUN curl -s "https://get.sdkman.io?rcupdate=false" | bash

# Install NVM.
RUN export NVM_DIR="$HOME/.nvm" && \
    git clone https://github.com/nvm-sh/nvm.git "$NVM_DIR" && \
    cd "$NVM_DIR" && \
    git checkout `git describe --abbrev=0 --tags --match "v[0-9]*" $(git rev-list --tags --max-count=1)`

# Install bash.utils.
RUN mkdir -p .local/opt && \
    git clone https://github.com/kherge/bash.utils.git .local/opt/bash.utils && \
    echo 'export BASH_UTILS=$HOME/.local/opt/bash.utils' >> .bashrc && \
    echo '. "$BASH_UTILS/bootstrap.sh"' >> .bashrc

# Run forever.
CMD ["sleep", "infinity"]
