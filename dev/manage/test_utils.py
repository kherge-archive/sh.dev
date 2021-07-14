from . import utils

from unittest import mock

@mock.patch("os.getgid")
def test_get_group_id(mock_getgid: mock.Mock):
    mock_getgid.return_value = 123

    result = utils.get_group_id()

    mock_getgid.assert_called_once()

    assert result == 123

@mock.patch("grp.getgrgid")
@mock.patch("os.getgid")
def test_get_group_name(mock_getgid: mock.Mock, mock_getgrgid: mock.Mock):
    mock_getgid.return_value = 123
    mock_getgrgid.return_value.gr_name = "test"

    result = utils.get_group_name()

    mock_getgid.assert_called_once()
    mock_getgrgid.assert_called_once_with(123)

    assert result == "test"

@mock.patch("dev.manage.config.get")
def test_get_label(mock_get: mock.Mock):
    mock_get.return_value = "value"

    assert utils.get_label() == f"{utils.LABEL_NAME}=value"
    assert utils.get_label(with_name=False) == "value"

@mock.patch("os.getuid")
def test_get_user_id(mock_getuid: mock.Mock):
    mock_getuid.return_value = 123

    result = utils.get_user_id()

    mock_getuid.assert_called_once()

    assert result == 123

@mock.patch("pwd.getpwuid")
@mock.patch("os.getuid")
def test_get_user_name(mock_getuid: mock.Mock, mock_getpwuid: mock.Mock):
    mock_getuid.return_value = 123
    mock_getpwuid.return_value.pw_name = "test"

    result = utils.get_user_name()

    mock_getuid.assert_called_once()
    mock_getpwuid.assert_called_once_with(123)

    assert result == "test"

@mock.patch("dev.manage.config.get")
def test_is_managed(mock_get: mock.Mock):
    mock_get.return_value = "test"

    object = mock.MagicMock()
    object.labels = {
        utils.LABEL_NAME: "test"
    }

    result = utils.is_managed(object)

    mock_get.assert_called_once()

    assert result == True
