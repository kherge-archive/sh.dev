#!/bin/bash
set -e

# Find the home directory.
HOME="/home/$(ls -1 /home | head -1)"

# Do not nuke existing setups.
if [ -f "$HOME/.bashrc" ]; then
    exit 0
fi

# Copy skeleton.
shopt -s dotglob
cp -dRp /etc/skel/* "$HOME/"
shopt -u dotglob

# Install sh.env.
git clone https://github.com/kherge/sh.env.git "$HOME/.local/opt/sh.env"

echo >> "$HOME/.bashrc"
echo 'ENV_DIR="$HOME/.local/opt/sh.env"' >> "$HOME/.bashrc"
echo '. "$ENV_DIR/env.sh"' >> "$HOME/.bashrc"

# Fix ownership
chown -R "$(stat -C %u "$HOME"):$(stat -C %g "$HOME")" "$HOME"
