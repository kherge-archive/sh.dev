from typer.testing import CliRunner

from .volume import app

import pytest

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["create"], f"create: default"],
    [["create", "test"], "create: test"]
])
def test_create(args, stdout):
    """Make sure the volume is created."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["destroy"], "destroy: default"],
    [["destroy", "test"], "destroy: test"]
])
def test_destroy(args, stdout):
    """Make sure the volume is destroyed."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

def test_list():
    """Make sure the available volume are listed."""
    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "list"
    assert result.exit_code == 0
