"""Application services for managing businesses and their schema."""
from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from anom.modules.business_def.domain import (
    BusinessCreate,
    BusinessDefinition,
    BusinessNotFoundError,
    BusinessUpdate,
    FieldDataType,
    FieldDefinition,
    FieldDefinitionCreate,
)
from anom.modules.business_def.repo import BusinessRepository


class BusinessService:
    """Coordinates persistence and validation for business definitions."""

    def __init__(self, repository: BusinessRepository) -> None:
        self._repository = repository

    def create_business(self, payload: BusinessCreate) -> BusinessDefinition:
        business = BusinessDefinition(
            id=uuid4(),
            name=payload.name,
            description=payload.description,
            created_at=datetime.utcnow(),
        )
        return self._repository.add_business(business)

    def list_businesses(self) -> List[BusinessDefinition]:
        return self._repository.list_businesses()

    def get_business(self, business_id: UUID) -> BusinessDefinition:
        business = self._repository.get_business(business_id)
        if business is None:
            raise BusinessNotFoundError(str(business_id))
        return business

    def update_business(self, business_id: UUID, payload: BusinessUpdate) -> BusinessDefinition:
        business = self.get_business(business_id)
        data = payload.model_dump(exclude_unset=True)
        updated = business.model_copy(update=data)
        return self._repository.update_business(updated)

    def add_field(self, business_id: UUID, payload: FieldDefinitionCreate) -> FieldDefinition:
        self.get_business(business_id)
        field = FieldDefinition(
            id=uuid4(),
            business_id=business_id,
            name=payload.name,
            data_type=payload.data_type,
            required=payload.required,
            description=payload.description,
            created_at=datetime.utcnow(),
        )
        return self._repository.add_field(field)

    def list_fields(self, business_id: UUID) -> List[FieldDefinition]:
        self.get_business(business_id)
        return self._repository.list_fields(business_id)


__all__ = [
    "BusinessService",
    "BusinessCreate",
    "BusinessDefinition",
    "FieldDefinition",
    "FieldDefinitionCreate",
    "FieldDataType",
    "BusinessNotFoundError",
]
