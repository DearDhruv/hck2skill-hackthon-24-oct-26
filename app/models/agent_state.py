from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.complaint import Complaint, IssueType, Ward

class ToolCallLog(BaseModel):
    step: int
    name: str
    description: str
    inputs: Dict[str, Any]
    output: Any
    latencyMs: int = 15

class ReasoningStep(BaseModel):
    stepIndex: int
    phase: str  # "OBSERVATION", "THINKING", "TOOL_EXECUTION", "SYNTHESIS"
    thought: str
    toolCall: Optional[ToolCallLog] = None

class SocialMediaDraft(BaseModel):
    platform: str = "X / Twitter"
    text: str
    tags: List[str]
    mentions: List[str]
    intentUrl: str
    previewHtml: Optional[str] = None

class AgentResponse(BaseModel):
    success: bool
    intent: str  # "FILE_COMPLAINT", "CHECK_STATUS", "GENERAL_QUERY", "VIDEO_SCAN"
    userQuery: Optional[str] = None
    reasoningTrace: List[ReasoningStep] = Field(default_factory=list)
    complaint: Optional[Complaint] = None
    socialDraft: Optional[SocialMediaDraft] = None
    message: str
    toolsInvoked: List[str] = Field(default_factory=list)

class ImageAnalysisResult(BaseModel):
    issue: IssueType
    confidence: float
    severity: str
    description: str
    detectedFeatures: List[str]
    suggestedDepartment: str
    boundingBox: Optional[Dict[str, float]] = None

class VideoFrameDetection(BaseModel):
    frameNumber: int
    timestampSeconds: float
    issue: IssueType
    confidence: float
    hazardDetected: bool
    boundingBox: Optional[Dict[str, float]] = None
    coordinates: Optional[Dict[str, float]] = None
    autoFiledTrackingId: Optional[str] = None
