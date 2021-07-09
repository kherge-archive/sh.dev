#!/bin/sh

# Re-number the conflicting group.
CONFLICT="$(grep :$GROUP_ID: /etc/group | cut -d: -f1)"

if [ "$CONFLICT" != '' ]; then
    echo "Renumbering $CONFLICT..."

    groupmod --gid 999 "$CONFLICT"
fi

# Re-number existing group.
if grep -F "$GROUP_NAME:" /etc/group; then
    echo "Renumbering $GROUP_NAME to $GROUP_ID..."

    groupmod --gid $GROUP_ID "$GROUP_NAME"

# Create missing group.
else
    echo "Creating $GROUP_NAME..."

    addgroup --gid $GROUP_ID "$GROUP_NAME"
fi
