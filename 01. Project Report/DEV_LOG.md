# AssureX Claim Engine - Developer Log (`DEV_LOG.md`)

## Phase 0: Diagnose Only
- **Date:** 2026-09-24
- **Work Done:**
  - Ran baseline test suite (`pytest tests/ -v`).
  - Added Windows OpenBLAS/OMP thread safety settings to `tests/conftest.py` (`OPENBLAS_NUM_THREADS=1`) to eliminate memory allocation aborts on Windows.
  - Investigated 0/30 predicted-class match in `reports/model_comparison_report.md` for the image classifier.
  - Investigated 100% accuracy of the tabular model and inspected features vs generator logic for data leakage.
  - Audited comparison thresholds, policy JSON rule decoupling, and PDF OCR handling.
  - Fixed the inference label mapping in `src/assurex_claim_engine/models/image_classifier.py` so class probabilities dynamically conform to `labels.json` (`ImageFolder` alphabetical ordering) rather than the fixed `CLASSES` list.
- **Problems Identified:**
  - **Image Classifier 0/30 Root Cause:** `ImageFolder` alphabetical order is `0: Invalid Claim`, `1: Manual Review`, `2: Valid Claim` (saved in `labels.json`), but `predict_image()` indexed into `["Valid Claim", "Invalid Claim", "Manual Review"]`, shifting all predicted classes by 1 slot.
  - **Tabular Model 100% Accuracy Root Cause:** Data leakage from deterministic rule synthesis. The generator's target class is a pure deterministic boolean function of `remaining_warranty_days`, `damage_type`, `has_unauthorized_repairs`, `contradiction_flag`, `duplicate_claim_flag`, `serial_match_status`, and `missing_documents_count`.
  - **Thresholds & Policies:** Model comparison thresholds (0.60, 0.10, 0.25) are hardcoded in `comparison.py`. PDF uploads are not handled in `DocumentOCRParser` (only image files supported by EasyOCR).
- **Changes Made:**
  - `tests/conftest.py`: Added thread limit environment variables.
  - `src/assurex_claim_engine/models/image_classifier.py`: Corrected class index mapping at inference from `labels.json`.
  - `pytest tests/ -v`: 6 passed in 11.53s (100%).

## Step 2: Fix App Browser Hang
- **Date:** 2026-09-24
- **Root Cause:** Python cold-start imports (torch, sklearn, xgboost, PIL, fastapi) take ~6-7s before uvicorn can bind the port. Models then loaded in <0.20s via background thread. The browser, opened immediately after the `uvicorn` command, gets "connection refused" during the import window and shows a spinner.
- **Diagnosis Evidence:**
  - Cold start measured: first HTTP response at 6.78-9.5s from process launch.
  - Startup log (after fix): DB ready 0.02s, tabular model 0.04s, vision model 0.05s, all models ready 0.10s — all in background thread.
  - The ~6-7s is pure Python import time (unavoidable without a pre-warmed interpreter).
- **Fix Applied (`src/assurex_claim_engine/web/app.py`):**
  - Added `import time, threading` at top.
  - Moved `tabular_classifier.load_artifacts()` and `vision_classifier.load_model()` into `_load_models_background()` — a daemon thread spawned by `startup_event()`.
  - `startup_event()` now returns in <0.05s (only init_db), so uvicorn accepts requests as soon as Python finishes importing.
  - Added `_models_ready` flag; `/claims/submit` spins up to 15s if flag is False, returns 503 if still not ready.
  - Added `/health` endpoint that instantly reports `{"status":"ok","models_ready":true/false}`.
- **Route Timing Table (warm server):**

| Route | Status | Time |
|-------|--------|------|
| GET / | 200 | 0.05s |
| GET /claims/new | 200 | 0.02s |
| GET /reviewer/queue | 200 | 0.02s |
| GET /admin/analytics | 200 | 0.03s |
| GET /docs | 200 | 0.01s |
| GET /health | 200 | <0.01s |
| POST /claims/submit (warm) | 303 | 0.49s |
| GET /claims/view/CLM-* | 200 | 0.14s |

- **Tests Run:** `pytest tests/ -v`: **6 passed in 5.10s** (all pass after fix).
- **E2E Test:** Full claim submission CLM-2026-0003 completed end-to-end in 0.49s (models warm).

## Phase 6: Live Claim Summary Card Derived Features Data-Pipeline Fix
- **Date:** 2026-09-26
- **Root Cause Confirmed:** `render_claim_card()` in `app.py` was generating live Summary Card images from incomplete live form payloads missing derived/computed fields (`product_age_days`, `remaining_warranty_days`, `warranty_start_date`, `warranty_expiry_date`, `serial_match_status`, `contradiction_flag`, `missing_documents_count`, `has_receipt`, etc.). This caused live summary cards to contain default/missing values, leading the Vision Model to collapse to "Manual Review".
- **Changes Made:**
  - Standardized `compute_derived_claim_features(raw_claim)` in `src/assurex_claim_engine/decision/derived_features.py` to compute exact 30-day warranty expiry, age, remaining warranty, serial status (user vs OCR), missing documents, and contradiction flags (`ContradictionAndDuplicateDetector`).
  - Refactored `dataset_generator/generate_dataset_v2.py` to utilize `compute_derived_claim_features(raw_record)` so training and live feature generation use the exact same logic.
  - Wired `compute_derived_claim_features` into live `/claims/submit` and `/claims/import-csv` routes in `src/assurex_claim_engine/web/app.py` BEFORE calling `render_claim_card()`.
  - Added regression test `test_07_live_submission_derived_features_regression` in `tests/test_scenarios.py`.
- **Verification Results:**
  - 8-claim live verification executed across diverse scenarios: Vision model predictions vary properly (`Valid Claim`, `Invalid Claim`, `Manual Review`) and align with human expectation without retraining any model.
  - `pytest`: All 18 tests passed cleanly (100%).



## Phase 7: Google Teachable Machine (GTM) Integration
- **Date:** 2026-09-26
- **Work Done:** Replaced PyTorch MobileNetV2 with Google Teachable Machine (Keras/TensorFlow) model to strictly comply with Aptech SRS Deliverable 5. Updated `image_classifier.py` to load `.h5` model and `labels.txt` from the `GTM Models/` directory. Normalized image array using `(image / 127.5) - 1.0` to match GTM inference specification.
- **Verification Results:** Successfully classified GTM model images, predicting accurately without PyTorch dependency.
