from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class IssueType(str, Enum):
    POTHOLE = "pothole"
    GARBAGE = "garbage"
    STREETLIGHT = "streetlight"
    WATERLOGGING = "waterlogging"

class ComplaintStatus(str, Enum):
    SUBMITTED = "Submitted"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    WORK_VERIFIED = "Work Verified"
    RESOLVED = "Resolved"

class Coordinates(BaseModel):
    lat: float
    lng: float

class Ward(BaseModel):
    id: str
    name: str
    zone: str
    areas: List[str]
    officeAddress: Optional[str] = None
    wardOfficer: Optional[str] = None
    contactPhone: Optional[str] = None
    coordinates: Optional[Coordinates] = None

class DepartmentInfo(BaseModel):
    code: str
    slaHours: int
    leadEngineer: str
    hotline: str
    escalationEmail: str
    socialHandle: str

class TimelineEvent(BaseModel):
    status: ComplaintStatus
    timestamp: str
    note: str

class Complaint(BaseModel):
    trackingId: str
    ward: str
    wardName: str
    zone: str
    area: str
    issue: IssueType
    department: str
    status: ComplaintStatus = ComplaintStatus.ASSIGNED
    priority: str = "High"
    description: str
    imageUrl: Optional[str] = None
    filedAt: str
    expectedSlaAt: Optional[str] = None
    assignedTo: Optional[str] = None
    wardOfficer: Optional[str] = None
    wardContactPhone: Optional[str] = None
    wardOfficeAddress: Optional[str] = None
    leadEngineer: Optional[str] = None
    departmentHotline: Optional[str] = None
    departmentEmail: Optional[str] = None
    amcHelpline: Optional[str] = "155303"
    tollFreeHelpline: Optional[str] = "1800-233-2330"
    whatsappGrievance: Optional[str] = "+91-99783-22880"
    timeline: List[TimelineEvent] = Field(default_factory=list)
    resolvedAt: Optional[str] = None
    citizenFeedback: Optional[str] = None

class CreateComplaintRequest(BaseModel):
    area: str
    issue: IssueType
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    priority: Optional[str] = "High"
    lat: Optional[float] = None
    lng: Optional[float] = None
