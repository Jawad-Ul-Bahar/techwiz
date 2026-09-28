@echo off
title AssureX Claim Engine - Web Application Server
cd /d "%~dp0"

echo =====================================================================
echo    AssureX Claim Engine - Enterprise AI Warranty Adjudication Platform
echo =====================================================================
echo.

set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONPATH=src;.;%PYTHONPATH%

echo [1/3] Checking environment and dependencies...
set PYTHON_EXE=
if exist ".venv\Scripts\python.exe" set PYTHON_EXE=.venv\Scripts\python.exe
if not defined PYTHON_EXE if exist "..\.venv\Scripts\python.exe" set PYTHON_EXE=..\.venv\Scripts\python.exe

if not defined PYTHON_EXE (
    echo Python virtual environment not found.
    pause
    exit /b 1
)

echo [2/3] Opening browser at http://127.0.0.1:8000...
start "" "http://127.0.0.1:8000"

echo [3/3] Launching Web Application Server...
echo.

%PYTHON_EXE% -m uvicorn src.assurex_claim_engine.web.app:app --host 127.0.0.1 --port 8000 --reload

pause
