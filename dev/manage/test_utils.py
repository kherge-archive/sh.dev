from . import utils

from unittest import mock

@mock.patch("dev.manage.config.get")
def test_get_label(mock_get):
    mock_get.return_value = "value"

    assert utils.get_label() == f"{utils.LABEL_NAME}=value"
    assert utils.get_label(with_name=False) == "value"
