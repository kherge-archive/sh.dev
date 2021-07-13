from .volume import app
from typer.testing import CliRunner
from typing import List
from unittest import mock

import pytest

runner = CliRunner()

def test_app():
    result = runner.invoke(app)

    assert result.exit_code == 0

@mock.patch("dev.manage.volume.create")
def test_create_with_name(mock_create: mock.Mock):
    result = runner.invoke(app, ["create", "test"])

    mock_create.assert_called_once_with("test")

    assert result.exit_code == 0

@mock.patch("dev.manage.volume.create")
def test_create_without_name(mock_create: mock.Mock):
    result = runner.invoke(app, ["create"])

    mock_create.assert_called_once_with("default")

    assert result.exit_code == 0

@mock.patch("dev.manage.volume.remove")
def test_destroy_with_name(mock_remove: mock.Mock):
    result = runner.invoke(app, ["destroy", "-y", "test"])

    mock_remove.assert_called_once_with("test")

    assert result.exit_code == 0

@mock.patch("dev.manage.volume.remove")
def test_destroy_without_name(mock_remove: mock.Mock):
    result = runner.invoke(app, ["destroy", "-y"])

    mock_remove.assert_called_once_with("default")

    assert result.exit_code == 0

@mock.patch("dev.cli.volume.tabulate")
@mock.patch("dev.manage.volume.listing")
def test_listing(mock_listing: mock.Mock, mock_tabulate: mock.Mock):
    mock_listing.return_value = ["a", "b", "c"]
    mock_tabulate.return_value = "tabulated"

    result = runner.invoke(app, ["list"])

    mock_tabulate.assert_called_once_with(
        [["a"], ["b"], ["c"]],
        headers=["Name"]
    )

    assert result.stdout.rstrip() == "tabulated"
    assert result.exit_code == 0
