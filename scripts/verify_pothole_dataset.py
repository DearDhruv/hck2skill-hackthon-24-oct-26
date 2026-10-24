import os
import sys
import io
import json
import time

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from PIL import Image
from app.services.amc_db import AMCDatabaseService
from app.services.vision_service import VisionAnalysisService
from app.services.agent_engine import CivicComplaintAgent

def run_benchmark():
    dataset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "test_pothole_dataset")
    db = AMCDatabaseService.get_instance()
    vision = VisionAnalysisService()
    agent = CivicComplaintAgent(db=db, vision_service=vision)

    test_locations = [
        {"area": "CG Road", "ward": "W12", "notes": "Deep crater along arterial commuter corridor"},
        {"area": "Bodakdev", "ward": "W08", "notes": "Fractured road surface with sub-base erosion"},
        {"area": "Stadium", "ward": "W12", "notes": "Multiple asphalt potholes blocking lane"},
        {"area": "Maninagar", "ward": "W27", "notes": "Depression near transit stop creating rim impact hazard"},
        {"area": "Vastrapur", "ward": "W08", "notes": "Severe road breakup with jagged bituminous rim"},
        {"area": "Kankaria", "ward": "W27", "notes": "Road crater with loose aggregate along ring road"},
        {"area": "Navrangpura", "ward": "W12", "notes": "Open road pit causing two-wheeler swerve risk"},
        {"area": "Law Garden", "ward": "W12", "notes": "Pavement collapse near commercial market"}
    ]

    results = []

    files = sorted([f for f in os.listdir(dataset_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    print("=" * 110)
    print(f"NAGRIKAMC PIPELINE BENCHMARK: TESTING {len(files)} REAL POTHOLE IMAGES")
    print("=" * 110)

    for idx, fn in enumerate(files):
        img_path = os.path.join(dataset_dir, fn)
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        with Image.open(img_path) as img:
            w, h = img.size
            format_name = img.format

        loc = test_locations[idx % len(test_locations)]
        neutral_filename = f"IMG_SURVEILLANCE_{idx+101:04d}.jpg"

        # 1. Vision Direct Analysis (analyze_civic_image)
        t0 = time.time()
        cv_res = vision.analyze_civic_image(
            image_bytes=img_bytes,
            filename=neutral_filename,
            text_hint=None
        )
        cv_latency = (time.time() - t0) * 1000

        # 2. Agent Full Pipeline (process_complaint_pipeline)
        t1 = time.time()
        agent_res = agent.process_complaint_pipeline(
            image_bytes=img_bytes,
            filename=neutral_filename,
            user_area=loc["area"],
            user_notes=loc["notes"]
        )
        pipeline_latency = (time.time() - t1) * 1000

        c = agent_res.complaint

        record = {
            "imageName": fn,
            "dimensions": f"{w}x{h}",
            "fileSizeBytes": len(img_bytes),
            "fileSizeKb": round(len(img_bytes) / 1024, 1),
            "format": format_name,
            "neutralTestFilename": neutral_filename,
            "cvLatencyMs": round(cv_latency, 2),
            "pipelineLatencyMs": round(pipeline_latency, 2),
            "classification": cv_res.issue.value,
            "confidence": cv_res.confidence,
            "severity": cv_res.severity,
            "boundingBox": cv_res.boundingBox,
            "detectedFeatures": cv_res.detectedFeatures,
            "suggestedDepartment": cv_res.suggestedDepartment,
            "filedTicket": {
                "trackingId": c.trackingId,
                "ward": c.ward,
                "wardName": c.wardName,
                "zone": c.zone,
                "area": c.area,
                "department": c.department,
                "status": c.status.value,
                "assignedTo": c.assignedTo,
                "expectedSlaAt": c.expectedSlaAt
            },
            "toolsInvoked": agent_res.toolsInvoked,
            "socialDraftText": agent_res.socialDraft.text if agent_res.socialDraft else None
        }

        results.append(record)

        print(f"[{idx+1}/{len(files)}] {fn}")
        print(f"  Dimensions: {w}x{h} ({record['fileSizeKb']} KB) | CV Classification: {cv_res.issue.value.upper()} (Conf: {cv_res.confidence*100:.1f}%, Sev: {cv_res.severity})")
        print(f"  BBox: {cv_res.boundingBox}")
        print(f"  Features: {cv_res.detectedFeatures[0]}")
        print(f"  Ticket Generated: {c.trackingId} -> Ward {c.ward} ({c.wardName}) -> {c.department}")
        print(f"  Tools Invoked: {', '.join(agent_res.toolsInvoked)} (Total Time: {record['pipelineLatencyMs']:.1f}ms)")
        print("-" * 110)

    # Save detailed JSON report
    report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Docs", "pothole_benchmark_results.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nExhaustive benchmark report saved to: {report_path}")
    return results

if __name__ == "__main__":
    run_benchmark()
