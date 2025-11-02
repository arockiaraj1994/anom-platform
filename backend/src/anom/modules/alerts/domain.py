"""Domain objects describing generated alerts."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from anom.modules.rules.domain import SeverityLevel


class AlertStatus(str, Enum):
    """Possible lifecycle states for an alert."""

    OPEN = "open"
    ACKED = "acked"
    CLOSED = "closed"


class AlertCreate(BaseModel):
    """Payload needed to register an alert."""

    business_id: UUID
    rule_id: UUID
    event_id: UUID
    message: str = Field(..., min_length=1, max_length=500)
    severity: SeverityLevel


class Alert(AlertCreate):
    """Stored alert model."""

    id: UUID
    created_at: datetime
    status: AlertStatus = AlertStatus.OPEN
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None


class AlertNotFoundError(Exception):
    """Raised when an alert cannot be found."""

    pass
