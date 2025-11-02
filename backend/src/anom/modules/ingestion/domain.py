"""Domain models for event ingestion."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field


class EventIngestRequest(BaseModel):
    """Incoming event payload."""

    payload: Dict[str, Any] = Field(..., description="Normalized event payload")


class EventRecord(BaseModel):
    """Stored representation of an ingested event."""

    id: UUID
    business_id: UUID
    payload: Dict[str, Any]
    received_at: datetime
