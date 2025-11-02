from fastapi.testclient import TestClient
import pytest

from anom.api import deps
from anom.api.main_app import create_app
from anom.modules.rules.domain import RuleOperator, SeverityLevel


@pytest.fixture()
def client() -> TestClient:
    deps.get_ingestion_service.cache_clear()
    deps.get_alert_service.cache_clear()
    deps.get_rule_service.cache_clear()
    deps.get_business_service.cache_clear()
    deps.get_event_repository.cache_clear()
    deps.get_alert_repository.cache_clear()
    deps.get_rule_repository.cache_clear()
    deps.get_business_repository.cache_clear()
    app = create_app()
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        test_client.close()


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_business_rule_and_ingestion_flow(client: TestClient):
    business_resp = client.post(
        "/businesses/",
        json={"name": "Test Business", "description": "Demo"},
    )
    assert business_resp.status_code == 201
    business_id = business_resp.json()["id"]

    field_resp = client.post(
        f"/businesses/{business_id}/fields",
        json={"name": "durationMs", "data_type": "integer", "required": True},
    )
    assert field_resp.status_code == 201

    rule_resp = client.post(
        f"/rules/{business_id}",
        json={
            "name": "Slow duration",
            "description": "Flag slow events",
            "severity": SeverityLevel.WARNING.value,
            "condition": {
                "field": "durationMs",
                "operator": RuleOperator.GT.value,
                "value": 5000,
            },
        },
    )
    assert rule_resp.status_code == 201

    ok_event = client.post(
        f"/ingest/{business_id}",
        json={"payload": {"durationMs": 1200}},
    )
    assert ok_event.status_code == 200
    assert ok_event.json()["alerts"] == []

    slow_event = client.post(
        f"/ingest/{business_id}",
        json={"payload": {"durationMs": 7200}},
    )
    assert slow_event.status_code == 200
    assert slow_event.json()["alerts"] == ["Rule 'Slow duration' triggered"]

    alerts_resp = client.get("/alerts/")
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    assert len(alerts) == 1
    alert_id = alerts[0]["id"]
    assert alerts[0]["status"] == "open"

    ack_resp = client.post(
        f"/alerts/{alert_id}/ack",
        json={"actor": "tester"},
    )
    assert ack_resp.status_code == 200
    assert ack_resp.json()["status"] == "acked"

    events_resp = client.get(f"/ingest/{business_id}")
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]
    assert len(events) == 2
    assert {event["payload"]["durationMs"] for event in events} == {1200, 7200}


def test_ingestion_missing_required_field_returns_error(client: TestClient):
    business_resp = client.post(
        "/businesses/",
        json={"name": "Required Field Biz"},
    )
    business_id = business_resp.json()["id"]

    client.post(
        f"/businesses/{business_id}/fields",
        json={"name": "amount", "data_type": "float", "required": True},
    )

    error_resp = client.post(
        f"/ingest/{business_id}",
        json={"payload": {}},
    )
    assert error_resp.status_code == 400
    assert "Missing required field" in error_resp.json()["detail"]
