from fastapi import FastAPI

from app.routes import private, public
from app.settings import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title=f"Je-hye Wiki {settings.app_mode.title()} API")
    app.state.settings = settings

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": settings.app_mode}

    if settings.app_mode == "public":
        app.include_router(public.router)
    else:
        app.include_router(private.router)

    return app
