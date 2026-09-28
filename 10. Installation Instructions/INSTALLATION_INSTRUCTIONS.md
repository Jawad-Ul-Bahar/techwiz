# AssureX Claim Engine - Installation Instructions

## System Prerequisites
- Operating System: Windows 10 / 11, macOS, or Ubuntu Linux
- Python Version: Python 3.10 to 3.14 (Python 3.11/3.12 recommended)
- Package Manager: pip or uv (recommended)
- Tesseract OCR: (Optional for document intake scanned PDFs/Images)

## Step-by-Step Installation

### Step 1: Open Project Directory
```bash
cd "assurex-claim-engine abdullah"
```

### Step 2: Create Python Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment
- Windows: `.venv\Scripts\activate`
- macOS / Linux: `source .venv/bin/activate`

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Verify Model Files
Ensure that:
- Python tabular models are in `model/v2/`
- Google Teachable Machine models are in `GTM Models/`
- Policy rules are in `policies/`
- SQLite database is initialized in `database/assurex.db`

Installation is complete!
