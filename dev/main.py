from .cli import config, container, env, image, volume

import typer

app = typer.Typer(add_completion=False)
app.add_typer(config.app, name="config")
app.add_typer(container.app, name="container")
app.add_typer(env.app, name="env")
app.add_typer(image.app, name="image")
app.add_typer(volume.app, name="volume")
