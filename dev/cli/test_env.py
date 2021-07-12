from typer.testing import CliRunner

from .env import app

import pytest

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [
        ["create"],
        "create: default (container: default, image: default, volume: default)"
    ],
    [
        ["create", "test"],
        "create: test (container: default, image: default, volume: default)"
    ]
])
def test_create(args, stdout):
    """Make sure the environment is created."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout
    assert result.exit_code == 0

@pytest.mark.parametrize("args,stdout", [
    [["destroy", "-y"], "destroy: default"],
    [["destroy", "-y", "test"], "destroy: test"]
])
def test_destroy(args, stdout):
    """Make sure the environment is destroyed."""
    result = runner.invoke(app, args)

    assert result.stdout.rstrip() == stdout.rstrip()
    assert result.exit_code == 0

def test_destroy_prompt():
    """Make sure the user is prompted to confirm before destroying."""
    result = runner.invoke(app, ["destroy"])

    assert result.stdout.rstrip() == "Are you sure? [y/N]:"
    assert result.exit_code == 0

def test_list():
    """Make sure the available environments are listed."""
    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "list"
    assert result.exit_code == 0
