"""Application service responsible for event ingestion."""
from __future__ import annotations

from datetime import datetime
from typing import List, Tuple
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from anom.modules.alerts.service import AlertCreate, AlertService
from anom.modules.business_def.domain import BusinessNotFoundError
from anom.modules.business_def.service import BusinessService
from anom.modules.ingestion.domain import EventIngestRequest, EventRecord
from anom.modules.ingestion.repo import EventRepository
from anom.modules.ingestion.validators import normalize_payload
from anom.modules.rule_engine.dispatcher import RuleDispatcher


class IngestionService:
    """Validates events, stores them, and triggers rule evaluation."""

    def __init__(
        self,
        business_service: BusinessService,
        event_repository: EventRepository,
        rule_dispatcher: RuleDispatcher,
        alert_service: AlertService,
    ) -> None:
        self._business_service = business_service
        self._event_repository = event_repository
        self._rule_dispatcher = rule_dispatcher
        self._alert_service = alert_service

    def ingest(self, business_id: UUID, payload: EventIngestRequest) -> Tuple[EventRecord, List[str]]:
        try:
            business = self._business_service.get_business(business_id)
        except BusinessNotFoundError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc

        fields = self._business_service.list_fields(business_id)
        normalized_payload = normalize_payload(payload.payload, fields)

        event = EventRecord(
            id=uuid4(),
            business_id=business.id,
            payload=normalized_payload,
            received_at=datetime.utcnow(),
        )
        stored_event = self._event_repository.add_event(event)

        triggered_rules = self._rule_dispatcher.evaluate_event(business_id, stored_event)
        alert_messages: List[str] = []
        for rule in triggered_rules:
            alert = self._alert_service.create_alert(
                AlertCreate(
                    business_id=business_id,
                    rule_id=rule.id,
                    event_id=stored_event.id,
                    message=f"Rule '{rule.name}' triggered",
                    severity=rule.severity,
                )
            )
            alert_messages.append(alert.message)

        return stored_event, alert_messages

    def list_events(self, business_id: UUID) -> List[EventRecord]:
        return self._event_repository.list_events(business_id)


__all__ = ["IngestionService", "EventIngestRequest", "EventRecord"]
