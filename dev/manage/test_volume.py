from . import volume
from .utils import LABEL_NAME
from unittest import mock

import pytest

@mock.patch("dev.manage.config.get")
def test_create(mock_get: mock.Mock):
    client = mock.MagicMock()
    mock_get.return_value = "test"

    volume.create("test", client=client)

    mock_get.assert_called_once_with("core.label")
    client.volumes.create.assert_called_once_with(
        name="test",
        labels={LABEL_NAME:"test"}
    )

@mock.patch("dev.manage.config.get")
def test_exists(mock_get):
    mock_get.return_value = "test"

    client = mock.MagicMock()
    found = mock.MagicMock()

    client.volumes.get.return_value = found
    found.attrs = {
        "Labels": {
            LABEL_NAME: "test"
        }
    }

    result = volume.exists("test", client)

    client.volumes.get.assert_called_once_with("test")

    assert result == True

@mock.patch("dev.manage.config.get")
def test_listing(mock_get: mock.Mock):
    mock_get.return_value = "test"

    listed = mock.MagicMock()
    listed.name = "listed"

    client = mock.MagicMock()
    client.volumes.list.return_value = [listed]

    result = volume.listing(client)

    client.volumes.list.assert_called_once_with(filters={
        "label": f"{LABEL_NAME}=test"
    })

    assert result == ["listed"]

@mock.patch("dev.manage.config.get")
def test_remove(mock_get: mock.Mock):
    mock_get.return_value = "test"

    client = mock.MagicMock()
    found = mock.MagicMock()

    client.volumes.get.return_value = found
    found.attrs = {
        "Labels": {
            LABEL_NAME: "test"
        }
    }

    volume.remove("test", client)

    client.volumes.get.assert_called_once_with("test")
    found.remove.assert_called_once()
