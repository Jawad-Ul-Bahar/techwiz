# AssureX Claim Engine - AI-Powered Warranty Adjudication Platform

> **Project Name:** AssureX Claim Engine  
> **Theme:** AI-Powered Document Ops  
> **Category:** NextWave AI and ML  
> **Specification:** Aptech SRS v1.0 Compliance  
> **Version:** 2.0.0 Enterprise Release  

---

## 📁 Aptech Techwiz Final Submission Structure (01 to 18)

The project has been structured according to the official **Final Submission Checklist**:

```
assurex-claim-engine/
│
├── 01. Project Report/                      # Comprehensive SRS Project Report & Architecture
├── 02. Complete Source Code/                # Full runnable application source code
│   ├── src/                                 # FastAPI application, OCR pipeline, ML inference
│   ├── static/                              # Vanilla CSS design system & icons
│   ├── templates/                           # Responsive Jinja2 templates & pagination
│   ├── database/                            # SQLite database (assurex.db)
│   ├── model/                               # Trained XGBoost & Scikit-Learn model artifacts
│   ├── GTM Models/                          # Teachable Machine Keras H5 & labels
│   ├── policies/                            # Category warranty policy rules (JSON)
│   ├── uploads/                             # Document vault storage
│   ├── tests/                               # Automated verification test suites
│   ├── dataset_generator/                   # Synthetic claim & visual card generators
│   ├── run_app.bat                          # 1-Click application launcher
│   ├── requirements.txt                     # Dependencies specification
│   └── pyproject.toml                       # Project metadata & build settings
│
├── 03. Structured Warranty Claim Dataset/   # Tabular dataset (train, val, test CSVs & metadata)
├── 04. Claim Summary Card Image Dataset/    # Visual summary cards split by class
├── 05. Python Model Files/                  # Saved ML joblib models & Jupyter notebooks
├── 06. Google Teachable Machine Model Files/# Google Teachable Machine Keras model & labels
├── 07. Warranty Policy Files/               # Category-specific warranty policy rules (JSON)
├── 08. Model Comparison Report/             # Dual-model comparison analysis & generator script
├── 09. Test Cases and Results/              # Audit report, manual test guide & test suites
├── 10. Installation Instructions/           # Setup & dependency installation guide
├── 11. Execution Instructions/              # 1-Click & CLI execution instructions
├── 12. Public GitHub Repository URL/        # GitHub repository information
├── 13. Deployment URL/                      # Deployed live application access & demo credentials
├── 14. Demonstration Video/                 # Video walkthrough link & timestamp index
├── 15. Technical Blog Link/                 # Technical publication article & key takeaways
├── 16. AI Tool Usage Declaration/           # AI assistance declaration per competition rules
├── 17. Team Contribution Record/            # Team members, roles & module contributions
├── 18. Final Submission Checklist/          # Official submission checklist & status index
│
├── run_app.bat                              # Root 1-Click launcher
└── README.md                                # Project documentation
```

---

## 🚀 How to Run the Application

### Option A: 1-Click Launch (Recommended)
Double-click **`run_app.bat`** in the project root:
- Automatically loads the virtual environment
- Launches the web server at `http://127.0.0.1:8000`
- Opens your browser automatically

### Option B: Command Line Launch
```bash
cd "02. Complete Source Code"
..\.venv\Scripts\python.exe -m uvicorn src.assurex_claim_engine.web.app:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🔑 Demo Login Accounts

| Role | Email | Password | Access Privileges |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@assurex.com` | `admin123` | Full Analytics, Policy Rule Manager, Audit Logs, Settings |
| **Claim Reviewer** | `reviewer@assurex.com` | `reviewer123` | Manual Review Queue, Dossier Review, Overrides |
| **Service Center** | `service@assurex.com` | `service123` | Log Repair Records, Product Search |
| **Customer** | `customer@assurex.com` | `customer123` | File Claims, Upload Invoices, Track Warranties |
