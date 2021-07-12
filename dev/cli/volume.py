import typer

app = typer.Typer(help="Manages the volumes.", name="volume")

@app.command()
def create(
    name: str = typer.Argument(
        "default",
        help="The name of the volume."
    )
):
    """
    Creates a new volume.
    """
    typer.echo(f'create: {name}')

@app.command()
def destroy(
    name: str = typer.Argument(
        "default",
        help="The name of the volume."
    )
):
    """
    Destroys an existing volume.
    """
    typer.echo(f'destroy: {name}')

@app.command()
def list():
    """
    Lists the available volumes.
    """
    typer.echo('list')
