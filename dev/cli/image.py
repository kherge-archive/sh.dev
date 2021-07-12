from .. import DOCKER_DIR
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(help="Manages the images.", name="image")

@app.command()
def create(
    name: str = typer.Argument(
        "default",
        help="The name of the image."
    ),
    path: Path = typer.Argument(
        Path(DOCKER_DIR),
        help="The path to the directory containing the Dockerfile.",
        metavar="[DIR]"
    )
):
    """
    Creates a new image.
    """
    typer.echo(f'create: {name} (from: {path})')

@app.command()
def destroy(
    name: str = typer.Argument(
        "default",
        help="The name of the image."
    )
):
    """
    Destroys an existing image.
    """
    typer.echo(f'destroy: {name}')

@app.command()
def list():
    """
    Lists the available images.
    """
    typer.echo('list')
