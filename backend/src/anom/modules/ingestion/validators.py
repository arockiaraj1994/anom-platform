"""Utility helpers to validate and normalize incoming events."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException, status

from anom.modules.business_def.domain import FieldDataType, FieldDefinition

_TYPE_CASTERS: Dict[FieldDataType, Any] = {
    FieldDataType.STRING: str,
    FieldDataType.INTEGER: int,
    FieldDataType.FLOAT: float,
    FieldDataType.BOOLEAN: bool,
    FieldDataType.DATETIME: datetime,
}


def _coerce_value(value: Any, data_type: FieldDataType) -> Any:
    if data_type is FieldDataType.STRING:
        if isinstance(value, str):
            return value
        raise TypeError("expected string")
    if data_type is FieldDataType.INTEGER:
        if isinstance(value, bool):  # pragma: no cover - defensive
            raise TypeError("boolean is not a valid integer")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise TypeError("expected integer") from exc
    if data_type is FieldDataType.FLOAT:
        try:
            return float(value)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise TypeError("expected float") from exc
    if data_type is FieldDataType.BOOLEAN:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.lower()
            if lowered in {"true", "1", "yes"}:
                return True
            if lowered in {"false", "0", "no"}:
                return False
        raise TypeError("expected boolean")
    if data_type is FieldDataType.DATETIME:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError as exc:  # pragma: no cover - defensive
                raise TypeError("expected ISO datetime string") from exc
        raise TypeError("expected datetime")
    raise TypeError(f"unsupported data type {data_type!s}")


def normalize_payload(
    payload: Dict[str, Any],
    field_definitions: list[FieldDefinition],
) -> Dict[str, Any]:
    """Validate payload against schema and return normalized data."""

    normalized: Dict[str, Any] = {}
    defined_fields = {field.name: field for field in field_definitions}

    for field in field_definitions:
        if field.required and field.name not in payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field '{field.name}'",
            )

    for key, value in payload.items():
        field = defined_fields.get(key)
        if not field:
            # allow additional properties for now
            normalized[key] = value
            continue
        try:
            normalized[key] = _coerce_value(value, field.data_type)
        except TypeError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{key}' expects {_TYPE_CASTERS[field.data_type].__name__}",
            ) from exc
    return normalized
