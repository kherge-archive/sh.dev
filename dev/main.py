from .cli import config, container, env, image, volume
from .manage.config import default

import logging
import typer

# Set default settings.
default("core.label", "default")
default("core.name", "default")

app = typer.Typer(add_completion=False)
app.add_typer(config.app)
app.add_typer(container.app)
app.add_typer(env.app)
app.add_typer(image.app)
app.add_typer(volume.app)

# Configure root logger.
logging.basicConfig(
    format="%(name)s: %(message)s",
    level=logging.ERROR
)

def setVerbosity(level: int):
    """Sets the logging level based on the verbosity requested.

    The verbosity level is mapped to these logging levels:
    - >=3 is DEBUG
    - ==2 is INFO
    - ==1 is WARN
    """
    logger = logging.getLogger()

    if level >= 3:
        logger.setLevel(logging.DEBUG)
    elif level == 2:
        logger.setLevel(logging.INFO)
    elif level == 1:
        logger.setLevel(logging.WARN)

    logger.debug(f"verbosity is {level}")

@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    _: int = typer.Option(
        0,
        "-v",
        "--verbose",
        callback=setVerbosity,
        count=True,
        help="Increases verbosity of invoked commands."
    )
):
    """A tool to manage containerized development environments."""
    if context.invoked_subcommand is not None:
        return

    typer.echo("default")
