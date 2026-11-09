from fastapi import FastAPI

from app.config import settings


def create_app() -> FastAPI:
    """Build the FastAPI application.

    A factory rather than a module-level app so tests can build a fresh
    instance with their own settings and dependencies.
    """
    app = FastAPI(title=settings.app_name)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
