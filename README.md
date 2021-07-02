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
- The [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) paths are used.
    - `$XDG_CONFIG_HOME/dev`
    - `$XDG_DATA_HOME/dev`

Requirements
------------

- Docker
- POSIX-compliant Shell

Installation
------------

1. Copy `dev.sh` to somewhere in your `$PATH`.
2. Rename `dev.sh` to `dev`.
3. Make it executable (e.g. `chmod 755 dev`).

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
