"""Coordinates rule evaluation for incoming events."""
from __future__ import annotations

from typing import List
from uuid import UUID

from anom.modules.ingestion.domain import EventRecord
from anom.modules.rule_engine.evaluator import evaluate_rule
from anom.modules.rules.domain import RuleDefinition
from anom.modules.rules.repo import RuleRepository


class RuleDispatcher:
    """Fetches rules for a business and evaluates them against events."""

    def __init__(self, repository: RuleRepository) -> None:
        self._repository = repository

    def evaluate_event(self, business_id: UUID, event: EventRecord) -> List[RuleDefinition]:
        triggered: List[RuleDefinition] = []
        for rule in self._repository.list_rules(business_id):
            if evaluate_rule(rule, event.payload):
                triggered.append(rule)
        return triggered


__all__ = ["RuleDispatcher"]
