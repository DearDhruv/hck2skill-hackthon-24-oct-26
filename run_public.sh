#!/usr/bin/env bash
# ==============================================================================
# Script: run_public.sh
# Purpose: Single-command launcher for NagrikAMC with an instant Public HTTPS URL
# Track 01 · Hack2Skill Hackathon 2026
#
# Features:
#   - Starts NagrikAMC FastAPI backend (if not already running)
#   - Establishes zero-config public HTTPS tunnel (Cloudflare Tunnel / SSH)
#   - Outputs clickable public demo URL for judges & mobile devices
#   - Supports foreground mode, background daemon mode (--daemon), and stop (--stop)
# ==============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT=8000
SERVER_LOG="$SCRIPT_DIR/server.log"
TUNNEL_LOG="$SCRIPT_DIR/tunnel.log"
SERVER_PID_FILE="$SCRIPT_DIR/.server.pid"
TUNNEL_PID_FILE="$SCRIPT_DIR/.tunnel.pid"
URL_FILE="$SCRIPT_DIR/PUBLIC_URL.txt"

# ------------------------------------------------------------------------------
# Usage / Help
# ------------------------------------------------------------------------------
show_help() {
    cat << EOF
Usage: ./run_public.sh [OPTIONS]

Options:
  --daemon, -d, --bg    Run server and public tunnel in the background indefinitely.
  --stop               Stop all running server and tunnel background processes.
  --status             Show current running status and active public URL.
  --help, -h           Show this help message.

Default (no options):  Runs in foreground and prints live status. Press Ctrl+C to stop.
EOF
    exit 0
}

# ------------------------------------------------------------------------------
# Action: Stop
# ------------------------------------------------------------------------------
stop_services() {
    echo "🛑 Stopping NagrikAMC server and public tunnel..."
    
    if [[ -f "$TUNNEL_PID_FILE" ]]; then
        TPID=$(cat "$TUNNEL_PID_FILE" 2>/dev/null || true)
        if [[ -n "$TPID" ]] && kill -0 "$TPID" 2>/dev/null; then
            kill "$TPID" 2>/dev/null || true
            echo "  ✓ Stopped tunnel process (PID: $TPID)"
        fi
        rm -f "$TUNNEL_PID_FILE"
    fi
    pkill -f "cloudflared tunnel --url" 2>/dev/null || true
    pkill -f "nokey@localhost.run" 2>/dev/null || true

    if [[ -f "$SERVER_PID_FILE" ]]; then
        SPID=$(cat "$SERVER_PID_FILE" 2>/dev/null || true)
        if [[ -n "$SPID" ]] && kill -0 "$SPID" 2>/dev/null; then
            kill "$SPID" 2>/dev/null || true
            echo "  ✓ Stopped server process (PID: $SPID)"
        fi
        rm -f "$SERVER_PID_FILE"
    fi

    # Check port 8000
    LOCAL_PIDS=$(lsof -t -i:"$PORT" 2>/dev/null || true)
    if [[ -n "$LOCAL_PIDS" ]]; then
        echo "  Freeing port $PORT (PIDs: $LOCAL_PIDS)..."
        kill -9 $LOCAL_PIDS 2>/dev/null || true
    fi

    rm -f "$URL_FILE" "$SCRIPT_DIR/.public_url"
    echo "✅ All services stopped successfully."
    exit 0
}

# ------------------------------------------------------------------------------
# Action: Status
# ------------------------------------------------------------------------------
show_status() {
    echo "🔍 Checking NagrikAMC Service Status:"
    PORT_ACTIVE=$(lsof -i:"$PORT" 2>/dev/null || true)
    if [[ -n "$PORT_ACTIVE" ]]; then
        echo "  🟢 Local Server is RUNNING on port $PORT."
    else
        echo "  🔴 Local Server is NOT running."
    fi

    if [[ -f "$URL_FILE" ]]; then
        ACTIVE_URL=$(cat "$URL_FILE" | tr -d '\r\n')
        echo "  🌐 Active Public URL: $ACTIVE_URL"
        if curl -s -m 4 "$ACTIVE_URL/api/wards" >/dev/null 2>&1 || curl -s -m 4 --doh-url https://1.1.1.1/dns-query "$ACTIVE_URL/api/wards" >/dev/null 2>&1; then
            echo "  ✓ Public URL is healthy & reachable!"
        else
            echo "  ⚠️ Public URL is not reachable (connection may have reset). Run './run_public.sh --daemon' to refresh."
        fi
    else
        echo "  ⚠️ No public URL file found ($URL_FILE)."
    fi
    exit 0
}

