import os
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models.complaint import Complaint, Ward, IssueType
from app.models.agent_state import AgentResponse
from app.services.amc_db import AMCDatabaseService
from app.services.agent_engine import CivicComplaintAgent

app = FastAPI(
    title="NagrikAMC / CivicPulse AI",
    description="Autonomous Civic Complaint Agent for Ahmedabad Municipal Corporation (Track 01)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
db_service = AMCDatabaseService.get_instance()
agent_engine = CivicComplaintAgent(db=db_service)

# Mount static files
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
os.makedirs(static_dir, exist_ok=True)
os.makedirs(os.path.join(static_dir, "samples"), exist_ok=True)
os.makedirs(os.path.join(static_dir, "uploads"), exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

class AgentQueryRequest(BaseModel):
    query: str

class FileSampleRequest(BaseModel):
    sampleName: str
    area: Optional[str] = None
    notes: Optional[str] = None
    issueType: Optional[str] = None

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "NagrikAMC / CivicPulse AI Backend is Active"}

@app.get("/api/wards", response_model=List[Ward])
def get_wards():
    """Returns all registered AMC municipal wards."""
    return db_service.get_wards()

@app.get("/api/complaints", response_model=List[Complaint])
def get_complaints():
    """Lists all complaints currently in AMC database."""
    return db_service.list_complaints()

@app.get("/api/complaints/{tracking_id}", response_model=Complaint)
def get_complaint(tracking_id: str):
    """Fetches details for a single tracking ID."""
    complaint = db_service.get_complaint_by_id(tracking_id)
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint '{tracking_id}' not found.")
    return complaint

@app.post("/api/complaints/{tracking_id}/advance", response_model=Complaint)
def advance_complaint_status(tracking_id: str):
    """
    Simulates real-world lifecycle progression (Assigned -> In Progress -> Work Verified -> Resolved).
    Used during live demos to showcase status changes.
    """
    updated = db_service.advance_complaint_status(tracking_id)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Complaint '{tracking_id}' not found.")
    return updated

@app.post("/api/complaints/file", response_model=AgentResponse)
async def file_complaint_upload(
    file: Optional[UploadFile] = File(None),
    sampleName: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    issueType: Optional[str] = Form(None)
):
    """
    Core Agent Entrypoint:
    Accepts photo (uploaded or sample), performs image analysis, ward/department lookup,
    generates tracking ID, and drafts social media escalation.
    """
    image_bytes = None
    filename = "photo.jpg"

    if file and file.filename:
        filename = file.filename
        image_bytes = await file.read()
    elif sampleName:
        filename = sampleName
        sample_path = os.path.join(static_dir, "samples", sampleName)
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()

    if not image_bytes:
        filename = "pothole_cg_road.jpg"
        fallback_path = os.path.join(static_dir, "samples", filename)
        if os.path.exists(fallback_path):
            with open(fallback_path, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = b"fake_synthetic_image_bytes"

    override_enum = None
    if issueType:
        try:
            override_enum = IssueType(issueType.lower())
        except ValueError:
            pass

    response = agent_engine.process_complaint_pipeline(
        image_bytes=image_bytes,
        filename=filename,
        user_area=area,
        user_notes=notes,
        override_issue=override_enum
    )
    return response

@app.post("/api/agent/query", response_model=AgentResponse)
def handle_agent_query(req: AgentQueryRequest):
    """
    Agent conversational query handler for status checks:
    e.g. 'what\\'s the status of AMC-2026-000123?' or 'what\\'s the status?'
    """
    return agent_engine.process_status_query(req.query)

@app.post("/api/video/scan")
def scan_road_video():
    """
    Stretch Goal: Frame-by-frame road hazard video scanner.
    Samples every 3 seconds, detects potholes, pins GPS coordinates, and auto-files tickets.
    """
    return agent_engine.run_video_scanner()

@app.post("/api/admin/reset")
def reset_database():
    """Restores database to seed state (INV-MOCK-01)."""
    success = db_service.reset_to_seed_data()
    return {"success": success, "message": "AMC Municipal Database reset to initial seed state."}
