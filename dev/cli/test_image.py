from typer.testing import CliRunner

from .. import DOCKER_DIR
from .image import app

import pytest

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["create"], f"create: default (from: {DOCKER_DIR})"],
    [["create", "test"], f"create: test (from: {DOCKER_DIR})"],
    [["create", "test", "/path/to/dir"], "create: test (from: /path/to/dir)"],
])
def test_create(args, stdout):
    """Make sure the image is created."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["destroy"], "destroy: default"],
    [["destroy", "test"], "destroy: test"]
])
def test_destroy(args, stdout):
    """Make sure the image is destroyed."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

def test_list():
    """Make sure the available images are listed."""
    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "list"
    assert result.exit_code == 0
