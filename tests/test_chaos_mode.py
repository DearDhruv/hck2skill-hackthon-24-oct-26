import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.chaos_service import (
    ChaosService,
    FaultType,
    MunicipalDatabaseCrashError,
    JurisdictionUnresolvedError,
    ChaosException
)
from app.services.amc_db import AMCDatabaseService


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_chaos_state():
    """Ensures chaos mode is safely reset and disabled before and after each test."""
    chaos = ChaosService.get_instance()
    chaos.disable()
    yield
    chaos.disable()


def test_chaos_status_defaults(client):
    """Verifies default chaos engine status and 6 registered fault profiles."""
    res = client.get("/api/chaos")
    assert res.status_code == 200
    data = res.json()
    assert data["enabled"] is False
    assert data["activeFault"] == "500_INTERNAL_ERROR"
    assert len(data["availableFaults"]) == 6

    expected_ids = {
        "500_INTERNAL_ERROR",
        "NETWORK_TIMEOUT",
        "RATE_LIMIT_429",
        "CORRUPTED_PAYLOAD",
        "JURISDICTION_UNRESOLVED",
        "CORRUPTED_IMAGE_UPLOAD"
    }
    actual_ids = {f["id"] for f in data["availableFaults"]}
    assert expected_ids == actual_ids


def test_chaos_toggle_endpoints(client):
    """Verifies POST /api/chaos/toggle enables, switches faults, and disables cleanly."""
    # Enable with default fault
    res1 = client.post("/api/chaos/toggle", json={"enabled": True})
    assert res1.status_code == 200
    assert res1.json()["enabled"] is True

    # Switch to RATE_LIMIT_429 and override timeout
    res2 = client.post("/api/chaos/toggle", json={"faultType": "RATE_LIMIT_429", "timeoutSeconds": 1.5})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["enabled"] is True
    assert data2["activeFault"] == "RATE_LIMIT_429"
    assert data2["timeoutSeconds"] == 1.5

    # Toggle off
    res3 = client.post("/api/chaos/toggle", json={"enabled": False})
    assert res3.status_code == 200
    assert res3.json()["enabled"] is False


def test_fault_500_internal_error(client):
    """Verifies Fault 1: 500_INTERNAL_ERROR triggers municipal database crash in API and service."""
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "500_INTERNAL_ERROR"})

    # Test API endpoint response
    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Stadium",
        "notes": "Chaos testing DB crash"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 500
    data = res.json()
    assert data["error"] is True
    assert data["chaosFault"] == "500_INTERNAL_ERROR"
    assert "Simulated AMC Municipal Database Crash" in data["detail"]

    # Test direct amc_db service integration
    db = AMCDatabaseService.get_instance()
    with pytest.raises(MunicipalDatabaseCrashError):
        db.list_complaints()


def test_fault_network_timeout(client):
    """Verifies Fault 2: NETWORK_TIMEOUT triggers 504 gateway timeout."""
    # Use small timeout for rapid test execution
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "NETWORK_TIMEOUT", "timeoutSeconds": 0.05})

    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Stadium"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 504
    data = res.json()
    assert data["error"] is True
    assert data["chaosFault"] == "NETWORK_TIMEOUT"
    assert "Municipal Gateway Timeout" in data["detail"]


def test_fault_rate_limit_429(client):
    """Verifies Fault 3: RATE_LIMIT_429 triggers 429 Too Many Requests with Retry-After header."""
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "RATE_LIMIT_429"})

    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Stadium"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 429
    assert res.headers.get("retry-after") == "60"
    data = res.json()
    assert data["error"] is True
    assert data["chaosFault"] == "RATE_LIMIT_429"
    assert "Rate Limit Exceeded" in data["detail"]


def test_fault_corrupted_payload(client):
    """Verifies Fault 4: CORRUPTED_PAYLOAD returns malformed non-JSON response payload."""
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "CORRUPTED_PAYLOAD"})

    # 1. Test complaint filing endpoint
    res1 = client.post("/api/complaints/file", data={"sampleName": "pothole_cg_road.jpg"})
    assert res1.status_code == 200
    assert b"<<<ERR_AMC_MUNICIPAL_CORRUPT_PAYLOAD" in res1.content
    with pytest.raises(Exception):
        res1.json()

    # 2. Test status query endpoint
    res2 = client.post("/api/agent/query", json={"query": "what's the status of AMC-2026-000123?"})
    assert res2.status_code == 200
    assert b"<<<ERR_AMC_MUNICIPAL_CORRUPT_PAYLOAD" in res2.content
    with pytest.raises(Exception):
        res2.json()


