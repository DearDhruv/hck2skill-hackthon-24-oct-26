import os
import re
import time
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from app.models.complaint import Complaint, Ward, IssueType
from app.models.agent_state import AgentResponse
from app.services.amc_db import AMCDatabaseService
from app.services.agent_engine import CivicComplaintAgent
from app.services.chaos_service import ChaosService, FaultType, ChaosException

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
app.add_middleware(GZipMiddleware, minimum_size=500)

# Initialize Services
db_service = AMCDatabaseService.get_instance()
agent_engine = CivicComplaintAgent(db=db_service)
chaos_service = ChaosService.get_instance()

@app.exception_handler(ChaosException)
async def handle_chaos_exception(request, exc: ChaosException):
    if exc.fault_type == FaultType.CORRUPTED_PAYLOAD.value:
        return Response(
            content="<<<ERR_AMC_MUNICIPAL_CORRUPT_PAYLOAD_CHUNK_HEX7F_BINARY_MALFORMED_DATA>>>",
            media_type="application/json",
            status_code=200
        )
    headers = {}
    if exc.http_status == 429:
        headers["Retry-After"] = "60"
    return JSONResponse(
        status_code=exc.http_status,
        headers=headers,
        content={
            "error": True,
            "chaosFault": exc.fault_type,
            "detail": str(exc),
            "message": str(exc),
            "subsystem": exc.subsystem,
            "httpCode": exc.http_status,
            "details": getattr(exc, "details", {})
        }
    )

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

class ChaosToggleRequest(BaseModel):
    enabled: Optional[bool] = None
    faultType: Optional[str] = None
    fault_type: Optional[str] = None
    timeoutSeconds: Optional[float] = None
    timeout_seconds: Optional[float] = None

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

@app.get("/api/chaos")
def get_chaos_status():
    """Returns current chaos status & active fault mode."""
    return chaos_service.get_status()

@app.post("/api/chaos/toggle")
def toggle_chaos(req: Optional[ChaosToggleRequest] = None):
    """Toggle chaos mode on/off and select fault type."""
    enabled = req.enabled if req else None
    fault = (req.faultType or req.fault_type) if req else None
    timeout_sec = (req.timeoutSeconds if (req and req.timeoutSeconds is not None) else (req.timeout_seconds if req else None))
    try:
        return chaos_service.toggle(enabled=enabled, fault_type=fault, timeout_seconds=timeout_sec)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    # Fast intercept for simulated corrupted municipal payload
    if chaos_service.enabled and chaos_service.active_fault == FaultType.CORRUPTED_PAYLOAD:
        chaos_service.record_fault(FaultType.CORRUPTED_PAYLOAD, {"endpoint": "/api/complaints/file"})
        return Response(
            content="<<<ERR_AMC_MUNICIPAL_CORRUPT_PAYLOAD_CHUNK_HEX7F_BINARY_MALFORMED_DATA>>>",
            media_type="application/json",
            status_code=200
        )

    image_bytes = None
    filename = "photo.jpg"
    image_url = None

    if file and file.filename:
        filename = file.filename
        image_bytes = await file.read()
        # Persist uploaded file to static/uploads
        clean_name = os.path.basename(file.filename).replace(" ", "_")
        unique_name = f"upload_{int(time.time())}_{clean_name}"
        upload_path = os.path.join(static_dir, "uploads", unique_name)
        with open(upload_path, "wb") as f:
            f.write(image_bytes)
        image_url = f"/static/uploads/{unique_name}"
    elif sampleName:
        filename = sampleName
        sample_path = os.path.join(static_dir, "samples", sampleName)
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()
        image_url = f"/static/samples/{sampleName}"

    if not image_bytes:
        filename = "pothole_cg_road.jpg"
        fallback_path = os.path.join(static_dir, "samples", filename)
        if os.path.exists(fallback_path):
            with open(fallback_path, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = b"fake_synthetic_image_bytes"
        image_url = f"/static/samples/{filename}"

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
        override_issue=override_enum,
        image_url=image_url
    )
    return response


@app.post("/api/agent/query", response_model=AgentResponse)
def handle_agent_query(req: AgentQueryRequest):
    """
    Agent conversational query handler for status checks:
    e.g. 'what\\'s the status of AMC-2026-000123?' or 'what\\'s the status?'
    """
    if chaos_service.enabled and chaos_service.active_fault == FaultType.CORRUPTED_PAYLOAD:
        chaos_service.record_fault(FaultType.CORRUPTED_PAYLOAD, {"endpoint": "/api/agent/query"})
        return Response(
            content="<<<ERR_AMC_MUNICIPAL_CORRUPT_PAYLOAD_CHUNK_HEX7F_BINARY_MALFORMED_DATA>>>",
            media_type="application/json",
            status_code=200
        )
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
