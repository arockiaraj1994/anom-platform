"""FastAPI router exposing rule management endpoints."""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from anom.api.deps import get_rule_service
from anom.modules.business_def.domain import BusinessNotFoundError
from anom.modules.rules.domain import RuleDefinition, RuleNotFoundError
from anom.modules.rules.service import RuleCreate, RuleService

router = APIRouter()


@router.post(
    "/{business_id}",
    response_model=RuleDefinition,
    status_code=status.HTTP_201_CREATED,
)
def create_rule(
    business_id: UUID,
    payload: RuleCreate,
    service: RuleService = Depends(get_rule_service),
) -> RuleDefinition:
    try:
        return service.create_rule(business_id, payload)
    except BusinessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


@router.get("/{business_id}", response_model=List[RuleDefinition])
def list_rules(
    business_id: UUID,
    service: RuleService = Depends(get_rule_service),
) -> List[RuleDefinition]:
    try:
        return service.list_rules(business_id)
    except BusinessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


@router.get("/{business_id}/{rule_id}", response_model=RuleDefinition)
def get_rule(
    business_id: UUID,
    rule_id: UUID,
    service: RuleService = Depends(get_rule_service),
) -> RuleDefinition:
    try:
        return service.get_rule(business_id, rule_id)
    except RuleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found") from exc


__all__ = ["router"]
