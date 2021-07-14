from ..manage import config, volume
from .utils import handle_error
from tabulate import tabulate

import typer

app = typer.Typer(help="Manages the volumes.", name="volume")

@app.command()
def create(
    name: str = typer.Argument(
        config.get("core.name"),
        help="The name of the volume."
    )
):
    """
    Creates a new volume.
    """
    try:
        volume.create(name)
    except BaseException as error:
        handle_error(error)

@app.command()
def destroy(
    confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Confirm destruction.",
        confirmation_prompt=True,
        prompt="Are you sure?",
        show_default=False
    ),
    name: str = typer.Argument(
        config.get("core.name"),
        help="The name of the volume."
    )
):
    """
    Destroys an existing volume.
    """
    try:
        if confirm:
            volume.remove(name)
    except BaseException as error:
        handle_error(error)

@app.command(name="list")
def listing():
    """
    Lists the available volumes.
    """
    try:
        volumes = list(map(lambda name: [name], volume.listing()))

        typer.echo(tabulate(volumes, headers=["Name"]))
    except BaseException as error:
        handle_error(error)
