from . import app
from .calcster import router

app.include_router(router)


def run() -> None:
    import os
    from pathlib import Path

    from fastapi_cli.cli import run

    root = Path(__file__).parent.parent
    os.chdir(root)
    run()
