from .cli import config, container, env, image, volume

import logging
import typer

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

@app.callback()
def main(
    verbose: int = typer.Option(
        0,
        "-v",
        "--verbose",
        count=True,
        help="Increases verbosity of invoked commands."
    )
):
    """A tool to manage containerized development environments."""
    if verbose >= 3:
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose == 2:
        logging.getLogger().setLevel(logging.INFO)
    elif verbose == 1:
        logging.getLogger().setLevel(logging.WARN)
