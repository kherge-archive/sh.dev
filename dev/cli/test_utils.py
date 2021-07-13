from . import utils
from unittest import mock

@mock.patch("typer.secho")
@mock.patch("logging.getLogger")
def test_echo_error_print(mock_getLogger: mock.Mock, mock_secho: mock.Mock):
    logger = mock.MagicMock()
    logger.isEnabledFor.return_value = False

    mock_getLogger.return_value = logger

    error = "The error message."

    utils.echo_error(error)

    mock_secho.assert_called_once_with(error, fg="red")

@mock.patch("logging.getLogger")
def test_echo_error_raise(mock_getLogger):
    logger = mock.MagicMock()
    logger.isEnabledFor.return_value = True

    mock_getLogger.return_value = logger

    expected = Exception("The test exception.")

    try:
        utils.echo_error(expected)
    except BaseException as actual:
        assert expected == actual
