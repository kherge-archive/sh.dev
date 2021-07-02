Containerized Development Environment Manager
=============================================

Uses Docker CLI to create a development environment as a container.

```sh
kherrera@machine Desktop % ./dev shell
[+] Building 1.5s (11/11) FINISHED                                                                                       
 => [internal] load build definition from Dockerfile                                                                0.0s
 => => transferring dockerfile: 882B                                                                                0.0s
 => [internal] load .dockerignore                                                                                   0.0s
 => => transferring context: 2B                                                                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:21.04                                                     1.3s
 => [auth] library/ubuntu:pull token for registry-1.docker.io                                                       0.0s
 => [1/6] FROM docker.io/library/ubuntu:21.04@sha256:a30456233740024b9d297f5bcaa7439446a97bc59b25cadcdae829c334827  0.0s
 => CACHED [2/6] RUN apt-get update &&     apt-get dist-upgrade -y &&     apt-get autoclean &&     apt-get autorem  0.0s
 => CACHED [3/6] RUN apt-get install -y     build-essential libssl-dev pkg-config     curl git gnupg2 sudo unzip v  0.0s
 => CACHED [4/6] RUN /bin/bash -c '[ "$(grep -F :20: < /etc/group)" != "" ] ||     addgroup --gid 20 "staff"'       0.0s
 => CACHED [5/6] RUN adduser --uid 501 --gid 20 "kherrera" &&     chown -R "kherrera:staff" "/home/kherrera" &&     0.0s
 => CACHED [6/6] WORKDIR /home/kherrera                                                                             0.0s
 => exporting to image                                                                                              0.0s
 => => exporting layers                                                                                             0.0s
 => => writing image sha256:35e3507030a86946720d6c3697b7f03c1e2847992ad8b7a8a0be3f4d103f4818                        0.0s
 => => naming to docker.io/library/dev:1.0                                                                          0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

kherrera@88ccb4fd6a0e:~$ 
```

Features
--------

- Script is (or should be) POSIX compliant for portability.
- Uses paths defined in the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).
- Uses a volume for the user's home folder.
    - Matches the username, UID, and GID.

Installation
------------

1. Copy `dev.sh` to somewhere in your `$PATH`.
2. Rename `dev.sh` to `dev`.
3. Make it executable (e.g. `chmod 755 dev`).

Usage
-----

Run `dev` without arguments to see a usage guide.