def test_fault_jurisdiction_unresolved(client):
    """Verifies Fault 5: JURISDICTION_UNRESOLVED triggers boundary dispute error in API & DB."""
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "JURISDICTION_UNRESOLVED"})

    # Test API endpoint
    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Disputed Border Buffer Zone"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 422
    data = res.json()
    assert data["error"] is True
    assert data["chaosFault"] == "JURISDICTION_UNRESOLVED"
    assert "Municipal GIS Boundary Discrepancy" in data["detail"]

    # Test direct amc_db service integration
    db = AMCDatabaseService.get_instance()
    with pytest.raises(JurisdictionUnresolvedError):
        db.find_ward_by_area("Navrangpura")


def test_fault_corrupted_image_upload(client):
    """Verifies Fault 6: CORRUPTED_IMAGE_UPLOAD triggers 400 unreadable image buffer error."""
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "CORRUPTED_IMAGE_UPLOAD"})

    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Stadium"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 400
    data = res.json()
    assert data["error"] is True
    assert data["chaosFault"] == "CORRUPTED_IMAGE_UPLOAD"
    assert "Corrupted Image Upload" in data["detail"]


def test_chaos_instant_recovery(client):
    """Verifies that turning chaos mode off immediately restores 100% normal functioning."""
    # 1. Break system with 500 error
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "500_INTERNAL_ERROR"})
    res_broken = client.post("/api/complaints/file", data={"sampleName": "pothole_cg_road.jpg", "area": "Stadium"})
    assert res_broken.status_code == 500

    # 2. 1-Click instant recovery: Disable chaos mode
    res_disable = client.post("/api/chaos/toggle", json={"enabled": False})
    assert res_disable.status_code == 200
    assert res_disable.json()["enabled"] is False

    # 3. Repeat request: Must succeed with 200 and registered complaint
    res_recovered = client.post("/api/complaints/file", data={"sampleName": "pothole_cg_road.jpg", "area": "Stadium"})
    assert res_recovered.status_code == 200
    data = res_recovered.json()
    assert data["success"] is True
    assert data["complaint"]["trackingId"].startswith("AMC-2026-")


def test_status_query_under_chaos(client):
    """Verifies conversational query endpoint also adheres to chaos state."""
    # Active 500 fault
    client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "500_INTERNAL_ERROR"})
    res = client.post("/api/agent/query", json={"query": "what's the status of 123?"})
    assert res.status_code == 500

    # Recover
    client.post("/api/chaos/toggle", json={"enabled": False})
    res_ok = client.post("/api/agent/query", json={"query": "what's the status of 123?"})
    assert res_ok.status_code == 200
    assert res_ok.json()["success"] is True


def test_invalid_fault_type_returns_400(client):
    """Verifies that attempting to set an unknown fault returns HTTP 400."""
    res = client.post("/api/chaos/toggle", json={"faultType": "NON_EXISTENT_EXPLOSION"})
    assert res.status_code == 400
    assert "Unknown fault type" in res.json()["detail"]


def test_empty_toggle_flips_state(client):
    """Verifies that calling /api/chaos/toggle with no body flips state."""
    res1 = client.post("/api/chaos/toggle")
    assert res1.status_code == 200
    assert res1.json()["enabled"] is True

    res2 = client.post("/api/chaos/toggle")
    assert res2.status_code == 200
    assert res2.json()["enabled"] is False


def test_index_contains_chaos_controls(client):
    """Verifies index.html renders the Chaos Testing controls and ErrorStateCard."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text
    assert 'id="btn-toggle-chaos"' in html
    assert 'id="chaos-fault-select"' in html
    assert 'id="error-state-card"' in html
    assert 'id="chaos-alert-banner"' in html
    assert 'id="btn-err-self-heal"' in html


def test_concurrent_chaos_toggles(client):
    """Verifies thread-safe chaos operations under concurrent requests."""
    from concurrent.futures import ThreadPoolExecutor

    def toggle_op(i):
        if i % 2 == 0:
            client.post("/api/chaos/toggle", json={"enabled": True, "faultType": "500_INTERNAL_ERROR"})
        else:
            client.post("/api/chaos/toggle", json={"enabled": False})
        return client.get("/api/chaos").status_code

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(toggle_op, range(20)))

    assert all(code == 200 for code in results)
