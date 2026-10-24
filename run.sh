#!/usr/bin/env bash
# ==============================================================================
# Script: run.sh
# Purpose: Single-command launcher for NagrikAMC Civic Complaint Agent
# Track 01 · Hack2Skill Hackathon 2026
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting NagrikAMC / CivicPulse AI Agent..."
echo "📍 Workspace: $SCRIPT_DIR"

# 1. Check or activate Python virtual environment
if [[ ! -d ".venv" ]]; then
    echo "📦 Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# 2. Check dependencies
if ! python -c "import fastapi, uvicorn, pydantic, PIL" 2>/dev/null; then
    echo "📥 Installing required dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

# 3. Ensure sample assets exist
if [[ ! -f "app/static/samples/pothole_cg_road.jpg" || ! -f "app/static/samples/video/frame_1_t0s.jpg" ]]; then
    echo "🖼️ Generating sample civic hazard images and road video frames..."
    python scripts/generate_sample_assets.py
fi


# 4. Launch FastAPI server
PORT=8000
echo "=================================================================="
echo "🎉 NagrikAMC Civic Complaint Agent is RUNNING!"
echo "👉 Open interactive demo in browser: http://localhost:$PORT"
echo "👉 API Swagger Docs:                http://localhost:$PORT/docs"
echo "=================================================================="

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload
