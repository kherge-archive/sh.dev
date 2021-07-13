import typer

app = typer.Typer(help="Manages the containers.", name="container")

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

@app.command(name="list")
def listing():
    """
    Lists the available containers.
    """
    typer.echo('list')

@app.command()
def shell(
    name: str = typer.Argument(
        "default",
        help="The name of the container."
    )
):
    """
    Attaches a shell to the running container.
    """
    typer.echo(f'shell: {name}')

@app.command()
def start(
    name: str = typer.Argument(
        "default",
        help="The name of the container."
    )
):
    """
    Starts the stopped container.
    """
    typer.echo(f'start: {name}')

@app.command()
def stop(
    name: str = typer.Argument(
        "default",
        help="The name of the container."
    )
):
    """
    Stops the running container.
    """
    typer.echo(f'stop: {name}')
