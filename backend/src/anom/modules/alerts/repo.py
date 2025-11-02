"""In-memory repository for alerts."""
from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from anom.modules.alerts.domain import Alert, AlertStatus


class AlertRepository:
    """Stores alerts keyed by their identifier."""

    def __init__(self) -> None:
        self._alerts: Dict[UUID, Alert] = {}

    def add_alert(self, alert: Alert) -> Alert:
        self._alerts[alert.id] = alert
        return alert.model_copy()

    def list_alerts(self, business_id: Optional[UUID] = None, status: Optional[AlertStatus] = None) -> List[Alert]:
        alerts = self._alerts.values()
        if business_id:
            alerts = [a for a in alerts if a.business_id == business_id]
        else:
            alerts = list(alerts)
        if status:
            alerts = [a for a in alerts if a.status == status]
        return [a.model_copy() for a in alerts]

    def get_alert(self, alert_id: UUID) -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        return alert.model_copy() if alert else None

    def update_alert(self, alert: Alert) -> Alert:
        self._alerts[alert.id] = alert
        return alert.model_copy()

    def clear(self) -> None:
        self._alerts.clear()
