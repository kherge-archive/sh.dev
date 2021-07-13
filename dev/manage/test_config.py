from . import config

from pytest_mock import MockerFixture
from unittest import mock


@mock.patch("pathlib.Path.open")
@mock.patch("pathlib.Path.exists")
@mock.patch("json.load")
def test_get(
    mock_load: mock.Mock,
    mock_exists: mock.Mock,
    mock_open: mock.Mock,
    mocker: MockerFixture
):
    toPathSpy = mocker.spy(config, "_toPath")
    mock_exists.return_value = True
    mock_load.return_value = "json value"

    value = config.get("test")

    toPathSpy.assert_called_once_with("test")
    mock_exists.assert_called_once()
    mock_open.assert_called_once()
    mock_load.assert_called_once()

    assert value == "json value"

@mock.patch("pathlib.Path.exists")
def test_exists(mock_exists: mock.Mock, mocker: MockerFixture):
    toPathSpy = mocker.spy(config, "_toPath")
    mock_exists.return_value = True

    result = config.exists("test")

    toPathSpy.assert_called_once_with("test")
    mock_exists.assert_called_once()

    assert result == True

@mock.patch("pathlib.Path.open")
@mock.patch("json.dump")
def test_set_with(
    mock_dump: mock.Mock,
    mock_open: mock.Mock,
    mocker: MockerFixture
):
    toPathSpy = mocker.spy(config, "_toPath")

    config.set("test", "value")

    toPathSpy.assert_called_once_with("test")
    mock_open.assert_called_once()
    mock_dump.assert_called_once()

    assert mock_dump.call_args_list[0][0][0] == "value"

@mock.patch("pathlib.Path.unlink")
def test_set_without(
    mock_unlink: mock.Mock,
    mocker: MockerFixture
):
    toPathSpy = mocker.spy(config, "_toPath")

    config.set("test", None)

    toPathSpy.assert_called_once_with("test")
    mock_unlink.assert_called_once()
