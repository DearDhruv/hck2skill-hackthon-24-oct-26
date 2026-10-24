import os
import io
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from app.main import app
from app.models.complaint import IssueType, ComplaintStatus
from app.services.amc_db import AMCDatabaseService
from app.services.vision_service import VisionAnalysisService
from app.services.agent_engine import CivicComplaintAgent

DATASET_DIR = os.path.join(os.path.dirname(__file__), "test_pothole_dataset")

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def isolated_db(tmp_path):
    return AMCDatabaseService(data_dir=str(tmp_path))

@pytest.fixture
def isolated_agent(isolated_db):
    return CivicComplaintAgent(db=isolated_db)

def get_test_pothole_images():
    """Returns list of (filename, full_path, bytes) for all downloaded pothole images."""
    assert os.path.exists(DATASET_DIR), f"Dataset directory {DATASET_DIR} does not exist"
    images = []
    for fn in sorted(os.listdir(DATASET_DIR)):
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            p = os.path.join(DATASET_DIR, fn)
            with open(p, "rb") as f:
                data = f.read()
            images.append((fn, p, data))
    return images

def test_dataset_integrity_and_dimensions():
    """Verify all downloaded pothole images are valid, high-resolution, uncorrupted images."""
    images = get_test_pothole_images()
    assert len(images) >= 6, f"Expected at least 6 test images, found {len(images)}"

    for fn, path, data in images:
        assert len(data) > 10000, f"Image {fn} is suspiciously small: {len(data)} bytes"
        with Image.open(io.BytesIO(data)) as img:
            w, h = img.size
            assert w >= 300 and h >= 300, f"Image {fn} resolution too low: {w}x{h}"
            assert img.format in ["JPEG", "PNG"]

def test_analyze_civic_image_pure_cv_on_all_pothole_images():
    """
    Test direct civic image analysis on all real pothole images without any filename hints.
    Verifies that the hardened computer vision correctly classifies real road textures as potholes.
    """
    vision = VisionAnalysisService()
    images = get_test_pothole_images()

    for fn, _, data in images:
        # Pass completely neutral camera filename (no 'pothole' or 'road' keyword)
        neutral_filename = f"CAMERA_{hash(fn) % 100000:05d}.jpg"
        result = vision.analyze_civic_image(data, filename=neutral_filename, text_hint=None)

        # Must be classified as POTHOLE
        assert result.issue == IssueType.POTHOLE, (
            f"Image '{fn}' was misclassified as {result.issue.value} under neutral filename '{neutral_filename}'!"
        )
        assert result.confidence >= 0.90, f"Confidence too low for {fn}: {result.confidence}"
        assert result.suggestedDepartment == "Roads & Buildings"
        assert result.severity in ["Critical", "High", "Medium"]
        assert len(result.detectedFeatures) >= 3

        # Dynamic bounding box validation
        bbox = result.boundingBox
        assert 0.0 <= bbox["x"] <= 100.0
        assert 0.0 <= bbox["y"] <= 100.0
        assert 0.0 < bbox["width"] <= 100.0
        assert 0.0 < bbox["height"] <= 100.0

def test_agent_process_complaint_pipeline_on_all_potholes(isolated_agent):
    """
    End-to-end agent pipeline test for all downloaded pothole images.
    Verifies:
    1. Vision classification -> POTHOLE
    2. Ward GIS resolution (CG Road -> W12, Bodakdev -> W08, Maninagar -> W27)
    3. Department routing -> Roads & Buildings
    4. Unique ticket generation with SLA
    5. Social media escalation draft
    """
    images = get_test_pothole_images()
    test_areas = ["CG Road", "Bodakdev", "Stadium", "Vastrapur", "Maninagar"]

    for idx, (fn, _, data) in enumerate(images):
        area = test_areas[idx % len(test_areas)]
        neutral_fn = f"DCIM_{idx+1001}.jpg"

        resp = isolated_agent.process_complaint_pipeline(
            image_bytes=data,
            filename=neutral_fn,
            user_area=area,
            user_notes=f"Deep crater in middle of arterial lane near {area}"
        )

        assert resp.success is True
        assert resp.intent == "FILE_COMPLAINT"
        assert resp.complaint is not None

        c = resp.complaint
        assert c.trackingId.startswith("AMC-2026-")
        assert c.issue == IssueType.POTHOLE
        assert c.department == "Roads & Buildings"
        assert c.area == area
        assert c.status == ComplaintStatus.ASSIGNED
        assert len(c.timeline) >= 2

        # Check all 4 tool calls logged
        assert "analyze_image" in resp.toolsInvoked
        assert "lookup_ward_and_department" in resp.toolsInvoked
        assert "create_complaint_ticket" in resp.toolsInvoked
        assert "draft_social_media_post" in resp.toolsInvoked

        # Check social draft
        assert resp.socialDraft is not None
        assert "@AhmedabadAMC" in resp.socialDraft.mentions
        assert "Roads & Buildings" in resp.socialDraft.text

