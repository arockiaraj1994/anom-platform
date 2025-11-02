"""Domain models describing rules and their conditions."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """Coarse-grained severity levels used for alerts."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class RuleOperator(str, Enum):
    """Supported comparison operators for basic rules."""

    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"


class RuleCondition(BaseModel):
    """Condition that must hold true for a rule to fire."""

    field: str = Field(..., min_length=1, max_length=120)
    operator: RuleOperator
    value: Any


class RuleCreate(BaseModel):
    """Payload required to create a rule definition."""

    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    condition: RuleCondition
    severity: SeverityLevel = SeverityLevel.WARNING


class RuleDefinition(RuleCreate):
    """Stored rule definition."""

    id: UUID
    business_id: UUID
    created_at: datetime


class RuleNotFoundError(Exception):
    """Raised when an operation references an unknown rule."""

    pass
