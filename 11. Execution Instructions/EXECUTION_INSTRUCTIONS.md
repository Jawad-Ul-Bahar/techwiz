# AssureX Claim Engine - Execution Instructions

## 1-Click Launch (Windows)
Double-click `run_app.bat` in the project root:
- Automatically verifies `.venv` environment and dependencies
- Automatically opens browser at `http://127.0.0.1:8000`
- Starts the FastAPI Uvicorn application server with live reload

## Manual Terminal Launch
```bash
.venv\Scripts\python.exe -m uvicorn src.assurex_claim_engine.web.app:app --host 127.0.0.1 --port 8000 --reload
```

## Evaluator / Demo Login Credentials
| Role | Email | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| Administrator | admin@assurex.com | Admin1234! | Full Analytics, Rule Policy Manager, Audit Logs, Settings |
| Reviewer / Adjuster | reviewer@assurex.com | Reviewer1234! | Manual Review Queue, Dossier Adjudication, Overrides |
| Customer | customer@assurex.com | Customer1234! | Claim Intake, Document Vault, Repair History, Track Status |

## Automated Test Execution
To execute all 18 automated test suites:
```bash
.venv\Scripts\python.exe -m pytest tests/
```
