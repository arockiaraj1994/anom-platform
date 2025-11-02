"""Dependency wiring for FastAPI endpoints."""
from __future__ import annotations

from functools import lru_cache

from anom.modules.alerts.repo import AlertRepository
from anom.modules.alerts.service import AlertService
from anom.modules.business_def.repo import BusinessRepository
from anom.modules.business_def.service import BusinessService
from anom.modules.ingestion.repo import EventRepository
from anom.modules.ingestion.service import IngestionService
from anom.modules.rule_engine.dispatcher import RuleDispatcher
from anom.modules.rules.repo import RuleRepository
from anom.modules.rules.service import RuleService


@lru_cache()
def get_business_repository() -> BusinessRepository:
    return BusinessRepository()


@lru_cache()
def get_rule_repository() -> RuleRepository:
    return RuleRepository()


@lru_cache()
def get_alert_repository() -> AlertRepository:
    return AlertRepository()


@lru_cache()
def get_event_repository() -> EventRepository:
    return EventRepository()


@lru_cache()
def get_business_service() -> BusinessService:
    return BusinessService(get_business_repository())


@lru_cache()
def get_rule_service() -> RuleService:
    return RuleService(get_rule_repository(), get_business_service())


@lru_cache()
def get_alert_service() -> AlertService:
    return AlertService(get_alert_repository())


@lru_cache()
def get_rule_dispatcher() -> RuleDispatcher:
    return RuleDispatcher(get_rule_repository())


@lru_cache()
def get_ingestion_service() -> IngestionService:
    return IngestionService(
        get_business_service(),
        get_event_repository(),
        get_rule_dispatcher(),
        get_alert_service(),
    )


__all__ = [
    "get_business_service",
    "get_rule_service",
    "get_ingestion_service",
    "get_alert_service",
]
