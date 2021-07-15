from ..manage import config, volume
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
    volume.create(name)

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
    if confirm:
        volume.remove(name)

@app.command(name="list")
def listing():
    """
    Lists the available volumes.
    """
    volumes = list(map(lambda name: [name], volume.listing()))

    typer.echo(tabulate(volumes, headers=["Name"]))
