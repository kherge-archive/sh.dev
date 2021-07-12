from .cli import config, container, env, image, volume

import typer

app = typer.Typer(add_completion=False)
app.add_typer(config.app)
app.add_typer(container.app)
app.add_typer(env.app)
app.add_typer(image.app)
app.add_typer(volume.app)
