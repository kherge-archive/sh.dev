from .config import app
from typer.testing import CliRunner
from unittest import mock

runner = CliRunner()

def test_app():
    result = runner.invoke(app)

    assert result.exit_code == 0

@mock.patch("dev.manage.config.get")
@mock.patch("dev.manage.config.exists")
def test_get(mock_exists: mock.Mock, mock_get: mock.Mock):
    mock_exists.return_value = True
    mock_get.return_value = "mock value"

    result = runner.invoke(app, ["get", "test"])

    mock_exists.assert_called_once_with("test")
    mock_get.assert_called_once_with("test")

    assert result.stdout.rstrip() == "mock value"
    assert result.exit_code == 0

@mock.patch("dev.manage.config.exists")
def test_get_missing(mock_exists: mock.Mock):
    mock_exists.return_value = False

    result = runner.invoke(app, ["get", "test"])

    mock_exists.assert_called_once_with("test")

    assert result.stdout.rstrip() == "<not set>"
    assert result.exit_code == 0

@mock.patch("dev.cli.config.tabulate")
@mock.patch("os.listdir")
@mock.patch("dev.manage.config.get")
def test_list(mock_get: mock.Mock, mock_listdir: mock.Mock, mock_tabulate: mock.Mock):
    mock_get.side_effect = ["av", "bv", "cv"]
    mock_listdir.return_value = ["ak.json", "bk.json", "ck.json"]
    mock_tabulate.return_value = "tabulated"

    result = runner.invoke(app, ["list"])

    assert result.stdout.rstrip() == "tabulated"
    assert result.exit_code == 0

@mock.patch("dev.manage.config.set")
def test_set(mock_set: mock.Mock):
    result = runner.invoke(app, ["set", "test", "value"])

    mock_set.assert_called_once_with("test", "value")

    assert result.exit_code == 0
