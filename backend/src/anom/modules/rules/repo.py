"""In-memory repository for rule definitions."""
from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from anom.modules.rules.domain import RuleDefinition


class RuleRepository:
    """Stores rules keyed by their parent business."""

    def __init__(self) -> None:
        self._rules: Dict[UUID, Dict[UUID, RuleDefinition]] = {}

    def add_rule(self, rule: RuleDefinition) -> RuleDefinition:
        rules_for_business = self._rules.setdefault(rule.business_id, {})
        rules_for_business[rule.id] = rule
        return rule.model_copy()

    def list_rules(self, business_id: UUID) -> List[RuleDefinition]:
        rules = self._rules.get(business_id, {})
        return [r.model_copy() for r in rules.values()]

    def get_rule(self, business_id: UUID, rule_id: UUID) -> Optional[RuleDefinition]:
        rule = self._rules.get(business_id, {}).get(rule_id)
        return rule.model_copy() if rule else None

    def all_rules(self) -> List[RuleDefinition]:
        return [rule.model_copy() for rules in self._rules.values() for rule in rules.values()]

    def clear(self) -> None:
        self._rules.clear()
