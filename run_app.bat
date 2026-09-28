@echo off
title AssureX Claim Engine - Web Application Server
cd /d "%~dp002. Complete Source Code"

echo =====================================================================
echo    AssureX Claim Engine - Enterprise AI Warranty Adjudication Platform
echo =====================================================================
echo.

REM Set thread-safety and Python import paths
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONPATH=src;.;%PYTHONPATH%

echo [1/3] Checking environment and dependencies...
if not exist "..\.venv\Scripts\python.exe" (
    echo Virtual environment not found in project root.
    echo Please ensure .venv is installed in the root folder.
    pause
    exit /b 1
)

echo [2/3] Opening browser at http://127.0.0.1:8000...
start "" "http://127.0.0.1:8000"

echo [3/3] Launching Web Application Server...
echo.

..\.venv\Scripts\python.exe -m uvicorn src.assurex_claim_engine.web.app:app --host 127.0.0.1 --port 8000 --reload

pause
