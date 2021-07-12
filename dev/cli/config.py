import typer

app = typer.Typer(help="Manages under-the-hood configuration settings.")

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
    typer.echo(f"get: {name}")

@app.command()
def list():
    """
    Lists the available configuration settings.
    """
    typer.echo("list")

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
    typer.echo(f"set: {name} = {value}")
