"""In-memory repository for storing ingested events."""
from __future__ import annotations

from typing import Dict, List
from uuid import UUID

from anom.modules.ingestion.domain import EventRecord


class EventRepository:
    """Stores event records grouped by business."""

    def __init__(self) -> None:
        self._events: Dict[UUID, List[EventRecord]] = {}

    def add_event(self, event: EventRecord) -> EventRecord:
        events_for_business = self._events.setdefault(event.business_id, [])
        events_for_business.append(event)
        return event.model_copy()

    def list_events(self, business_id: UUID) -> List[EventRecord]:
        return [event.model_copy() for event in self._events.get(business_id, [])]

    def clear(self) -> None:
        self._events.clear()
