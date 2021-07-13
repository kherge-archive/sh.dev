from . import utils
from unittest import mock

import typer

@mock.patch("typer.secho")
@mock.patch("logging.getLogger")
def test_handle_error_print(mock_getLogger: mock.Mock, mock_secho: mock.Mock):
    logger = mock.MagicMock()
    logger.isEnabledFor.return_value = False

    mock_getLogger.return_value = logger

    error = "The error message."

    try:
        utils.handle_error(error)
    except BaseException as caught:
        assert isinstance(caught, typer.Exit)

        mock_secho.assert_called_once_with(error, fg="red")

@mock.patch("logging.getLogger")
def test_handle_error_raise(mock_getLogger: mock.Mock):
    logger = mock.MagicMock()
    logger.isEnabledFor.return_value = True

    mock_getLogger.return_value = logger

    expected = Exception("The test exception.")

    try:
        utils.handle_error(expected)
    except BaseException as actual:
        assert expected == actual
