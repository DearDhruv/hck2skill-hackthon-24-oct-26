import os
import io
import pytest
from concurrent.futures import ThreadPoolExecutor
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
    assert any(w["id"] == "W27" for w in wards)

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

def test_api_file_real_upload_and_persistence(client):
    """
    Verifies that uploading a real citizen image actually writes the file to disk
    and returns a valid, statically accessible imageUrl without 404 errors.
    """
    dummy_bytes = b"fake_png_header_and_citizen_photo_payload_bytes_12345"
    files = {
        "file": ("citizen_hazard_test.jpg", dummy_bytes, "image/jpeg")
    }
    data = {
        "area": "Kankaria",
        "notes": "Piles of trash near lakeside walkway"
    }
    res = client.post("/api/complaints/file", files=files, data=data)
    assert res.status_code == 200
    resp_data = res.json()
    assert resp_data["success"] is True
    c = resp_data["complaint"]
    img_url = c["imageUrl"]
    assert img_url.startswith("/static/uploads/")

    # Verify static file is actually served and reachable
    img_res = client.get(img_url)
    assert img_res.status_code == 200
    assert img_res.content == dummy_bytes

def test_api_status_query(client):
    res = client.post("/api/agent/query", json={"query": "what's the status of AMC-2026-000123?"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["complaint"]["trackingId"] == "AMC-2026-000123"

def test_api_status_query_number_variations(client):
    # Short query "what is the status of 124?"
    res1 = client.post("/api/agent/query", json={"query": "what is the status of 124?"})
    assert res1.status_code == 200
    assert res1.json()["complaint"]["trackingId"] == "AMC-2026-000124"

    # Short prefix "AMC-125"
    res2 = client.post("/api/agent/query", json={"query": "status AMC-125"})
    assert res2.status_code == 200
    assert res2.json()["complaint"]["trackingId"] == "AMC-2026-000125"

def test_api_advance_lifecycle(client):
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
    for det in data["detections"]:
        assert det["frameImageUrl"] is not None

def test_api_reset_seed(client):
    res = client.post("/api/admin/reset")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_api_404_handling(client):
    res = client.get("/api/complaints/AMC-2026-NONEXISTENT")
    assert res.status_code == 404

def test_api_concurrent_filings(client):
    """
    Stress test verifying thread safety and unique ID generation under concurrent requests.
    """
    def file_one(idx):
        payload = {
            "sampleName": "pothole_cg_road.jpg",
            "area": "Stadium",
            "notes": f"Concurrent filing test #{idx}"
        }
        res = client.post("/api/complaints/file", data=payload)
        return res.json()["complaint"]["trackingId"]

    with ThreadPoolExecutor(max_workers=4) as executor:
        tracking_ids = list(executor.map(file_one, range(4)))

    assert len(tracking_ids) == 4
    # All IDs must be unique
    assert len(set(tracking_ids)) == 4


def test_api_authority_contact_affordances(client):
    """
    Verifies that municipal complaint responses supply complete, actionable authority contact affordances:
    - Ward officer name & direct contact phone (tel:)
    - Physical ward office address
    - AMC 24x7 Helpline (155303) & Toll-Free (1800-233-2330)
    - WhatsApp Grievance Desk
    - Department Lead Engineer & escalation hotline/email
    """
    # 1. Test via filing
    payload = {
        "sampleName": "pothole_cg_road.jpg",
        "area": "CG Road",
        "notes": "Testing authority contact links"
    }
    file_res = client.post("/api/complaints/file", data=payload)
    assert file_res.status_code == 200
    c_filed = file_res.json()["complaint"]
    assert c_filed["ward"] == "W12"
    assert c_filed["wardOfficer"] == "Shri Arvind Trivedi"
    assert c_filed["wardContactPhone"] == "+91-79-2755-1201"
    assert "Usmanpura" in c_filed["wardOfficeAddress"]
    assert c_filed["leadEngineer"] == "Er. Rajesh Dave"
    assert c_filed["departmentHotline"] == "+91-79-2755-1234"
    assert c_filed["amcHelpline"] == "155303"
    assert c_filed["tollFreeHelpline"] == "1800-233-2330"
    assert c_filed["whatsappGrievance"] == "+91-99783-22880"

    # 2. Test via status query
    tid = c_filed["trackingId"]
    query_res = client.post("/api/agent/query", json={"query": f"what's the status of {tid}?"})
    assert query_res.status_code == 200
    q_data = query_res.json()
    assert q_data["complaint"]["wardOfficer"] == "Shri Arvind Trivedi"
    assert "155303" in q_data["message"]
    assert "Shri Arvind Trivedi" in q_data["message"]

    # 3. Test via GET single complaint
    get_res = client.get(f"/api/complaints/{tid}")
    assert get_res.status_code == 200
    c_get = get_res.json()
    assert c_get["wardOfficer"] == "Shri Arvind Trivedi"
    assert c_get["wardContactPhone"] == "+91-79-2755-1201"

    # 4. Test seed complaint (W27 - Maninagar)
    seed_res = client.get("/api/complaints/AMC-2026-000124")
    assert seed_res.status_code == 200
    c_seed = seed_res.json()
    assert c_seed["ward"] == "W27"
    assert c_seed["wardOfficer"] == "Smt. Bhavna Solanki"
    assert c_seed["wardContactPhone"] == "+91-79-2546-4301"
    assert "Rambaug" in c_seed["wardOfficeAddress"]
    assert c_seed["leadEngineer"] == "Er. Minaxi Patel"
    assert c_seed["departmentHotline"] == "+91-79-2755-5678"

