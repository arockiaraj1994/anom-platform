"""Application services for managing alerts."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from anom.modules.alerts.domain import Alert, AlertCreate, AlertNotFoundError, AlertStatus
from anom.modules.alerts.repo import AlertRepository


class AlertService:
    """Provides alert lifecycle operations."""

    def __init__(self, repository: AlertRepository) -> None:
        self._repository = repository

    def create_alert(self, payload: AlertCreate) -> Alert:
        alert = Alert(
            id=uuid4(),
            business_id=payload.business_id,
            rule_id=payload.rule_id,
            event_id=payload.event_id,
            message=payload.message,
            severity=payload.severity,
            created_at=datetime.utcnow(),
            status=AlertStatus.OPEN,
        )
        return self._repository.add_alert(alert)

    def list_alerts(
        self,
        *,
        business_id: Optional[UUID] = None,
        status: Optional[AlertStatus] = None,
    ) -> List[Alert]:
        return self._repository.list_alerts(business_id=business_id, status=status)

    def get_alert(self, alert_id: UUID) -> Alert:
        alert = self._repository.get_alert(alert_id)
        if alert is None:
            raise AlertNotFoundError(str(alert_id))
        return alert

    def acknowledge_alert(self, alert_id: UUID, actor: str) -> Alert:
        alert = self.get_alert(alert_id)
        updated = alert.model_copy(
            update={
                "status": AlertStatus.ACKED,
                "acknowledged_by": actor,
                "acknowledged_at": datetime.utcnow(),
            }
        )
        return self._repository.update_alert(updated)


__all__ = [
    "AlertService",
    "AlertCreate",
    "Alert",
    "AlertStatus",
    "AlertNotFoundError",
]
