"""FastAPI router for ingesting events."""
from __future__ import annotations

from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends

from anom.api.deps import get_ingestion_service
from anom.modules.ingestion.domain import EventIngestRequest
from anom.modules.ingestion.service import IngestionService

router = APIRouter()


@router.post("/{business_id}")
def ingest_event(
    business_id: UUID,
    payload: EventIngestRequest,
    service: IngestionService = Depends(get_ingestion_service),
) -> Dict[str, Any]:
    event, alerts = service.ingest(business_id, payload)
    return {"event": event, "alerts": alerts}


@router.get("/{business_id}")
def list_events(
    business_id: UUID,
    service: IngestionService = Depends(get_ingestion_service),
) -> Dict[str, Any]:
    events = service.list_events(business_id)
    return {"events": events}


__all__ = ["router"]
