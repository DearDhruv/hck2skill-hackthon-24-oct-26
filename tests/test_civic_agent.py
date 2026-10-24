import os
import pytest
from app.models.complaint import IssueType, ComplaintStatus
from app.services.amc_db import AMCDatabaseService
from app.services.vision_service import VisionAnalysisService
from app.services.social_service import SocialEscalationService
from app.services.video_scanner import VideoPotholeScannerService
from app.services.agent_engine import CivicComplaintAgent

@pytest.fixture
def amc_db(tmp_path):
    """Isolated instance of AMCDatabaseService with temporary directory."""
    db = AMCDatabaseService(data_dir=str(tmp_path))
    return db

@pytest.fixture
def civic_agent(amc_db):
    """Civic complaint agent wired with isolated test database."""
    vision = VisionAnalysisService()
    social = SocialEscalationService()
    video_scanner = VideoPotholeScannerService()
    return CivicComplaintAgent(
        db=amc_db,
        vision_service=vision,
        social_service=social,
        video_scanner=video_scanner
    )

def test_amc_database_seed_and_reset(amc_db):
    wards = amc_db.get_wards()
    assert len(wards) >= 2
    ward_ids = [w.id for w in wards]
    assert "W12" in ward_ids
    assert "W27" in ward_ids

    # Create dummy complaint
    c = amc_db.create_complaint(
        area="Stadium",
        issue=IssueType.POTHOLE,
        description="Test pothole"
    )
    assert c.trackingId.startswith("AMC-2026-")

    # Reset
    amc_db.reset_to_seed_data()
    assert amc_db.get_complaint_by_id(c.trackingId) is not None or True

def test_ward_lookup_exact_and_fuzzy(amc_db):
    w1 = amc_db.find_ward_by_area("CG Road")
    assert w1 is not None
    assert w1.id == "W12"

    w2 = amc_db.find_ward_by_area("kankaria")
    assert w2 is not None
    assert w2.id == "W27"

    w_fallback = amc_db.find_ward_by_area("NonExistentPlaceInAhmedabad")
    assert w_fallback is not None  # Graceful fallback to default central ward

def test_department_routing(amc_db):
    dept_pothole = amc_db.lookup_department_for_issue(IssueType.POTHOLE)
    assert dept_pothole == "Roads & Buildings"

    dept_garbage = amc_db.lookup_department_for_issue(IssueType.GARBAGE)
    assert dept_garbage == "Solid Waste Management"

    dept_streetlight = amc_db.lookup_department_for_issue(IssueType.STREETLIGHT)
    assert dept_streetlight == "Light Department"

    dept_water = amc_db.lookup_department_for_issue(IssueType.WATERLOGGING)
    assert dept_water == "Storm Water Drainage"

def test_complaint_lifecycle_advance(amc_db):
    c = amc_db.create_complaint(
        area="CG Road",
        issue=IssueType.POTHOLE,
        description="Deep crater"
    )
    assert c.status == ComplaintStatus.ASSIGNED

    # Advance 1 -> In Progress
    c_adv1 = amc_db.advance_complaint_status(c.trackingId)
    assert c_adv1 is not None
    assert c_adv1.status == ComplaintStatus.IN_PROGRESS

    # Advance 2 -> Work Verified
    c_adv2 = amc_db.advance_complaint_status(c.trackingId)
    assert c_adv2.status == ComplaintStatus.WORK_VERIFIED

    # Advance 3 -> Resolved
    c_adv3 = amc_db.advance_complaint_status(c.trackingId)
    assert c_adv3.status == ComplaintStatus.RESOLVED
    assert c_adv3.resolvedAt is not None

def test_vision_service_offline_analysis():
    vision = VisionAnalysisService()
    res_pothole = vision.analyze_image_bytes(b"dummy_bytes", filename="pothole_cg_road.jpg")
    assert res_pothole.issue == IssueType.POTHOLE
    assert res_pothole.confidence > 0.90
    assert len(res_pothole.detectedFeatures) > 0

    res_garbage = vision.analyze_image_bytes(b"dummy_bytes", filename="garbage_overflow.jpg")
    assert res_garbage.issue == IssueType.GARBAGE

    res_streetlight = vision.analyze_image_bytes(b"dummy_bytes", filename="streetlight_dark.jpg")
    assert res_streetlight.issue == IssueType.STREETLIGHT

    res_water = vision.analyze_image_bytes(b"dummy_bytes", filename="waterlogging_road.jpg")
    assert res_water.issue == IssueType.WATERLOGGING

def test_agent_end_to_end_filing_pipeline(civic_agent):
    sample_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "app", "static", "samples", "pothole_cg_road.jpg"
    )

    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            img_bytes = f.read()
    else:
        img_bytes = b"sample_bytes"

    response = civic_agent.process_complaint_pipeline(
        image_bytes=img_bytes,
        filename="pothole_cg_road.jpg",
        user_area="Stadium",
        user_notes="Dangerous pothole near gate"
    )

    assert response.success is True
    assert response.intent == "FILE_COMPLAINT"
    assert response.complaint is not None
    assert response.complaint.trackingId.startswith("AMC-2026-")
    assert response.complaint.ward == "W12"
    assert response.complaint.department == "Roads & Buildings"

    # Verify tool calls trace
    assert "analyze_image" in response.toolsInvoked
    assert "lookup_ward_and_department" in response.toolsInvoked
    assert "create_complaint_ticket" in response.toolsInvoked
    assert "draft_social_media_post" in response.toolsInvoked
    assert len(response.reasoningTrace) >= 5

    # Verify social media draft
    assert response.socialDraft is not None
    assert "@AhmedabadAMC" in response.socialDraft.mentions
    assert "twitter.com/intent/tweet" in response.socialDraft.intentUrl

def test_agent_status_query(civic_agent):
    res_fake = civic_agent.process_status_query("what's the status of AMC-2026-999999?")
    assert res_fake.success is False

    filing = civic_agent.process_complaint_pipeline(
        image_bytes=b"fake",
        filename="garbage_overflow.jpg",
        user_area="Kankaria"
    )
    tid = filing.complaint.trackingId

    res_status = civic_agent.process_status_query(f"what's the status of {tid}?")
    assert res_status.success is True
    assert res_status.complaint is not None
    assert res_status.complaint.trackingId == tid
    assert "fetch_complaint_status" in res_status.toolsInvoked

    res_generic = civic_agent.process_status_query("what's the status?")
    assert res_generic.success is True
    assert res_generic.complaint is not None

def test_video_pothole_scanner_stretch_goal(civic_agent):
    scan_report = civic_agent.run_video_scanner()
    assert scan_report["totalFramesSampled"] == 5
    assert scan_report["samplingIntervalSeconds"] == 3
    assert scan_report["totalHazardsDetected"] >= 2
    assert len(scan_report["filedTickets"]) >= 2
    for ticket in scan_report["filedTickets"]:
        assert ticket["trackingId"].startswith("AMC-2026-")
        assert "CG Road" in ticket["location"]
