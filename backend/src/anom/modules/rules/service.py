"""Application services exposing rule operations."""
from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from anom.modules.business_def.domain import BusinessNotFoundError
from anom.modules.business_def.service import BusinessService
from anom.modules.rules.domain import RuleCreate, RuleDefinition, RuleNotFoundError
from anom.modules.rules.repo import RuleRepository


class RuleService:
    """Coordinates rule validation and storage."""

    def __init__(self, repository: RuleRepository, business_service: BusinessService) -> None:
        self._repository = repository
        self._business_service = business_service

    def create_rule(self, business_id: UUID, payload: RuleCreate) -> RuleDefinition:
        # ensure business exists
        self._business_service.get_business(business_id)
        rule = RuleDefinition(
            id=uuid4(),
            business_id=business_id,
            name=payload.name,
            description=payload.description,
            condition=payload.condition,
            severity=payload.severity,
            created_at=datetime.utcnow(),
        )
        return self._repository.add_rule(rule)

    def list_rules(self, business_id: UUID) -> List[RuleDefinition]:
        # ensure business exists
        self._business_service.get_business(business_id)
        return self._repository.list_rules(business_id)

    def get_rule(self, business_id: UUID, rule_id: UUID) -> RuleDefinition:
        rule = self._repository.get_rule(business_id, rule_id)
        if rule is None:
            raise RuleNotFoundError(str(rule_id))
        return rule


__all__ = ["RuleService", "RuleCreate", "RuleDefinition", "RuleNotFoundError", "BusinessNotFoundError"]
