from ..manage import config

import typer

app = typer.Typer(help="Manages the environments.", name="env")

@app.command()
def create(
    container: str = typer.Option(
        config.get("core.name"),
        "-c",
        "--container",
        help="The name of the container.",
        metavar="NAME"
    ),
    image: str = typer.Option(
        config.get("core.name"),
        "-i",
        "--image",
        help="The name of the image.",
        metavar="NAME"
    ),
    name: str = typer.Argument(
        config.get("core.name"),
        help="The name of the environment."
    ),
    volume: str = typer.Option(
        config.get("core.name"),
        "-v",
        "--volume",
        help="The name of the volume.",
        metavar="NAME"
    )
):
    """
    Creates a new containerized development environment.

    If the data volume, image, or container do not exist, they will be created
    using their corresponding names (or default values). If any of these objects
    already exist, then they will be re-used instead.
    """
    typer.echo(f"create: {name} (container: {container}, image: {image}, volume: {volume})")

@app.command()
def destroy(
    confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        confirmation_prompt=True,
        help="Confirm destruction.",
        prompt="Are you sure?"
    ),
    name: str = typer.Argument(
        config.get("core.name"),
        help="The name of the environment."
    )
):
    """
    Destroys an existing containerized development environment.

    Any data volume, image, or container that match their corresponding names
    (or default values) will be permantently removed. Since recovery will not
    be possible, it is advised that you make any backups you may need later.

    To delete just the data volume, image, or container for the environment,
    consider using the container, image, and volume commands instead.
    """
    if confirm:
        typer.echo(f"destroy: {name}")

@app.command(name="list")
def listing():
    """
    Lists the available environments.
    """
    typer.echo('list')