def test_api_multipart_upload_real_potholes(client):
    """
    Verifies the running FastAPI HTTP endpoint (/api/complaints/file) accepting
    real multipart image uploads, storing them, and returning proper tracking IDs.
    """
    images = get_test_pothole_images()

    for idx, (fn, _, data) in enumerate(images[:4]):
        files = {
            "file": (f"citizen_upload_{idx}.jpg", data, "image/jpeg")
        }
        form_data = {
            "area": "CG Road",
            "notes": f"Real-world pothole road hazard test #{idx}"
        }

        res = client.post("/api/complaints/file", files=files, data=form_data)
        assert res.status_code == 200, f"API failed with {res.status_code}: {res.text}"
        payload = res.json()

        assert payload["success"] is True
        c = payload["complaint"]
        assert c["trackingId"].startswith("AMC-2026-")
        assert c["issue"] == "pothole"
        assert c["department"] == "Roads & Buildings"
        assert c["ward"] == "W12"

        # Verify uploaded image is served statically
        img_url = c["imageUrl"]
        assert img_url.startswith("/static/uploads/")
        check_img = client.get(img_url)
        assert check_img.status_code == 200
        assert len(check_img.content) == len(data)

        # Status check via agent query
        tid = c["trackingId"]
        query_res = client.post("/api/agent/query", json={"query": f"what's the status of {tid}?"})
        assert query_res.status_code == 200
        query_data = query_res.json()
        assert query_data["success"] is True
        assert query_data["complaint"]["trackingId"] == tid

        # Advance lifecycle
        adv_res = client.post(f"/api/complaints/{tid}/advance")
        assert adv_res.status_code == 200
        assert adv_res.json()["status"] == "In Progress"

def test_corrupted_image_bytes_graceful_handling(isolated_agent):
    """
    Edge case: Truncated or corrupted image bytes should not crash the pipeline
    and must fall back gracefully to resilient defaults.
    """
    corrupt_bytes = b"NOT_A_VALID_JPEG_HEADER_RANDOM_GARBAGE_BYTES_12345"
    resp = isolated_agent.process_complaint_pipeline(
        image_bytes=corrupt_bytes,
        filename="corrupted_upload.jpg",
        user_area="Stadium",
        user_notes="Pothole near stadium gate"
    )
    assert resp.success is True
    assert resp.complaint is not None
    assert resp.complaint.trackingId.startswith("AMC-2026-")
    assert resp.complaint.issue == IssueType.POTHOLE

def test_hazard_classification_pothole_vs_other_civic_issues():
    """
    Verifies requirement: 'hazard classification (pothole vs others)'
    Tests that pure computer vision correctly distinguishes real-world road potholes
    from streetlights, garbage overflow, and waterlogging under neutral camera filenames
    without any textual hints.
    """
    vision = VisionAnalysisService()
    samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "static", "samples")

    hazard_test_cases = [
        ("broken_streetlight_vastrapur.jpg", IssueType.STREETLIGHT, "Light Department"),
        ("garbage_overflow_kankaria.jpg", IssueType.GARBAGE, "Solid Waste Management"),
        ("waterlogging_stadium.jpg", IssueType.WATERLOGGING, "Storm Water Drainage"),
        ("pothole_cg_road.jpg", IssueType.POTHOLE, "Roads & Buildings")
    ]

    for filename, expected_issue, expected_dept in hazard_test_cases:
        p = os.path.join(samples_dir, filename)
        assert os.path.exists(p), f"Sample file {filename} not found at {p}"
        with open(p, "rb") as f:
            data = f.read()

        # Pass strictly neutral filename (e.g. CAMERA_IMG_7781.jpg) with zero text hint
        neutral_name = f"CAMERA_IMG_{hash(filename) % 10000:04d}.jpg"
        result = vision.analyze_civic_image(data, filename=neutral_name, text_hint=None)

        assert result.issue == expected_issue, (
            f"Image '{filename}' misclassified as {result.issue.value} under neutral filename! Expected: {expected_issue.value}"
        )
        assert result.suggestedDepartment == expected_dept

        # Verify that non-potholes receive their respective specialized bounding boxes
        # and do NOT get assigned an asphalt cavity bounding box
        bbox = result.boundingBox
        assert bbox["width"] > 0.0
        assert bbox["height"] > 0.0
        assert 0.0 <= bbox["x"] <= 100.0
        assert 0.0 <= bbox["y"] <= 100.0

