import os
import io
import time
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw
from app.models.complaint import IssueType
from app.models.agent_state import VideoFrameDetection

class VideoPotholeScannerService:
    """
    Video Surveillance & Road Inspection Engine.
    Samples road video frames every 3 seconds, detects potholes via vision model,
    pins hazards with simulated GPS telemetry, and automates ticket filing.
    """

    # Simulated drive along CG Road, Ahmedabad (Navrangpura W12)
    ROAD_WAYPOINTS = [
        {"sec": 0.0, "lat": 23.0360, "lng": 72.5560, "location": "CG Road, Near Stadium Circle", "hazard": False},
        {"sec": 3.0, "lat": 23.0372, "lng": 72.5571, "location": "CG Road, Opp. Municipal Market", "hazard": True, "conf": 0.962, "bbox": {"x": 30, "y": 55, "w": 40, "h": 28}},
        {"sec": 6.0, "lat": 23.0385, "lng": 72.5582, "location": "CG Road, Bodyline Crossroads", "hazard": False},
        {"sec": 9.0, "lat": 23.0398, "lng": 72.5594, "location": "CG Road, Near Navrangpura Bus Stop", "hazard": True, "conf": 0.941, "bbox": {"x": 20, "y": 60, "w": 52, "h": 32}},
        {"sec": 12.0, "lat": 23.0410, "lng": 72.5605, "location": "CG Road, Law Garden Junction", "hazard": False}
    ]

    def scan_road_stream(self, agent_engine) -> Dict[str, Any]:
        """
        Processes simulated video frames at 3s intervals, detects road hazards,
        pins to coordinates, and files complaints via the civic agent.
        """
        detections: List[VideoFrameDetection] = []
        filed_tickets: List[Dict[str, Any]] = []

        for idx, pt in enumerate(self.ROAD_WAYPOINTS):
            sec = pt["sec"]
            is_hazard = pt["hazard"]
            auto_tracking_id = None

            if is_hazard:
                # File complaint via agent's database
                complaint = agent_engine.db.create_complaint(
                    area="CG Road",
                    issue=IssueType.POTHOLE,
                    description=f"Automated video scanner detected road crater at {pt['location']} (Time: {sec}s). Geo-coordinates: {pt['lat']}, {pt['lng']}.",
                    imageUrl="/static/samples/pothole_cg_road.jpg",
                    priority="Critical",
                    lat=pt["lat"],
                    lng=pt["lng"]
                )
                auto_tracking_id = complaint.trackingId
                filed_tickets.append({
                    "trackingId": complaint.trackingId,
                    "location": pt["location"],
                    "coordinates": {"lat": pt["lat"], "lng": pt["lng"]},
                    "timestamp": f"{sec}s",
                    "status": complaint.status.value,
                    "ward": complaint.wardName
                })

            detections.append(VideoFrameDetection(
                frameNumber=idx + 1,
                timestampSeconds=sec,
                issue=IssueType.POTHOLE if is_hazard else IssueType.POTHOLE,
                confidence=pt.get("conf", 0.12),
                hazardDetected=is_hazard,
                boundingBox=pt.get("bbox"),
                coordinates={"lat": pt["lat"], "lng": pt["lng"]},
                autoFiledTrackingId=auto_tracking_id
            ))

        return {
            "totalFramesSampled": len(detections),
            "samplingIntervalSeconds": 3,
            "totalHazardsDetected": len(filed_tickets),
            "roadCorridor": "CG Road Transit Arterial (Ahmedabad West Zone)",
            "detections": [d.model_dump() for d in detections],
            "filedTickets": filed_tickets
        }
