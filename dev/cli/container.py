import typer

app = typer.Typer(help="Manages the containers.")

@app.command()
def create(
    image: str = typer.Option(
        "default",
        "-i",
        "--image",
        help="The name of the image used to create the container."
    ),
    name: str = typer.Argument(
        "default",
        help="The name of the container."
    )
):
    """
    Creates a new container.
    """
    typer.echo(f'create: {name} (image: {image})')

@app.command()
def destroy(
    name: str = typer.Argument(
        "default",
        help="The name of the container."
    )
):
    """
    Destroys an existing container.
    """
    typer.echo(f'destroy: {name}')

@app.command()
def list():
    """
    Lists the available containers.
    """
    typer.echo('list')
