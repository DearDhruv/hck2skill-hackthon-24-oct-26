import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_index(client):
    res = client.get("/")
    assert res.status_code == 200

def test_api_get_wards(client):
    res = client.get("/api/wards")
    assert res.status_code == 200
    wards = res.json()
    assert len(wards) >= 2
    assert any(w["id"] == "W12" for w in wards)

def test_api_get_complaints(client):
    res = client.get("/api/complaints")
    assert res.status_code == 200
    complaints = res.json()
    assert len(complaints) >= 1

def test_api_file_sample_complaint(client):
    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "Stadium",
        "notes": "FastAPI integration test crater"
    }
    res = client.post("/api/complaints/file", data=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["intent"] == "FILE_COMPLAINT"
    assert data["complaint"]["trackingId"].startswith("AMC-2026-")
    assert data["complaint"]["ward"] == "W12"
    assert data["complaint"]["department"] == "Roads & Buildings"
    assert len(data["reasoningTrace"]) >= 4

def test_api_status_query(client):
    res = client.post("/api/agent/query", json={"query": "what's the status of AMC-2026-000123?"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["complaint"]["trackingId"] == "AMC-2026-000123"

def test_api_advance_lifecycle(client):
    # First file a complaint
    file_res = client.post("/api/complaints/file", data={"sampleName": "waterlogging_stadium.jpg", "area": "Stadium"})
    tid = file_res.json()["complaint"]["trackingId"]

    adv_res = client.post(f"/api/complaints/{tid}/advance")
    assert adv_res.status_code == 200
    assert adv_res.json()["status"] == "In Progress"

def test_api_video_scan(client):
    res = client.post("/api/video/scan")
    assert res.status_code == 200
    data = res.json()
    assert data["totalFramesSampled"] == 5
    assert data["totalHazardsDetected"] >= 2

def test_api_reset_seed(client):
    res = client.post("/api/admin/reset")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_api_404_handling(client):
    res = client.get("/api/complaints/AMC-2026-NONEXISTENT")
    assert res.status_code == 404
