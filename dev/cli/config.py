from .. import CONFIG_DIR
from ..manage import config
from tabulate import tabulate

import os
import typer

app = typer.Typer(
    help="Manages under-the-hood configuration settings.",
    name="config"
)

@app.command()
def get(
    name: str = typer.Argument(
        ...,
        help="The name of the configuration setting."
    )
):
    """
    Retrieves the value of a configuration setting.
    """
    if config.exists(name):
        typer.echo(config.get(name))
    else:
        typer.secho("<not set>", err=True, fg=typer.colors.RED)

@app.command(name="list")
def listing():
    """
    Lists the available configuration settings.
    """
    paths = os.listdir(CONFIG_DIR)
    paths.sort()

    table = []

    for path in paths:
        name = os.path.splitext(path)[0]
        value = config.get(name)

        table.append([name, value])

    typer.echo(tabulate(table, headers=["key", "value"]))

@app.command()
def set(
    name: str = typer.Argument(
        ...,
        help="The name of the configuration setting."
    ),
    value: str = typer.Argument(
        ...,
        help="The new value for the configuration setting."
    )
):
    """
    Sets the value of a configuration setting.
    """
    config.set(name, value)
