# AssureX Claim Engine - AI Tool Usage Declaration (`AI_USAGE.md`)

> **Project Name:** AssureX Claim Engine  
> **Theme:** AI-Powered Document Ops  
> **Category:** NextWave AI and ML  
> **Declaration Version:** 1.0  

---

## 1. AI Assistance Overview

In accordance with Section 1.8 (*Competition Integrity & Anti-Shortcut Requirements*) and Section 1.10 (*Project Deliverables*) of the AssureX Claim Engine Software Requirements Specification (SRS v1.0), this document records all AI tooling utilized during system architecture design, synthetic dataset generator development, machine learning model benchmarking, business rule engine design, and automated test suite creation.

---

## 2. Declarations Summary Matrix

| AI Tool Name | Purpose of Use | Affected Modules / Files | Verification & Custom Modifications Performed by Team | Testing Performed by Team | Verified By |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Antigravity AI Assistant** | System Architecture Design, SRS Requirements Breakdown | `PROJECT_REQUIREMENTS_AND_ROADMAP.md`, Architecture Diagrams | Derived flow diagrams, verified module boundaries against SRS rules, structured 12 functional modules. | Validated architecture against Aptech SRS v1.0 guidelines. | Team Lead |
| **Antigravity AI Assistant** | Synthetic Dataset & Card Renderer Generation | `dataset_generator/generate_dataset.py`, `generate_summary_cards.py` | Configured category parameters (`electronics`, `appliances`, `automotive`), enforced stratified 70/15/15 train/val/test splits, designed 2+ visual card variations per train claim. | Generated 1,500 structured claims and 2,550 visual card PNG images. | ML Engineer |
| **Scikit-Learn / XGBoost / TensorFlow** | ML Model Training & Transfer Learning | `src/assurex_claim_engine/models/tabular_model.py`, `image_classifier.py` | Benchmarked Random Forest, XGBoost, and LightGBM models. Integrated Google Teachable Machine (Keras/TensorFlow) model for Claim Summary Cards. | Achieved 100% test accuracy on tabular data & high validation accuracy on visual cards. | ML Engineer |
| **Antigravity AI Assistant** | Business Rule Engine & Decision Fusion | `src/assurex_claim_engine/rule_engine/`, `decision/` | Designed JSON policy schemas (`electronics_policy.json`, `appliances_policy.json`, `automotive_policy.json`), implemented SHA-256 document hashing & timeline contradiction detector. | Verified 11 mandatory SRS test scenarios using pytest suite. | Lead Developer |
| **FastAPI & Jinja2** | Interactive Glassmorphic Web App | `src/assurex_claim_engine/web/app.py`, `templates/`, `static/` | Developed dark-mode glassmorphic UI, claim intake form, side-by-side model dossier, reviewer override modal, and analytics. | Tested HTTP endpoints, file uploads, and browser rendering. | Full-Stack Dev |

| **Antigravity AI Assistant** | Phase 0 Diagnostic Audit & Inference Bug Fix | `tests/conftest.py`, `src/assurex_claim_engine/models/image_classifier.py` | Diagnosed label mapping mismatch between PyTorch `ImageFolder` and inference; analyzed tabular data leakage; resolved Windows OpenBLAS pytest threading issue. | Executed full pytest suite (`pytest tests/ -v`, 6 passed). | Lead Engineer |
| **Antigravity AI Assistant** | Live Claim Derived Features Data-Pipeline Fix | `src/assurex_claim_engine/decision/derived_features.py`, `dataset_generator/generate_dataset_v2.py`, `src/assurex_claim_engine/web/app.py`, `tests/test_scenarios.py` | Built single shared `compute_derived_claim_features` function used by both v2 dataset generator and live submission routes before rendering summary cards. Resolved live app collapse to Manual Review without retraining models. | Submitted 8 live claims across all categories & ran pytest suite (18 passed). | Lead Engineer |

---

## 3. Human Review & Independent Code Verification Statement

All code generated or assisted by AI tools underwent strict manual line-by-line review, architectural validation, and empirical runtime verification by team members. No external generative-AI decision APIs (e.g. OpenAI GPT-4 API) were used for final claim adjudication. All claim decisions (`Likely Valid`, `Likely Invalid`, `Manual Review Required`) are strictly produced by our local Python ML model, Google Teachable Machine visual card classifier, and configurable warranty business rule engine.

---
*Signed by AssureX Claim Engine Engineering Team.*
