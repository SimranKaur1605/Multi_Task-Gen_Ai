@echo off
title GenAI Studio Launcher
color 0A

echo.
echo  ==========================================
echo    GenAI Studio -- Auto Launcher
echo  ==========================================
echo.

:: ── Check Python ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install from https://python.org
    pause
    exit /b
)

:: ── Create venv if missing ────────────────────────────────
if not exist ".venv" (
    echo  [SETUP] Creating virtual environment...
    python -m venv .venv
)

:: ── Activate venv ─────────────────────────────────────────
call .venv\Scripts\activate.bat

:: ── Install dependencies ──────────────────────────────────
echo  [SETUP] Installing / verifying dependencies...
pip install -r requirements.txt -q

:: ── Check .env ────────────────────────────────────────────
if not exist ".env" (
    echo  [WARN] .env file not found!
    echo  Create a .env file with:  GROQ_API_KEY=your_key_here
    pause
    exit /b
)

:: ── Launch FastAPI backend in background ──────────────────
echo.
echo  [START] Starting FastAPI backend on http://localhost:8000 ...
start "GenAI Backend" cmd /k "call .venv\Scripts\activate.bat && uvicorn main:app --reload --port 8000"

:: ── Wait a moment for server to boot ─────────────────────
timeout /t 2 /nobreak >nul

:: ── Open frontend in default browser ─────────────────────
echo  [START] Opening frontend in browser...
start "" "%~dp0frontend\index.html"

echo.
echo  ==========================================
echo   Both services are running!
echo   Backend : http://localhost:8000
echo   Frontend: frontend/index.html
echo   Close the backend window to stop.
echo  ==========================================
echo.
pause
