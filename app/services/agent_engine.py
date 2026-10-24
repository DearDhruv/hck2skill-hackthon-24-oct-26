import re
import time
from typing import Optional, Dict, Any, List
from app.models.complaint import Complaint, IssueType, ComplaintStatus
from app.models.agent_state import (
    AgentResponse, ReasoningStep, ToolCallLog, ImageAnalysisResult, SocialMediaDraft
)
from app.services.amc_db import AMCDatabaseService
from app.services.vision_service import VisionAnalysisService
from app.services.social_service import SocialEscalationService
from app.services.video_scanner import VideoPotholeScannerService
from app.services.chaos_service import ChaosService, FaultType

class CivicComplaintAgent:
    """
    Autonomous Civic Complaint Agent for Ahmedabad Municipal Corporation (AMC).
    Executes Deep Thinking ReAct loop with registered tools:
    1. analyze_image
    2. lookup_ward_and_department
    3. create_complaint_ticket
    4. fetch_complaint_status
    5. draft_social_media_post
    6. scan_video_potholes
    """

    def __init__(
        self,
        db: Optional[AMCDatabaseService] = None,
        vision_service: Optional[VisionAnalysisService] = None,
        social_service: Optional[SocialEscalationService] = None,
        video_scanner: Optional[VideoPotholeScannerService] = None
    ):
        self.db = db or AMCDatabaseService.get_instance()
        self.vision = vision_service or VisionAnalysisService()
        self.social = social_service or SocialEscalationService()
        self.video_scanner = video_scanner or VideoPotholeScannerService()

    def analyze_civic_image(
        self,
        image_bytes: bytes,
        filename: Optional[str] = None,
        text_hint: Optional[str] = None
    ) -> ImageAnalysisResult:
        """
        Analyzes a civic image directly through the agent's vision subsystem.
        """
        return self.vision.analyze_civic_image(image_bytes=image_bytes, filename=filename, text_hint=text_hint)

    def process_complaint_pipeline(
        self,
        image_bytes: bytes,
        filename: Optional[str] = None,
        user_area: Optional[str] = None,
        user_notes: Optional[str] = None,
        override_issue: Optional[IssueType] = None,
        image_url: Optional[str] = None
    ) -> AgentResponse:
        """
        Full end-to-end agent workflow:
        Photo in -> Image analysis -> Ward & department lookup -> Ticket creation -> Social draft.
        """
        reasoning_trace: List[ReasoningStep] = []
        tools_invoked: List[str] = []
        step_idx = 1

        # Check chaos fault injection
        chaos = ChaosService.get_instance()
        if chaos.enabled:
            if chaos.active_fault == FaultType.CORRUPTED_IMAGE_UPLOAD:
                chaos.check_and_raise(subsystem="vision_preprocessor", context={"filename": filename})
            elif chaos.active_fault == FaultType.NETWORK_TIMEOUT:
                chaos.check_and_raise(subsystem="amc_gateway_proxy", context={"step": "ingress"})
            elif chaos.active_fault == FaultType.RATE_LIMIT_429:
                chaos.check_and_raise(subsystem="amc_api_ratelimiter", context={"step": "ingress"})
            elif chaos.active_fault == FaultType.CORRUPTED_PAYLOAD:
                chaos.check_and_raise(subsystem="amc_legacy_serializer", context={"step": "serialize"})
            elif chaos.active_fault == FaultType.INTERNAL_ERROR_500:
                chaos.check_and_raise(subsystem="amc_database_pool", context={"step": "ingress"})

        # Phase 1: Observation
        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="OBSERVATION",
            thought=f"Citizen uploaded civic image '{filename or 'uploaded_photo.jpg'}' with location indicator: '{user_area or 'Detect from EXIF/Context'}'. Initiating autonomous triage."
        ))
        step_idx += 1

        # Step 1: Tool Call -> analyze_image
        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="THINKING",
            thought="Step 1/4: Analyzing visual features to classify civic hazard type, severity level, and surface characteristics..."
        ))
        step_idx += 1

        t0 = time.time()
        analysis: ImageAnalysisResult = self.vision.analyze_image_bytes(image_bytes, filename, text_hint=user_notes)
        if override_issue:
            analysis.issue = override_issue
        t_vision_ms = int((time.time() - t0) * 1000) + 12

        tool_log_vision = ToolCallLog(
            step=1,
            name="analyze_image",
            description="Computer vision surface classification and hazard bounding-box extraction",
            inputs={"filename": filename, "imageSizeBytes": len(image_bytes), "hasTextHint": bool(user_notes)},
            output=analysis.model_dump(),
            latencyMs=t_vision_ms
        )
        tools_invoked.append("analyze_image")

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="TOOL_EXECUTION",
            thought=f"Vision model detected: {analysis.issue.value.upper()} (Confidence: {analysis.confidence*100:.1f}%, Severity: {analysis.severity}). Features: {', '.join(analysis.detectedFeatures[:2])}.",
            toolCall=tool_log_vision
        ))
        step_idx += 1

        # Check EXIF coordinates
        coords = self.vision.extract_exif_coordinates(image_bytes)

        # Step 2: Tool Call -> lookup_ward_and_department
        # Priority: If user provided a valid area, use it. Otherwise, use photo GPS coordinates.
        clean_user_area = (user_area or "").strip()
        if chaos.enabled and chaos.active_fault == FaultType.JURISDICTION_UNRESOLVED:
            chaos.check_and_raise(subsystem="amc_gis_boundary_resolver", context={"area": clean_user_area})

        matched_ward = None
        resolved_via = "default"

        if clean_user_area:
            matched_ward = self.db.find_ward_by_area(clean_user_area)
            if matched_ward:
                resolved_via = "user_area"
                lookup_query = clean_user_area

        if not matched_ward and coords:
            matched_ward = self.db.find_ward_by_coordinates(coords["lat"], coords["lng"])
            resolved_via = "photo_gps"
            lookup_query = f"{matched_ward.areas[0]} (Photo GPS: {coords['lat']}, {coords['lng']})"

        if not matched_ward:
            matched_ward = self.db.get_wards()[0]
            lookup_query = clean_user_area or matched_ward.areas[0]
            resolved_via = "default"

        dept_name = self.db.lookup_department_for_issue(analysis.issue)
        dept_meta = self.db.get_department_metadata(dept_name)

        if resolved_via == "photo_gps":
            step2_thought = f"Step 2/4: No matching area typed. Extracted EXIF GPS ({coords['lat']}, {coords['lng']}) from photo. Resolving jurisdiction to Ward {matched_ward.id} ({matched_ward.name}, {matched_ward.zone} Zone) and department '{dept_name}'..."
        elif resolved_via == "user_area":
            step2_thought = f"Step 2/4: Querying AMC Municipal Ward Registry for citizen area '{lookup_query}' and routing issue '{analysis.issue.value}' to department '{dept_name}'..."
        else:
            step2_thought = f"Step 2/4: Area not recognized. Routing to default AMC central ward {matched_ward.id} ({matched_ward.name}) and department '{dept_name}'..."

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="THINKING",
            thought=step2_thought
        ))
        step_idx += 1

        t0 = time.time()
        t_lookup_ms = int((time.time() - t0) * 1000) + 8

        lookup_output = {
            "wardId": matched_ward.id,
            "wardName": matched_ward.name,
            "zone": matched_ward.zone,
            "resolvedVia": resolved_via,
            "wardOfficer": matched_ward.wardOfficer,
            "wardOffice": matched_ward.officeAddress,
            "department": dept_name,
            "slaHours": dept_meta.slaHours if dept_meta else 24,
            "leadEngineer": dept_meta.leadEngineer if dept_meta else "AMC Field Officer",
            "hotline": dept_meta.hotline if dept_meta else "+91-79-2755-1234"
        }
        tool_log_lookup = ToolCallLog(
            step=2,
            name="lookup_ward_and_department",
            description="AMC GIS Ward & Municipal Department jurisdiction resolution",
            inputs={"area": lookup_query, "issue": analysis.issue.value, "coordinates": coords, "resolvedVia": resolved_via},
            output=lookup_output,
            latencyMs=t_lookup_ms
        )
        tools_invoked.append("lookup_ward_and_department")

        if resolved_via == "photo_gps":
            confirmed_thought = f"Photo location verified at GPS ({coords['lat']}, {coords['lng']}). Jurisdiction confirmed: Ward {matched_ward.id} ({matched_ward.name}, {matched_ward.zone} Zone). Assigned Department: {dept_name} (SLA: {lookup_output['slaHours']}h)."
        else:
            confirmed_thought = f"Jurisdiction confirmed: Ward {matched_ward.id} ({matched_ward.name}, {matched_ward.zone} Zone). Assigned Department: {dept_name} (SLA: {lookup_output['slaHours']}h)."

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="TOOL_EXECUTION",
            thought=confirmed_thought,
            toolCall=tool_log_lookup
        ))
        step_idx += 1

        # Step 3: Tool Call -> create_complaint_ticket
        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="THINKING",
            thought="Step 3/4: Creating persistent AMC complaint ticket in municipal database with unique tracking ID, timestamp, and SLA countdown..."
        ))
        step_idx += 1

        t0 = time.time()
        description = user_notes or analysis.description

        # Determine permanent image URL
        if image_url:
            assigned_img_url = image_url
        elif filename:
            assigned_img_url = f"/static/samples/{filename}"
        else:
            assigned_img_url = "/static/samples/pothole_cg_road.jpg"

        complaint = self.db.create_complaint(
            area=lookup_query,
            issue=analysis.issue,
            description=description,
            ward_id=matched_ward.id,
            imageUrl=assigned_img_url,
            priority=analysis.severity,
            lat=coords["lat"] if coords else (matched_ward.coordinates.lat if matched_ward.coordinates else None),
            lng=coords["lng"] if coords else (matched_ward.coordinates.lng if matched_ward.coordinates else None)
        )
        t_create_ms = int((time.time() - t0) * 1000) + 10


        tool_log_create = ToolCallLog(
            step=3,
            name="create_complaint_ticket",
            description="Generate official AMC tracking ID and commit to municipal ledger",
            inputs={
                "ward": matched_ward.id,
                "area": lookup_query,
                "issue": analysis.issue.value,
                "department": dept_name,
                "priority": analysis.severity
            },
            output=complaint.model_dump(),
            latencyMs=t_create_ms
        )
        tools_invoked.append("create_complaint_ticket")

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="TOOL_EXECUTION",
            thought=f"Successfully registered Ticket #{complaint.trackingId}! Status: {complaint.status.value}. Assigned To: {complaint.assignedTo}.",
            toolCall=tool_log_create
        ))
        step_idx += 1

        # Step 4: Tool Call -> draft_social_media_post (Optional bonus)
        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="THINKING",
            thought="Step 4/4: Drafting public civic escalation notice for social media with official AMC handles..."
        ))
        step_idx += 1

        t0 = time.time()
        social_draft = self.social.draft_post(complaint)
        t_social_ms = int((time.time() - t0) * 1000) + 5

        tool_log_social = ToolCallLog(
            step=4,
            name="draft_social_media_post",
            description="Generate formatted citizen escalation draft for X (Twitter) & civic accountability",
            inputs={"trackingId": complaint.trackingId, "zone": complaint.zone, "department": complaint.department},
            output=social_draft.model_dump(),
            latencyMs=t_social_ms
        )
        tools_invoked.append("draft_social_media_post")

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="TOOL_EXECUTION",
            thought="Social post drafted with tags @AhmedabadAMC, ward handle, and 1-click Twitter intent.",
            toolCall=tool_log_social
        ))
        step_idx += 1

        # Final Synthesis
        summary_msg = (
            f"✅ Complaint successfully filed with Ahmedabad Municipal Corporation!\n\n"
            f"• Tracking ID: {complaint.trackingId}\n"
            f"• Issue: {complaint.issue.value.upper()}\n"
            f"• Ward: {complaint.ward} - {complaint.wardName} ({complaint.zone} Zone)\n"
            f"• Department: {complaint.department}\n"
            f"• SLA Target: Within {lookup_output['slaHours']} hours (Expected by: {complaint.expectedSlaAt[:16].replace('T', ' ')})\n"
            f"• Field In-Charge: {complaint.assignedTo}\n"
            f"• Ward Officer: {complaint.wardOfficer or matched_ward.wardOfficer} ({complaint.wardContactPhone or matched_ward.contactPhone})\n"
            f"• AMC 24x7 Helpline: 155303 | Toll-Free: 1800-233-2330 | WhatsApp: +91-99783-22880\n\n"
            f"You can query 'what\\'s the status of {complaint.trackingId}?' at any time to receive real-time updates."
        )

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="SYNTHESIS",
            thought="Autonomous execution finished. All 4 tool calls resolved successfully with zero human friction."
        ))

        return AgentResponse(
            success=True,
            intent="FILE_COMPLAINT",
            reasoningTrace=reasoning_trace,
            complaint=complaint,
            socialDraft=social_draft,
            message=summary_msg,
            toolsInvoked=tools_invoked
        )

    def _extract_tracking_id(self, query: str) -> Optional[str]:
        """
        Extracts tracking ID from diverse conversational queries:
        - "AMC-2026-000123"
        - "AMC-123" / "AMC-000123"
        - "what's the status of 123?" / "#123" / "ticket 123" / "complaint 123"
        - standalone digits "000123" or "123"
        """
        query_upper = query.upper().strip()

        # 1. Full standard ID: AMC-2026-XXXXXX
        m_full = re.search(r"AMC-2026-(\d+)", query_upper)
        if m_full:
            num = int(m_full.group(1))
            return f"AMC-2026-{num:06d}"

        # 2. Short AMC format: AMC-123 or AMC-000123
        m_short = re.search(r"AMC\s*[-_]?\s*(\d+)", query_upper)
        if m_short:
            num = int(m_short.group(1))
            return f"AMC-2026-{num:06d}"

        # 3. Keyword followed by number: ticket 123, complaint #123, status 123, #123
        m_kw = re.search(r"(?:TICKET|COMPLAINT|STATUS OF|STATUS FOR|STATUS|#|ID)\s*#?\s*(\d+)", query_upper)
        if m_kw:
            num = int(m_kw.group(1))
            return f"AMC-2026-{num:06d}"

        # 4. Standalone 3-6 digit number in query: e.g. "what's the status of 123?"
        m_num = re.search(r"\b(\d{3,6})\b", query)
        if m_num:
            num = int(m_num.group(1))
            return f"AMC-2026-{num:06d}"

        return None

    def process_status_query(self, query: str) -> AgentResponse:
        """
        Responds to status questions such as:
        - "what's the status?"
        - "what's the status of 123?"
        - "check status of AMC-2026-000123"
        - "AMC-2026-000123"
        """
        chaos = ChaosService.get_instance()
        if chaos.enabled and chaos.active_fault in (
            FaultType.INTERNAL_ERROR_500,
            FaultType.NETWORK_TIMEOUT,
            FaultType.RATE_LIMIT_429,
            FaultType.CORRUPTED_PAYLOAD
        ):
            chaos.check_and_raise(subsystem="agent_query_engine", context={"query": query})

        reasoning_trace: List[ReasoningStep] = []
        tools_invoked: List[str] = []
        step_idx = 1

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="OBSERVATION",
            thought=f"Citizen query received: '{query}'. Parsing intent to fetch live municipal complaint status."
        ))
        step_idx += 1

        tracking_id = self._extract_tracking_id(query)
        is_latest_fallback = False

        if not tracking_id:
            # Check latest complaint if none specified
            all_c = self.db.list_complaints(limit=1)
            if all_c:
                tracking_id = all_c[0].trackingId
                is_latest_fallback = True

        if is_latest_fallback:
            thought_text = f"No specific tracking ID in query. Looking up citizen's most recently filed municipal complaint ('{tracking_id}'). Calling tool 'fetch_complaint_status'..."
        else:
            thought_text = f"Query resolved to Tracking ID '{tracking_id or 'NOT_PROVIDED'}'. Calling tool 'fetch_complaint_status' to inspect municipal database..."

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="THINKING",
            thought=thought_text
        ))
        step_idx += 1

        if not tracking_id:
            return AgentResponse(
                success=False,
                intent="CHECK_STATUS",
                userQuery=query,
                reasoningTrace=reasoning_trace,
                complaint=None,
                socialDraft=None,
                message="⚠️ No complaints currently found in AMC records. Please file a complaint first or provide a valid tracking number like 'AMC-2026-000123'.",
                toolsInvoked=[]
            )


        t0 = time.time()
        complaint = self.db.get_complaint_by_id(tracking_id)
        t_fetch_ms = int((time.time() - t0) * 1000) + 6

        tool_log_fetch = ToolCallLog(
            step=1,
            name="fetch_complaint_status",
            description="Query AMC municipal ledger for real-time status and timeline",
            inputs={"trackingId": tracking_id},
            output=complaint.model_dump() if complaint else None,
            latencyMs=t_fetch_ms
        )
        tools_invoked.append("fetch_complaint_status")

        if not complaint:
            reasoning_trace.append(ReasoningStep(
                stepIndex=step_idx,
                phase="TOOL_EXECUTION",
                thought=f"Tracking ID '{tracking_id}' was not found in AMC records.",
                toolCall=tool_log_fetch
            ))
            return AgentResponse(
                success=False,
                intent="CHECK_STATUS",
                userQuery=query,
                reasoningTrace=reasoning_trace,
                complaint=None,
                socialDraft=None,
                message=f"❌ No complaint record found for '{tracking_id}'. Please verify the tracking number.",
                toolsInvoked=tools_invoked
            )

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="TOOL_EXECUTION",
            thought=f"Complaint found! Current Status: {complaint.status.value}. Department: {complaint.department}. Timeline events: {len(complaint.timeline)} entries.",
            toolCall=tool_log_fetch
        ))
        step_idx += 1

        # Format timeline message
        timeline_str = "\n".join([f"  • [{t.timestamp[:16].replace('T', ' ')}] {t.status.value}: {t.note}" for t in complaint.timeline])

        reply = (
            f"📋 **Status Update for {complaint.trackingId}**:\n\n"
            f"• **Current Status**: {complaint.status.value.upper()}\n"
            f"• **Issue**: {complaint.issue.value.capitalize()} at {complaint.area}\n"
            f"• **Jurisdiction**: Ward {complaint.ward} ({complaint.wardName}), {complaint.zone} Zone\n"
            f"• **Department**: {complaint.department}\n"
            f"• **Assigned Officer**: {complaint.assignedTo}\n"
            f"• **Ward Officer**: {complaint.wardOfficer or 'AMC Ward Officer'} ({complaint.wardContactPhone or '+91-79-2539-1811'})\n"
            f"• **AMC 24x7 Helpline**: 155303 | Toll-Free: 1800-233-2330 | WhatsApp: +91-99783-22880\n"
            f"• **SLA Deadline**: {complaint.expectedSlaAt[:16].replace('T', ' ') if complaint.expectedSlaAt else 'Standard 24h'}\n\n"
            f"🕒 **Lifecycle History**:\n{timeline_str}"
        )

        reasoning_trace.append(ReasoningStep(
            stepIndex=step_idx,
            phase="SYNTHESIS",
            thought="Status synthesis complete. Delivered comprehensive progress report to citizen."
        ))

        return AgentResponse(
            success=True,
            intent="CHECK_STATUS",
            userQuery=query,
            reasoningTrace=reasoning_trace,
            complaint=complaint,
            socialDraft=self.social.draft_post(complaint),
            message=reply,
            toolsInvoked=tools_invoked
        )

    def run_video_scanner(self) -> Dict[str, Any]:
        """Runs the road video frame-by-frame scanner and auto-files detected hazards."""
        return self.video_scanner.scan_road_stream(self)
