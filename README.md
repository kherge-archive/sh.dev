Containerized Development Environment Manager
=============================================

Manages access to a persistent, containerized development environment.

```sh
user@host:~$ dev shell
[...]
user@88ccb4fd6a0e:~$
```

Features
--------

- The container user's home folder persists across container instances through a volume.
    - Eases iterative changes to the container.
- The user name, UID, and GID match the host user name, UID, and GID.
- The shell script is portable across POSIX-compliant shells.
- Has [`sh.env`](https://github.com/kherge/sh.env) installed by default.

Requirements
------------

- Docker
- POSIX-compliant Shell

Installation
------------

1. Clone this repository to `$HOME/.local/opt/sh.dev`.
2. Symlink `$HOME/.local/opt/sh.dev/dev.sh` to somewhere in your `PATH`.

Usage
-----

### Running

Run `dev` without arguments to see a usage guide.

```sh
$ dev
```

### Root Access

You can use `sudo` with the password `dev`.

```sh
$ sudo apt install <package>
```

### Installing Binaries

- When installing binaries, install them per user instead of system wide.
    - For example, use [nvm](https://github.com/nvm-sh/nvm) or [SDKMAN!](https://sdkman.io/).
- Packages should probably be installed through the `Dockerfile`.
    1. Find `DOCKERFILE` and add the desired packages.
    2. Run `./dev clean -c -i`.
    3. Run `./dev shell`.
