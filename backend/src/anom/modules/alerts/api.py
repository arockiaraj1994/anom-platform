"""FastAPI router exposing alert operations."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from anom.api.deps import get_alert_service
from anom.modules.alerts.domain import Alert, AlertNotFoundError, AlertStatus
from anom.modules.alerts.service import AlertService

router = APIRouter()


class AlertAcknowledgeRequest(BaseModel):
    actor: str = Field(..., min_length=1, max_length=120)


@router.get("/", response_model=List[Alert])
def list_alerts(
    business_id: Optional[UUID] = Query(default=None),
    status_param: Optional[AlertStatus] = Query(default=None, alias="status"),
    service: AlertService = Depends(get_alert_service),
) -> List[Alert]:
    return service.list_alerts(business_id=business_id, status=status_param)


@router.get("/{alert_id}", response_model=Alert)
def get_alert(
    alert_id: UUID,
    service: AlertService = Depends(get_alert_service),
) -> Alert:
    try:
        return service.get_alert(alert_id)
    except AlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found") from exc


@router.post("/{alert_id}/ack", response_model=Alert)
def acknowledge_alert(
    alert_id: UUID,
    payload: AlertAcknowledgeRequest,
    service: AlertService = Depends(get_alert_service),
) -> Alert:
    try:
        return service.acknowledge_alert(alert_id, payload.actor)
    except AlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found") from exc


__all__ = ["router"]
