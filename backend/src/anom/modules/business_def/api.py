"""FastAPI router exposing business definition endpoints."""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from anom.api.deps import get_business_service
from anom.modules.business_def.domain import (
    BusinessDefinition,
    BusinessNotFoundError,
    FieldDefinition,
)
from anom.modules.business_def.service import (
    BusinessCreate,
    BusinessService,
    BusinessUpdate,
    FieldDefinitionCreate,
)

router = APIRouter()


@router.post("/", response_model=BusinessDefinition, status_code=status.HTTP_201_CREATED)
def create_business(
    payload: BusinessCreate,
    service: BusinessService = Depends(get_business_service),
) -> BusinessDefinition:
    return service.create_business(payload)


@router.get("/", response_model=List[BusinessDefinition])
def list_businesses(
    service: BusinessService = Depends(get_business_service),
) -> List[BusinessDefinition]:
    return service.list_businesses()


@router.get("/{business_id}", response_model=BusinessDefinition)
def get_business(
    business_id: UUID,
    service: BusinessService = Depends(get_business_service),
) -> BusinessDefinition:
    try:
        return service.get_business(business_id)
    except BusinessNotFoundError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


@router.patch("/{business_id}", response_model=BusinessDefinition)
def update_business(
    business_id: UUID,
    payload: BusinessUpdate,
    service: BusinessService = Depends(get_business_service),
) -> BusinessDefinition:
    try:
        return service.update_business(business_id, payload)
    except BusinessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


@router.post(
    "/{business_id}/fields",
    response_model=FieldDefinition,
    status_code=status.HTTP_201_CREATED,
)
def add_field(
    business_id: UUID,
    payload: FieldDefinitionCreate,
    service: BusinessService = Depends(get_business_service),
) -> FieldDefinition:
    try:
        return service.add_field(business_id, payload)
    except BusinessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


@router.get("/{business_id}/fields", response_model=List[FieldDefinition])
def list_fields(
    business_id: UUID,
    service: BusinessService = Depends(get_business_service),
) -> List[FieldDefinition]:
    try:
        return service.list_fields(business_id)
    except BusinessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found") from exc


__all__ = ["router"]
