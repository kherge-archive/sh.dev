import logging
import typer

def echo_error(error: BaseException):
    """Prints the error message, or re-raises the error if DEBUG logging."""
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        raise error
    else:
        typer.secho(str(error), fg=typer.colors.RED)

        raise typer.Exit(code=1)
