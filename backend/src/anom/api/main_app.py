"""Application entry-point for the Anom Platform backend."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from anom.modules.alerts.api import router as alerts_router
from anom.modules.business_def.api import router as business_router
from anom.modules.ingestion.api import router as ingestion_router
from anom.modules.rules.api import router as rules_router


def create_app() -> FastAPI:
    app = FastAPI(title="Anom Platform API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(business_router, prefix="/businesses", tags=["businesses"])
    app.include_router(ingestion_router, prefix="/ingest", tags=["ingestion"])
    app.include_router(rules_router, prefix="/rules", tags=["rules"])
    app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])

    return app


app = create_app()


__all__ = ["app", "create_app"]