# Parse flags
DAEMON_MODE=0
for arg in "$@"; do
    case "$arg" in
        --daemon|-d|--bg|--background)
            DAEMON_MODE=1
            ;;
        --stop)
            stop_services
            ;;
        --status)
            show_status
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo "Unknown argument: $arg"
            show_help
            ;;
    esac
done

# ------------------------------------------------------------------------------
# 1. Environment & Dependencies Check
# ------------------------------------------------------------------------------
echo "=================================================================="
echo "🚀 NagrikAMC · Single-Command Public Server Launcher"
echo "=================================================================="

if [[ ! -d ".venv" ]]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if ! python -c "import fastapi, uvicorn, pydantic, PIL" 2>/dev/null; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

if [[ ! -f "app/static/samples/pothole_cg_road.jpg" || ! -f "app/static/samples/video/frame_1_t0s.jpg" ]]; then
    echo "🖼️ Generating sample civic assets..."
    python scripts/generate_sample_assets.py
fi

# ------------------------------------------------------------------------------
# 2. Start or Verify Backend Server on Port 8000
# ------------------------------------------------------------------------------
SERVER_WAS_RUNNING=0
if lsof -i:"$PORT" >/dev/null 2>&1; then
    echo "⚡ Port $PORT is already active. Using existing server instance."
    SERVER_WAS_RUNNING=1
else
    echo "🔧 Starting FastAPI server on port $PORT..."
    uvicorn app.main:app --host 0.0.0.0 --port "$PORT" > "$SERVER_LOG" 2>&1 &
    SERVER_PID=$!
    echo "$SERVER_PID" > "$SERVER_PID_FILE"
    
    # Wait for server to become responsive
    SERVER_READY=0
    for i in {1..15}; do
        if curl -s -m 1 "http://127.0.0.1:$PORT/" >/dev/null 2>&1; then
            SERVER_READY=1
            break
        fi
        sleep 1
    done

    if [[ "$SERVER_READY" -eq 1 ]]; then
        echo "  ✓ Server started successfully (PID: $SERVER_PID)"
    else
        echo "  ⚠️ Server started but waiting for initial response. Check $SERVER_LOG"
    fi
fi

# ------------------------------------------------------------------------------
# 3. Establish Public HTTPS Tunnel
# ------------------------------------------------------------------------------
echo "🌐 Establishing secure public HTTPS tunnel..."
rm -f "$TUNNEL_LOG" "$URL_FILE"

# Clean up any previous tunnel instances
pkill -f "cloudflared tunnel --url" 2>/dev/null || true
pkill -f "nokey@localhost.run" 2>/dev/null || true

TUNNEL_TYPE=""
if command -v cloudflared >/dev/null 2>&1; then
    TUNNEL_TYPE="cloudflared"
    echo "  Using Cloudflare Tunnel (cloudflared)..."
    nohup cloudflared tunnel --url "http://127.0.0.1:$PORT" > "$TUNNEL_LOG" 2>&1 &
    TUNNEL_PID=$!
    URL_REGEX="https://[a-zA-Z0-9.-]+\.trycloudflare\.com"
else
    TUNNEL_TYPE="ssh"
    echo "  Using zero-install SSH reverse tunnel (localhost.run)..."
    nohup ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
        -R 80:127.0.0.1:"$PORT" nokey@localhost.run > "$TUNNEL_LOG" 2>&1 &
    TUNNEL_PID=$!
    URL_REGEX="https://[a-zA-Z0-9.-]+\.lhr\.life"
fi

echo "$TUNNEL_PID" > "$TUNNEL_PID_FILE"

