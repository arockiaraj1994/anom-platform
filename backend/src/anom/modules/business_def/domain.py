"""Domain models for business definitions and schema fields."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FieldDataType(str, Enum):
    """Supported data types for a field definition."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"


class BusinessCreate(BaseModel):
    """Payload required to create a business definition."""

    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)


class BusinessUpdate(BaseModel):
    """Payload to update mutable business attributes."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)


class BusinessDefinition(BusinessCreate):
    """Representation of a business use case within the platform."""

    id: UUID
    created_at: datetime


class FieldDefinitionCreate(BaseModel):
    """Payload required to create a schema field for a business."""

    name: str = Field(..., min_length=1, max_length=120)
    data_type: FieldDataType
    required: bool = True
    description: Optional[str] = Field(default=None, max_length=500)


class FieldDefinition(FieldDefinitionCreate):
    """Schema field tied to a specific business definition."""

    id: UUID
    business_id: UUID
    created_at: datetime


class BusinessNotFoundError(Exception):
    """Raised when an operation references an unknown business."""

    pass


class FieldNotFoundError(Exception):
    """Raised when an operation references an unknown field."""

    pass
