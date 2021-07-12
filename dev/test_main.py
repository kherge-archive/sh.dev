from typer.testing import CliRunner

from .main import app

import pytest

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0
    assert result.stdout.rstrip() == "default"

@pytest.mark.parametrize("command", [
    "config",
    "container",
    "env",
    "image",
    "volume"
])
def test_subcommand(command):
    """Make sure the config command is registered."""
    result = runner.invoke(app, [command])

    assert result.exit_code == 0
