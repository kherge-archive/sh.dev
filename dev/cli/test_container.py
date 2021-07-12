from typer.testing import CliRunner

from .container import app

import pytest

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["create"], "create: default (image: default)"],
    [["create", "test"], "create: test (image: default)"],
    [["create", "test", "-i", "image"], "create: test (image: image)"],
    [["create", "test", "--image", "image"], "create: test (image: image)"]
])
def test_create(args, stdout):
    """Make sure the container is created."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["destroy"], "destroy: default"],
    [["destroy", "test"], "destroy: test"]
])
def test_destroy(args, stdout):
    """Make sure the container is destroyed."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

def test_list():
    """Make sure the available containers are listed."""
    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "list"
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["start"], "start: default"],
    [["start", "test"], "start: test"]
])
def test_start(args, stdout):
    """Make sure the container is started."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["stop"], "stop: default"],
    [["stop", "test"], "stop: test"]
])
def test_stop(args, stdout):
    """Make sure the container is stopped."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0