# Extract Public URL
PUBLIC_URL=""
for i in {1..25}; do
    if [[ -f "$TUNNEL_LOG" ]]; then
        PUBLIC_URL=$(grep -oE "$URL_REGEX" "$TUNNEL_LOG" | head -n 1 || true)
        if [[ -n "$PUBLIC_URL" ]]; then
            # If cloudflared, make sure it has registered connection
            if [[ "$TUNNEL_TYPE" == "cloudflared" ]]; then
                if grep -q "Registered tunnel connection" "$TUNNEL_LOG" 2>/dev/null; then
                    break
                fi
            else
                break
            fi
        fi
    fi
    sleep 1
done

if [[ -z "$PUBLIC_URL" ]]; then
    # Fallback to whatever URL was printed
    PUBLIC_URL=$(grep -oE "$URL_REGEX" "$TUNNEL_LOG" | head -n 1 || true)
fi

if [[ -z "$PUBLIC_URL" ]]; then
    echo "⚠️ Public URL extraction is taking longer than expected."
    echo "  Check tunnel output in: $TUNNEL_LOG"
else
    echo "$PUBLIC_URL" > "$URL_FILE"
    echo "$PUBLIC_URL" > "$SCRIPT_DIR/.public_url"
fi

# ------------------------------------------------------------------------------
# 4. Display Status Banner
# ------------------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "🎉 NagrikAMC / CivicPulse AI Agent is ONLINE!"
echo "=================================================================="
if [[ -n "$PUBLIC_URL" ]]; then
    echo "🌟 PUBLIC DEMO URL:     $PUBLIC_URL"
    echo "📱 Mobile / Remote:     $PUBLIC_URL"
fi
echo "💻 Local Browser:       http://localhost:$PORT"
echo "📚 Swagger API Docs:    http://localhost:$PORT/docs"
echo "📝 Server Log:          $SERVER_LOG"
echo "📡 Tunnel Log:          $TUNNEL_LOG"
echo "=================================================================="

# ------------------------------------------------------------------------------
# 5. Daemon Mode vs Foreground Handling
# ------------------------------------------------------------------------------
if [[ "$DAEMON_MODE" -eq 1 ]]; then
    echo "🚀 Running INDEFINITELY in the background."
    echo "   - View live tunnel log: tail -f $TUNNEL_LOG"
    echo "   - View live server log: tail -f $SERVER_LOG"
    echo "   - Check status:         ./run_public.sh --status"
    echo "   - Stop anytime with:    ./run_public.sh --stop"
    echo "=================================================================="
    exit 0
fi

# Cleanup handler for foreground mode
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    if [[ -n "${TUNNEL_PID:-}" ]]; then
        kill "$TUNNEL_PID" 2>/dev/null || true
    fi
    rm -f "$TUNNEL_PID_FILE" "$URL_FILE" "$SCRIPT_DIR/.public_url"
    
    if [[ "$SERVER_WAS_RUNNING" -eq 0 && -n "${SERVER_PID:-}" ]]; then
        kill "$SERVER_PID" 2>/dev/null || true
        rm -f "$SERVER_PID_FILE"
    fi
    echo "✅ Shutdown complete."
    exit 0
}

trap cleanup INT TERM

echo "👉 Running in foreground. Press [Ctrl + C] to stop."
echo "   (To run indefinitely in the background, use: ./run_public.sh --daemon)"
echo ""

# Keep alive & monitor tunnel
while true; do
    if ! kill -0 "$TUNNEL_PID" 2>/dev/null; then
        echo "⚠️ Tunnel disconnected. Reconnecting..."
        if [[ "$TUNNEL_TYPE" == "cloudflared" ]]; then
            nohup cloudflared tunnel --url "http://127.0.0.1:$PORT" > "$TUNNEL_LOG" 2>&1 &
        else
            nohup ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
                -R 80:127.0.0.1:"$PORT" nokey@localhost.run > "$TUNNEL_LOG" 2>&1 &
        fi
        TUNNEL_PID=$!
        echo "$TUNNEL_PID" > "$TUNNEL_PID_FILE"
    fi
    sleep 5
done
