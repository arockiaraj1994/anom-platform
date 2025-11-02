"""Helpers for evaluating rules against events."""
from __future__ import annotations

from typing import Any, Callable, Dict

from anom.modules.rules.domain import RuleCondition, RuleDefinition, RuleOperator

_OPERATOR_FUNCS: Dict[RuleOperator, Callable[[Any, Any], bool]] = {
    RuleOperator.EQ: lambda left, right: left == right,
    RuleOperator.NE: lambda left, right: left != right,
    RuleOperator.GT: lambda left, right: left > right,
    RuleOperator.GTE: lambda left, right: left >= right,
    RuleOperator.LT: lambda left, right: left < right,
    RuleOperator.LTE: lambda left, right: left <= right,
}


def evaluate_rule(rule: RuleDefinition, payload: Dict[str, Any]) -> bool:
    """Return True if the rule condition matches the event payload."""

    condition: RuleCondition = rule.condition
    if condition.field not in payload:
        return False
    comparator = _OPERATOR_FUNCS[condition.operator]
    try:
        return comparator(payload[condition.field], condition.value)
    except TypeError:  # pragma: no cover - defensive
        return False


__all__ = ["evaluate_rule"]
