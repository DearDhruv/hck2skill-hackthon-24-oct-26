import json
import os
import shutil
import threading
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from app.models.complaint import Complaint, Ward, IssueType, ComplaintStatus, TimelineEvent, DepartmentInfo

class AMCDatabaseService:
    """
    Mock Municipal (AMC) System Engine.
    Provides reactive, offline-first, thread-safe access to Ahmedabad Municipal Corporation
    wards, departments, and citizen complaint records.
    Implements INV-MOCK-01 with resetToSeedData() for demo resilience.
    """
    _instance = None
    _lock = threading.RLock()

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(base_dir, "data")
        else:
            self.data_dir = data_dir

        self.seed_file = os.path.join(self.data_dir, "amc_seed_database.json")
        self.active_file = os.path.join(self.data_dir, "amc_active_db.json")
        self._ensure_initialized()

    @classmethod
    def get_instance(cls) -> "AMCDatabaseService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _ensure_initialized(self):
        with self._lock:
            if not os.path.exists(self.active_file):
                if os.path.exists(self.seed_file):
                    shutil.copyfile(self.seed_file, self.active_file)
                else:
                    self._create_fallback_data()

    def _create_fallback_data(self):
        default_payload = {
            "wards": [
                {
                    "id": "W12",
                    "name": "Navrangpura",
                    "zone": "West",
                    "areas": ["Navrangpura", "Stadium", "CG Road", "Law Garden", "Gujarat University"],
                    "officeAddress": "AMC West Zone Office, Usmanpura, Ahmedabad",
                    "wardOfficer": "Shri Arvind Trivedi",
                    "contactPhone": "+91-79-2755-1201"
                },
                {
                    "id": "W27",
                    "name": "Maninagar",
                    "zone": "South",
                    "areas": ["Maninagar", "Kankaria", "Jawahar Chowk", "Rambaug"],
                    "officeAddress": "AMC South Zone Office, Rambaug, Maninagar",
                    "wardOfficer": "Smt. Bhavna Solanki",
                    "contactPhone": "+91-79-2546-4301"
                }
            ],
            "departments": {
                "pothole": "Roads & Buildings",
                "garbage": "Solid Waste Management",
                "streetlight": "Light Department",
                "waterlogging": "Storm Water Drainage"
            },
            "departmentMetadata": {},
            "complaints": []
        }
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.active_file, "w", encoding="utf-8") as f:
            json.dump(default_payload, f, indent=2)

    def _read_data(self) -> Dict[str, Any]:
        with self._lock:
            try:
                with open(self.active_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                with open(self.seed_file, "r", encoding="utf-8") as f:
                    return json.load(f)

    def _write_data(self, data: Dict[str, Any]):
        with self._lock:
            with open(self.active_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def reset_to_seed_data(self) -> bool:
        """Restores database to seed state for fresh judge demos."""
        with self._lock:
            if os.path.exists(self.seed_file):
                shutil.copyfile(self.seed_file, self.active_file)
                return True
            return False

    def get_wards(self) -> List[Ward]:
        data = self._read_data()
        return [Ward(**w) for w in data.get("wards", [])]

    def get_departments_map(self) -> Dict[str, str]:
        data = self._read_data()
        return data.get("departments", {})

    def get_department_metadata(self, department_name: str) -> Optional[DepartmentInfo]:
        data = self._read_data()
        meta = data.get("departmentMetadata", {}).get(department_name)
        if meta:
            return DepartmentInfo(**meta)
        return None

    def lookup_department_for_issue(self, issue: IssueType) -> str:
        dept_map = self.get_departments_map()
        return dept_map.get(issue.value, "General Municipal Administration")

    def find_ward_by_area(self, query: str) -> Optional[Ward]:
        """
        Fuzzy & exact area lookup across AMC ward registries.
        Case-insensitive matching for area names (e.g. 'CG Road', 'kankaria', 'stadium').
        """
        if not query:
            return None
        cleaned_query = query.strip().lower()
        wards = self.get_wards()

        # 1. Exact or partial match in area lists
        for ward in wards:
            for area in ward.areas:
                if cleaned_query in area.lower() or area.lower() in cleaned_query:
                    return ward

        # 2. Match ward name or ID directly
        for ward in wards:
            if cleaned_query in ward.name.lower() or ward.id.lower() == cleaned_query:
                return ward

        # Fallback to Navrangpura (W12 - West Zone) as central default if not found
        return wards[0] if wards else None

    def find_ward_by_coordinates(self, lat: float, lng: float) -> Ward:
        """Closest Euclidean distance to known ward centers."""
        wards = self.get_wards()
        if not wards:
            raise ValueError("No wards registered in AMC database.")

        best_ward = wards[0]
        min_dist_sq = float("inf")
        for ward in wards:
            if ward.coordinates:
                d = (ward.coordinates.lat - lat) ** 2 + (ward.coordinates.lng - lng) ** 2
                if d < min_dist_sq:
                    min_dist_sq = d
                    best_ward = ward
        return best_ward

    def create_complaint(
        self,
        area: str,
        issue: IssueType,
        description: str,
        ward_id: Optional[str] = None,
        imageUrl: Optional[str] = None,
        priority: str = "High",
        lat: Optional[float] = None,
        lng: Optional[float] = None
    ) -> Complaint:
        data = self._read_data()
        complaints = data.get("complaints", [])

        # Determine Ward
        ward: Optional[Ward] = None
        if ward_id:
            for w in self.get_wards():
                if w.id == ward_id:
                    ward = w
                    break
        if not ward:
            ward = self.find_ward_by_area(area)
        if not ward and lat is not None and lng is not None:
            ward = self.find_ward_by_coordinates(lat, lng)
        if not ward:
            wards = self.get_wards()
            ward = wards[0]

        # Determine Department
        department_name = self.lookup_department_for_issue(issue)
        dept_meta = self.get_department_metadata(department_name)
        sla_hours = dept_meta.slaHours if dept_meta else 24
        lead_engineer = dept_meta.leadEngineer if dept_meta else "AMC Field Officer"

        # Generate unique tracking ID: AMC-2026-XXXXXX
        now = datetime.now()
        timestamp_str = now.isoformat(timespec="seconds")
        expected_sla = (now + timedelta(hours=sla_hours)).isoformat(timespec="seconds")

        # Determine next ID index
        existing_ids = [c.get("trackingId", "") for c in complaints]
        max_num = 125
        for tid in existing_ids:
            if tid.startswith("AMC-2026-"):
                try:
                    num = int(tid.replace("AMC-2026-", ""))
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        next_id = f"AMC-2026-{max_num + 1:06d}"

        new_complaint = Complaint(
            trackingId=next_id,
            ward=ward.id,
            wardName=ward.name,
            zone=ward.zone,
            area=area,
            issue=issue,
            department=department_name,
            status=ComplaintStatus.ASSIGNED,
            priority=priority,
            description=description,
            imageUrl=imageUrl or "/static/samples/pothole_cg_road.jpg",
            filedAt=timestamp_str,
            expectedSlaAt=expected_sla,
            assignedTo=f"{lead_engineer} ({ward.name} Ward Cell)",
            timeline=[
                TimelineEvent(
                    status=ComplaintStatus.SUBMITTED,
                    timestamp=timestamp_str,
                    note="Complaint received and verified via CivicPulse AI Agent."
                ),
                TimelineEvent(
                    status=ComplaintStatus.ASSIGNED,
                    timestamp=timestamp_str,
                    note=f"Assigned to {department_name} ({ward.name} Ward). Work crew notified."
                )
            ]
        )

        complaints.insert(0, new_complaint.model_dump())
        data["complaints"] = complaints
        self._write_data(data)
        return new_complaint

    def get_complaint_by_id(self, tracking_id: str) -> Optional[Complaint]:
        data = self._read_data()
        cleaned_id = tracking_id.strip().upper()
        for c in data.get("complaints", []):
            if c.get("trackingId", "").upper() == cleaned_id:
                return Complaint(**c)
        return None

    def advance_complaint_status(self, tracking_id: str) -> Optional[Complaint]:
        """
        Simulates live lifecycle progress for dynamic judge demos.
        Transitions: Assigned -> In Progress -> Work Verified -> Resolved
        """
        data = self._read_data()
        complaints = data.get("complaints", [])
        cleaned_id = tracking_id.strip().upper()
        now_str = datetime.now().isoformat(timespec="seconds")

        for c in complaints:
            if c.get("trackingId", "").upper() == cleaned_id:
                curr_status = c.get("status")
                next_status = None
                note = ""

                if curr_status == ComplaintStatus.ASSIGNED.value:
                    next_status = ComplaintStatus.IN_PROGRESS.value
                    note = "Field inspection team dispatched. Heavy equipment on site."
                elif curr_status == ComplaintStatus.IN_PROGRESS.value:
                    next_status = ComplaintStatus.WORK_VERIFIED.value
                    note = "Physical repair/cleaning completed. Quality supervisor verification in progress."
                elif curr_status == ComplaintStatus.WORK_VERIFIED.value:
                    next_status = ComplaintStatus.RESOLVED.value
                    note = "Quality audit passed. Issue officially resolved and closed."
                    c["resolvedAt"] = now_str
                else:
                    return Complaint(**c)

                c["status"] = next_status
                timeline = c.get("timeline", [])
                timeline.append({
                    "status": next_status,
                    "timestamp": now_str,
                    "note": note
                })
                c["timeline"] = timeline
                self._write_data(data)
                return Complaint(**c)

        return None

    def list_complaints(self, limit: int = 50) -> List[Complaint]:
        data = self._read_data()
        return [Complaint(**c) for c in data.get("complaints", [])[:limit]]
