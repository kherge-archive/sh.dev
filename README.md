sh.dev
======

A tool to manage containerized development environments.

```sh
me@host:~$ dev
me@guest:~$ echo "I'm inside the container!"
```

Requirements
------------

- Docker
- Python 3.8+

Installing
----------

### Linux

TBD

### macOS

TBD

### Windows

TBD

Usage
-----

TBD

Development
-----------

[Poetry](https://python-poetry.org/) is used for package management.

    poetry install

### Unit Tests

Unit tests can be run once with `pytest`. To include code coverage reporting, use `pytest --cov dev/`. To generate an HTML report on code coverage, use `pytest --cov dev --cov-report=html`.

#### Watching for Changes

To run unit tests using a watcher, use `ptw`.

License
-------

This project is released under the ISC license.
