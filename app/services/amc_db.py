import json
import os
import re
import shutil
import threading
from datetime import datetime, timedelta

from typing import List, Optional, Dict, Any
from app.models.complaint import Complaint, Ward, IssueType, ComplaintStatus, TimelineEvent, DepartmentInfo
from app.services.chaos_service import ChaosService, FaultType

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
            # Canonical seed file location in workspace
            canonical_seed = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "amc_seed_database.json"
            )

            # Ensure seed file exists in this instance's data_dir
            if not os.path.exists(self.seed_file):
                os.makedirs(self.data_dir, exist_ok=True)
                if os.path.exists(canonical_seed) and os.path.abspath(canonical_seed) != os.path.abspath(self.seed_file):
                    shutil.copyfile(canonical_seed, self.seed_file)
                else:
                    self._create_fallback_data()

            # Ensure active file exists
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
                    "contactPhone": "+91-79-2755-1201",
                    "coordinates": {"lat": 23.0375, "lng": 72.5583}
                },
                {
                    "id": "W27",
                    "name": "Maninagar",
                    "zone": "South",
                    "areas": ["Maninagar", "Kankaria", "Jawahar Chowk", "Rambaug"],
                    "officeAddress": "AMC South Zone Office, Rambaug, Maninagar",
                    "wardOfficer": "Smt. Bhavna Solanki",
                    "contactPhone": "+91-79-2546-4301",
                    "coordinates": {"lat": 22.9978, "lng": 72.6033}
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
        with open(self.seed_file, "w", encoding="utf-8") as f:
            json.dump(default_payload, f, indent=2)
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
        """Atomic write using temporary file to prevent partial file writes / corruption."""
        with self._lock:
            temp_file = self.active_file + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_file, self.active_file)

    def reset_to_seed_data(self) -> bool:
        """Restores database to seed state for fresh judge demos (INV-MOCK-01)."""
        with self._lock:
            if os.path.exists(self.seed_file):
                temp_file = self.active_file + ".tmp"
                shutil.copyfile(self.seed_file, temp_file)
                os.replace(temp_file, self.active_file)
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
        Supports area names (e.g. 'CG Road', 'Kankaria'), ward names ('Navrangpura', 'Bodakdev'),
        ward IDs ('W12', 'W27', 'Ward 27', 'Ward-12'), and zones ('South Zone', 'West Zone').
        Returns None if no matching ward is found.
        """
        if not query:
            return None

        chaos = ChaosService.get_instance()
        if chaos.enabled and chaos.active_fault == FaultType.JURISDICTION_UNRESOLVED:
            chaos.check_and_raise(subsystem="amc_gis_boundary_resolver", context={"query": query})

        cleaned_query = query.strip().lower()
        wards = self.get_wards()

        # 1. Match normalized ward ID (e.g. "w12", "w27", "ward 12", "ward-27", "ward 08")
        id_numeric_match = re.search(r"(?:ward|w)?\s*[-_]?\s*(\d+)", cleaned_query)
        if id_numeric_match:
            num = int(id_numeric_match.group(1))
            for ward in wards:
                ward_num_match = re.search(r"\d+", ward.id)
                if ward_num_match and int(ward_num_match.group(0)) == num:
                    return ward

        # 2. Exact match on ward name or ward ID
        for ward in wards:
            if cleaned_query == ward.name.lower() or cleaned_query == ward.id.lower():
                return ward

        # 3. Exact match in areas list
        for ward in wards:
            for area in ward.areas:
                if cleaned_query == area.lower():
                    return ward

        # 4. Area substring / contains match
        for ward in wards:
            for area in ward.areas:
                if area.lower() in cleaned_query or (len(cleaned_query) >= 3 and cleaned_query in area.lower()):
                    return ward

        # 5. Ward name substring match
        for ward in wards:
            if ward.name.lower() in cleaned_query or (len(cleaned_query) >= 4 and cleaned_query in ward.name.lower()):
                return ward

        # 6. Zone match
        for ward in wards:
            if ward.zone.lower() in cleaned_query:
                return ward

        return None


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
        with self._lock:
            chaos = ChaosService.get_instance()
            if chaos.enabled and chaos.active_fault in (FaultType.INTERNAL_ERROR_500, FaultType.JURISDICTION_UNRESOLVED):
                chaos.check_and_raise(subsystem="amc_database_pool", context={"action": "create_complaint"})

            data = self._read_data()
            complaints = data.get("complaints", [])

            # Determine Ward
            ward: Optional[Ward] = None
            if ward_id:
                for w in self.get_wards():
                    if w.id == ward_id:
                        ward = w
                        break
            if not ward and area and area.strip():
                ward = self.find_ward_by_area(area.strip())
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
            dept_hotline = dept_meta.hotline if dept_meta else "+91-79-2755-1234"
            dept_email = dept_meta.escalationEmail if dept_meta else "grievance@ahmedabadcity.gov.in"

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
                wardOfficer=ward.wardOfficer or "Shri Arvind Trivedi",
                wardContactPhone=ward.contactPhone or "+91-79-2755-1201",
                wardOfficeAddress=ward.officeAddress or f"AMC {ward.name} Ward Office, {ward.zone} Zone, Ahmedabad",
                leadEngineer=lead_engineer,
                departmentHotline=dept_hotline,
                departmentEmail=dept_email,
                amcHelpline="155303",
                tollFreeHelpline="1800-233-2330",
                whatsappGrievance="+91-99783-22880",
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

    def _enrich_complaint_dict(self, c_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all complaints (including legacy/seed) have complete authority contact affordances."""
        c = dict(c_dict)
        ward_id = c.get("ward")
        ward_obj = None
        for w in self.get_wards():
            if w.id == ward_id or w.name.lower() == (c.get("wardName") or "").lower():
                ward_obj = w
                break

        dept_meta = self.get_department_metadata(c.get("department", ""))

        if not c.get("wardOfficer") and ward_obj:
            c["wardOfficer"] = ward_obj.wardOfficer
        if not c.get("wardContactPhone") and ward_obj:
            c["wardContactPhone"] = ward_obj.contactPhone
        if not c.get("wardOfficeAddress") and ward_obj:
            c["wardOfficeAddress"] = ward_obj.officeAddress

        if not c.get("leadEngineer") and dept_meta:
            c["leadEngineer"] = dept_meta.leadEngineer
        if not c.get("departmentHotline") and dept_meta:
            c["departmentHotline"] = dept_meta.hotline
        if not c.get("departmentEmail") and dept_meta:
            c["departmentEmail"] = dept_meta.escalationEmail

        c.setdefault("amcHelpline", "155303")
        c.setdefault("tollFreeHelpline", "1800-233-2330")
        c.setdefault("whatsappGrievance", "+91-99783-22880")
        return c

    def get_complaint_by_id(self, tracking_id: str) -> Optional[Complaint]:
        chaos = ChaosService.get_instance()
        if chaos.enabled and chaos.active_fault == FaultType.INTERNAL_ERROR_500:
            chaos.check_and_raise(subsystem="amc_database_pool", context={"action": "get_complaint_by_id", "id": tracking_id})

        data = self._read_data()
        cleaned_id = tracking_id.strip().upper()
        for c in data.get("complaints", []):
            if c.get("trackingId", "").upper() == cleaned_id:
                return Complaint(**self._enrich_complaint_dict(c))
        return None

    def advance_complaint_status(self, tracking_id: str) -> Optional[Complaint]:
        """
        Simulates live lifecycle progress for dynamic judge demos.
        Transitions: Assigned -> In Progress -> Work Verified -> Resolved
        """
        with self._lock:
            chaos = ChaosService.get_instance()
            if chaos.enabled and chaos.active_fault == FaultType.INTERNAL_ERROR_500:
                chaos.check_and_raise(subsystem="amc_database_pool", context={"action": "advance_complaint_status", "id": tracking_id})

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
                        return Complaint(**self._enrich_complaint_dict(c))

                    c["status"] = next_status
                    timeline = c.get("timeline", [])
                    timeline.append({
                        "status": next_status,
                        "timestamp": now_str,
                        "note": note
                    })
                    c["timeline"] = timeline
                    self._write_data(data)
                    return Complaint(**self._enrich_complaint_dict(c))

            return None

    def list_complaints(self, limit: int = 50) -> List[Complaint]:
        chaos = ChaosService.get_instance()
        if chaos.enabled and chaos.active_fault == FaultType.INTERNAL_ERROR_500:
            chaos.check_and_raise(subsystem="amc_database_pool", context={"action": "list_complaints"})

        data = self._read_data()
        return [Complaint(**self._enrich_complaint_dict(c)) for c in data.get("complaints", [])[:limit]]
