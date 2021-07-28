sh.dev
======

Manages access to a persistent, containerized development environment.

```sh
user@host:~$ dev
dev@dev:~$ echo 'Hello from inside the container!'
```

> It is recommended that you use the container managed by this script with [Visual Studio Code's Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers), or your IDE's equivalent option.

Features
--------

- Uses Docker to manage containers.
    - Built on the [kherge/dev](https://github.com/kherge/docker.dev) image.
    - Volume is used on the home directory so that its data can persist across container recreations, allowing for iterative changes to a container's Dockerfile. (Just remember to install everything locally!)

Requirements
------------

- Docker
- POSIX-compliant Shell

Installation
------------

1. Clone this repository to: `$HOME/.local/opt/sh.dev`
2. Create a symbolic link from `$HOME/.local/opt/sh.dev/dev.sh` to: `$HOME/.local/bin/dev`

```sh
git clone https://github.com/kherge/sh.dev.git ~/.local/opt/sh.dev
ln -s ~/.local/opt/sh.dev/dev.sh ~/.local/bin/dev
```

> If this is your first time using `$HOME/.local`, you might need to create the directories.
>
> ```sh
> mkdir -p ~/.local/bin
> mkdir -p ~/.local/opt
> ```
