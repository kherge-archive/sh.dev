from typer.testing import CliRunner

from .config import app

runner = CliRunner()

def test_app():
    """Make sure the app can run without any arguments."""
    result = runner.invoke(app)

    assert result.exit_code == 0

def test_get():
    """Make sure the configuration setting value is printed."""
    result = runner.invoke(app, ["get", "test"])

    assert result.stdout.rstrip() == "get: test"
    assert result.exit_code == 0

def test_list():
    """Make sure the available settings and their values are listed."""
    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "list"
    assert result.exit_code == 0

def test_set():
    """Make sure the configuration setting value is replaced."""
    result = runner.invoke(app, ["set", "test", "value"])

    assert result.stdout.rstrip() == "set: test = value"
    assert result.exit_code == 0
