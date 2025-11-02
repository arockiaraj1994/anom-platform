"""In-memory repository for business definitions and schema fields."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from uuid import UUID

from anom.modules.business_def.domain import BusinessDefinition, FieldDefinition


class BusinessRepository:
    """Simple in-memory persistence layer used for the first iteration."""

    def __init__(self) -> None:
        self._businesses: Dict[UUID, BusinessDefinition] = {}
        self._fields: Dict[UUID, Dict[UUID, FieldDefinition]] = {}

    def add_business(self, business: BusinessDefinition) -> BusinessDefinition:
        self._businesses[business.id] = business
        return business.model_copy()

    def list_businesses(self) -> List[BusinessDefinition]:
        return [b.model_copy() for b in self._businesses.values()]

    def get_business(self, business_id: UUID) -> Optional[BusinessDefinition]:
        business = self._businesses.get(business_id)
        return business.model_copy() if business else None

    def update_business(self, business: BusinessDefinition) -> BusinessDefinition:
        self._businesses[business.id] = business
        return business.model_copy()

    def add_field(self, field: FieldDefinition) -> FieldDefinition:
        fields_for_business = self._fields.setdefault(field.business_id, {})
        fields_for_business[field.id] = field
        return field.model_copy()

    def list_fields(self, business_id: UUID) -> List[FieldDefinition]:
        fields = self._fields.get(business_id, {})
        return [f.model_copy() for f in fields.values()]

    def get_field(self, business_id: UUID, field_id: UUID) -> Optional[FieldDefinition]:
        field = self._fields.get(business_id, {}).get(field_id)
        return field.model_copy() if field else None

    def iter_fields(self, business_id: UUID) -> Iterable[FieldDefinition]:
        yield from (f.model_copy() for f in self._fields.get(business_id, {}).values())

    def clear(self) -> None:
        self._businesses.clear()
        self._fields.clear()
