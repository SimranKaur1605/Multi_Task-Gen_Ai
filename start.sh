#!/bin/bash
set -e

echo ""
echo "=========================================="
echo "   GenAI Studio -- Auto Launcher"
echo "=========================================="
echo ""

# ── Check Python ───────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found. Install from https://python.org"
    exit 1
fi

# ── Create venv if missing ─────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "[SETUP] Creating virtual environment..."
    python3 -m venv .venv
fi

# ── Activate ───────────────────────────────────────────────
source .venv/bin/activate

# ── Install dependencies ───────────────────────────────────
echo "[SETUP] Installing / verifying dependencies..."
pip install -r requirements.txt -q

# ── Check .env ─────────────────────────────────────────────
if [ ! -f ".env" ]; then
    echo "[WARN] .env file not found!"
    echo "Create a .env file with:  GROQ_API_KEY=your_key_here"
    exit 1
fi

# ── Start FastAPI backend ──────────────────────────────────
echo ""
echo "[START] Starting FastAPI backend on http://localhost:8000 ..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# ── Wait for server ────────────────────────────────────────
sleep 2

# ── Open frontend ──────────────────────────────────────────
FRONTEND="$(pwd)/frontend/index.html"
echo "[START] Opening frontend..."
if command -v xdg-open &>/dev/null; then
    xdg-open "$FRONTEND"           # Linux
elif command -v open &>/dev/null; then
    open "$FRONTEND"               # macOS
fi

echo ""
echo "=========================================="
echo " Backend running at http://localhost:8000"
echo " Frontend opened in your browser"
echo " Press Ctrl+C to stop everything"
echo "=========================================="
echo ""

# Keep script alive; kill backend on exit
trap "kill $BACKEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait $BACKEND_PID
