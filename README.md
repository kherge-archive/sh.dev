sh.dev
======

Manages access to a persistent, containerized development environment.

```sh
user@host:~$ dev
user@dev:~$
```

Features
--------

- Uses a customizable Dockerfile for easy, iterative changes to the OS.
    - Bundles [`sh.env`](https://github.com/kherge/sh.env).
- Uses a data volume to persist the home directory across containers.
- Matches the user name, UID, group name, and GID in the container.

Requirements
------------

- Docker
- Python 3

Installation
------------

1. Clone this repository to `$HOME/.local/opt/sh.dev`.
2. Run `pip3 install -r $HOME/.local/opt/sh.dev/app/requirements.txt`.
3. Symlink `$HOME/.local/opt/sh.dev/app/dev.py` to `dev` somewhere in your `PATH`.

Usage
-----

All help and usage documentation is built into the tool.

```sh
# Root command help.
dev -h

# Container management help.
dev container -h

# Image management help.
dev image -h

# Volume management help.
dev volume -h
```

### Running

The `dev` command without any arguments will create the volume, image, and
container before attaching a shell. If any of those already exist, they will
be re-used.

### Root Access

You can use `sudo` with the password `dev`.

```sh
user@dev:~$ sudo apt install <package>
```

> Instead of installing packages after the fact, I recommend customizing the
> Dockerfile to install those packages. This will allow package installation
> to be preserved across container destroy/create.

### Updating the Container

Once you have customized the `Dockerfile`, you will need to manage the
container and image before the changes can be applied.

```sh
dev container stop
dev container destroy
dev image destroy
dev
```
