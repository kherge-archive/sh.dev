import logging
import typer

def handle_error(error: BaseException):
    """Displays the error before exiting.

    If the current logging level is set to DEBUG, the error will be re-raised
    as is to allow the full stack trace to be printed for analysis. For any
    other logging level, the string representation of the error will be
    printed to STDERR and the typer.Exit error is raised with a status code
    of 1 (one).
    """
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        raise error
    else:
        typer.secho(str(error), fg=typer.colors.RED)

        raise typer.Exit(code=1)
