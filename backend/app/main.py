from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.audit_routes import router as audit_router
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.import_routes import router as import_router
from app.api.routes.meta_routes import router as meta_router
from app.api.routes.project_routes import router as project_router
from app.api.routes.query_history_routes import router as query_history_router
from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(import_router, prefix="/api")
    app.include_router(project_router, prefix="/api")
    app.include_router(meta_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(audit_router, prefix="/api")
    app.include_router(query_history_router, prefix="/api")

    @app.on_event("startup")
    def on_startup() -> None:
        settings.upload_path.mkdir(parents=True, exist_ok=True)
        settings.export_path.mkdir(parents=True, exist_ok=True)
        init_db()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