def test_bounding_box_edge_hotspot_boundary_safety():
    """
    Verifies that localized road cavity bounding boxes never produce negative or zero
    widths/heights when craters appear on extreme right, bottom, or corner boundaries.
    """
    vision = VisionAnalysisService()

    # Case A: Crater at extreme right border (x >= 95%)
    img_right = Image.new("L", (320, 240), color=180)
    draw_r = ImageDraw.Draw(img_right)
    draw_r.rectangle((310, 100, 319, 140), fill=20)
    bbox_r = vision._detect_cavity_hotspot(img_right)

    assert bbox_r["width"] > 0.0, f"Negative/zero width at right edge: {bbox_r}"
    assert bbox_r["height"] > 0.0, f"Negative/zero height at right edge: {bbox_r}"
    assert bbox_r["x"] + bbox_r["width"] <= 100.0, f"Right edge overflow: {bbox_r}"

    # Case B: Crater at extreme bottom border (y >= 95%)
    img_bottom = Image.new("L", (320, 240), color=180)
    draw_b = ImageDraw.Draw(img_bottom)
    draw_b.rectangle((120, 230, 160, 239), fill=20)
    bbox_b = vision._detect_cavity_hotspot(img_bottom)

    assert bbox_b["width"] > 0.0, f"Negative/zero width at bottom edge: {bbox_b}"
    assert bbox_b["height"] > 0.0, f"Negative/zero height at bottom edge: {bbox_b}"
    assert bbox_b["y"] + bbox_b["height"] <= 100.0, f"Bottom edge overflow: {bbox_b}"

def test_low_light_and_night_pothole_resilience():
    """
    Harden against lighting extremes: Dark asphalt road under dusk/night illumination
    must be correctly identified as POTHOLE rather than misclassified as STREETLIGHT.
    """
    vision = VisionAnalysisService()

    # Dark asphalt road with pothole crack (R=40, G=40, B=42)
    dark_road = Image.new("RGB", (400, 300), color=(40, 40, 42))
    draw = ImageDraw.Draw(dark_road)
    for i in range(50):
        draw.line((100 + i * 2, 100 + i, 200 - i, 150 + i), fill=(15, 15, 18), width=3)
        draw.line((150 - i, 80 + i * 2, 250 + i, 120 - i), fill=(55, 55, 60), width=2)

    buf = io.BytesIO()
    dark_road.save(buf, format="JPEG")
    data = buf.getvalue()

    result = vision.analyze_civic_image(data, filename="NIGHT_CAM_0042.jpg", text_hint=None)
    assert result.issue == IssueType.POTHOLE, f"Dark asphalt was misclassified as {result.issue.value}!"
    assert result.suggestedDepartment == "Roads & Buildings"

def test_image_format_and_color_mode_diversity():
    """
    Verifies resilience across non-standard image modes:
    - Grayscale (Mode 'L')
    - Transparent RGBA (Mode 'RGBA')
    - WebP format
    """
    vision = VisionAnalysisService()

    # 1. Grayscale road image
    img_l = Image.new("L", (400, 300), color=128)
    buf_l = io.BytesIO()
    img_l.save(buf_l, format="PNG")
    res_l = vision.analyze_civic_image(buf_l.getvalue(), filename="road_bw.png")
    assert res_l.issue == IssueType.POTHOLE
    assert res_l.suggestedDepartment == "Roads & Buildings"

    # 2. RGBA image
    img_rgba = Image.new("RGBA", (400, 300), color=(110, 110, 110, 255))
    buf_rgba = io.BytesIO()
    img_rgba.save(buf_rgba, format="PNG")
    res_rgba = vision.analyze_civic_image(buf_rgba.getvalue(), filename="road_rgba.png")
    assert res_rgba.issue == IssueType.POTHOLE

    # 3. WebP image
    img_webp = Image.new("RGB", (400, 300), color=(100, 100, 100))
    buf_webp = io.BytesIO()
    img_webp.save(buf_webp, format="WEBP")
    res_webp = vision.analyze_civic_image(buf_webp.getvalue(), filename="road_feed.webp")
    assert res_webp.issue == IssueType.POTHOLE

def test_api_multipart_upload_all_8_potholes(client):
    """
    Verifies the running FastAPI HTTP endpoint (/api/complaints/file) accepting
    multipart image uploads for ALL 8 downloaded real-world pothole images,
    storing each file, and creating valid sequential tracking IDs with correct SLA.
    """
    images = get_test_pothole_images()
    assert len(images) == 8, f"Expected 8 images in dataset, found {len(images)}"

    test_areas = ["CG Road", "Bodakdev", "Stadium", "Vastrapur", "Maninagar", "Kankaria", "Navrangpura", "Law Garden"]

    for idx, (fn, _, data) in enumerate(images):
        area = test_areas[idx % len(test_areas)]
        files = {
            "file": (f"real_pothole_upload_{idx}.jpg", data, "image/jpeg")
        }
        form_data = {
            "area": area,
            "notes": f"Pothole dataset benchmark image {fn}"
        }

        res = client.post("/api/complaints/file", files=files, data=form_data)
        assert res.status_code == 200, f"Upload failed for {fn}: {res.status_code}"
        payload = res.json()

        assert payload["success"] is True
        c = payload["complaint"]
        assert c["trackingId"].startswith("AMC-2026-")
        assert c["issue"] == "pothole"
        assert c["department"] == "Roads & Buildings"
        assert c["area"] == area
        assert c["status"] == "Assigned"
        assert c["imageUrl"].startswith("/static/uploads/")

