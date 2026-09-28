"""
AssureX Claim Engine - 30-Claim Model Comparison Report Generator
Evaluates 30 unseen test claims using:
1. Python Tabular ML Model
2. Visual Claim Summary Card Image Classifier
3. Dual-Model Comparator
4. Configurable Warranty Business Rule Evaluator
5. Decision Fusion Engine

Generates 'reports/model_comparison_report.md'
"""

import os
import sys
import types

# Ensure the project root (parent of this 'reports/' folder) is on sys.path
# so that top-level packages like `dataset_generator` can be imported regardless
# of what the current working directory is when this script is executed.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import pandas as pd
from PIL import Image

from assurex_claim_engine.models.tabular_model import TabularClaimClassifier
from assurex_claim_engine.models.image_classifier import ImageClassifierPipeline
from assurex_claim_engine.decision.fusion import DecisionFusionEngine
from dataset_generator.generate_summary_cards import render_claim_card

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_30_claim_report():
    print("Generating 30-Claim Model Comparison Report...")
    test_csv_path = "data/v2/test.csv" if os.path.exists("data/v2/test.csv") else "data/test.csv"
    test_df = pd.read_csv(test_csv_path).head(30)

    tabular_model = TabularClaimClassifier()
    tabular_model.load_artifacts()

    image_pipeline = ImageClassifierPipeline()
    fusion_engine = DecisionFusionEngine()

    report_rows = []
    
    match_count = 0
    disagreement_count = 0
    final_decisions_summary = {"Likely Valid": 0, "Likely Invalid": 0, "Manual Review Required": 0}

    for idx, row in test_df.iterrows():
        claim_dict = row.to_dict()
        claim_id = row["claim_id"]
        actual_class = row["actual_class"]

        # 1. Tabular Model Prediction
        py_res = tabular_model.predict_single(claim_dict)

        # 2. Render Card & Get Vision Prediction
        card_img = render_claim_card(row, variation_id=1)
        vis_res = image_pipeline.predict_image(card_img)

        # 3. Decision Fusion
        decision_dossier = fusion_engine.evaluate_full_claim(claim_dict, py_res, vis_res)

        comp = decision_dossier["comparison"]
        rule_eval = decision_dossier["rule_evaluation"]
        contra = decision_dossier["contradictions"]
        dups = decision_dossier["duplicates"]
        final_dec = decision_dossier["final_decision"]

        if comp["classes_match"]:
            match_count += 1
        else:
            disagreement_count += 1

        final_decisions_summary[final_dec] = final_decisions_summary.get(final_dec, 0) + 1

        card_filename = f"{claim_id}_v1.png"

        report_rows.append({
            "claim_id": claim_id,
            "actual_class": actual_class,
            "py_class": py_res["predicted_class"],
            "py_valid_conf": py_res["probabilities"].get("Valid Claim", 0.0),
            "py_invalid_conf": py_res["probabilities"].get("Invalid Claim", 0.0),
            "py_review_conf": py_res["probabilities"].get("Manual Review", 0.0),
            "card_filename": card_filename,
            "vis_class": vis_res["predicted_class"],
            "vis_valid_conf": vis_res["probabilities"].get("Valid Claim", 0.0),
            "vis_invalid_conf": vis_res["probabilities"].get("Invalid Claim", 0.0),
            "vis_review_conf": vis_res["probabilities"].get("Manual Review", 0.0),
            "match_status": "MATCH" if comp["classes_match"] else "DISAGREEMENT",
            "conf_diff": comp["confidence_difference"],
            "consistency_status": comp["consistency_status"],
            "rules_passed": len(rule_eval["passed_rules"]),
            "rules_failed": len(rule_eval["failed_rules"]),
            "missing_docs": ", ".join(rule_eval["missing_documents"]) if rule_eval["missing_documents"] else "None",
            "contradictions": len(contra["contradictions"]),
            "duplicate_flag": "YES" if dups["is_duplicate"] else "NO",
            "final_decision": final_dec
        })

    # Build Markdown Report Output
    md_content = r"""# AssureX Claim Engine - 30-Claim Model Comparison Report

> **Evaluation Date:** """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + r"""  
> **Total Test Claims Analyzed:** 30 Unseen Records  

---

## Executive Summary Metrics

| Metric Name | Value / Result |
| :--- | :--- |
| **Total Claims Evaluated** | 30 Claims |
| **Model Predictions Match Rate** | """ + f"{match_count} / 30 ({round(match_count/30*100, 1)}%)" + r""" |
| **Model Disagreements** | """ + f"{disagreement_count} Claims" + r""" |
| **Final Decisions Breakdown** | """ + f"Valid: {final_decisions_summary.get('Likely Valid', 0)} | Invalid: {final_decisions_summary.get('Likely Invalid', 0)} | Manual Review: {final_decisions_summary.get('Manual Review Required', 0)}" + r""" |

---

## Detailed 30-Claim Adjudication Log

| Claim ID | Actual Class | Python ML Class (Conf) | Vision Model Class (Conf) | Match Status | Conf Diff | Consistency Status | Missing Docs | Final Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for r in report_rows:
        py_str = f"{r['py_class']} ({r['py_valid_conf']:.2f}/{r['py_invalid_conf']:.2f}/{r['py_review_conf']:.2f})"
        vis_str = f"{r['vis_class']} ({r['vis_valid_conf']:.2f}/{r['vis_invalid_conf']:.2f}/{r['vis_review_conf']:.2f})"
        md_content += f"| `{r['claim_id']}` | {r['actual_class']} | {py_str} | {vis_str} | **{r['match_status']}** | {r['conf_diff']:.4f} | {r['consistency_status']} | {r['missing_docs']} | `{r['final_decision']}` |\n"

    md_content += """

---

## Major Disagreements & Edge Case Analysis

1. **Model Disagreements:**  
   Claims where the Python tabular model and Vision Summary Card model predict different classes are automatically flagged and routed to the **Manual Review Queue** to prevent false automated decisions.

2. **Rule Hard Fails vs AI Predictions:**  
   If business rules detect expired warranties, excluded damages, or unauthorized repairs, the **Decision Fusion Engine** overrides positive model confidence and enforces `Likely Invalid` or `Manual Review Required`.

---
*Report generated automatically by AssureX Claim Engine Verification Suite.*
"""

    with open("reports/model_comparison_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print("30-Claim Model Comparison Report saved to 'reports/model_comparison_report.md'")

if __name__ == "__main__":
    generate_30_claim_report()
