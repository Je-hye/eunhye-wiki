import os

from fastapi import FastAPI

from app.factory import create_app
from app.settings import Settings


def build_app() -> FastAPI:
    mode = os.environ.get("APP_MODE", "")
    if mode != "private":
        raise RuntimeError("The private entrypoint requires APP_MODE=private")

    settings = Settings.from_values(
        app_mode=mode,
        database_url=os.environ.get("DATABASE_URL", ""),
        notes_path=os.environ.get("NOTES_PATH"),
    )
    return create_app(settings)


app = build_app()
