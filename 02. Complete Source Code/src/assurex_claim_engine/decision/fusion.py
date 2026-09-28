"""
AssureX Claim Engine - Decision Fusion & Explanation Engine
Fuses all signals into the final adjudication decision:
1. Python Tabular ML Prediction & Confidence
2. Vision Summary Card Model Prediction & Confidence
3. Dual-Model Consistency Status
4. Configurable Business Rule Results (Hard Fail, Manual Review)
5. Contradiction & Duplicate Detection Flags

Final Decision Classes:
- 'Likely Valid'
- 'Likely Invalid'
- 'Manual Review Required'
"""

from typing import Dict, Any, List
from assurex_claim_engine.decision.comparison import DualModelComparator
from assurex_claim_engine.rule_engine.evaluator import PolicyRuleEvaluator
from assurex_claim_engine.decision.contradiction import ContradictionAndDuplicateDetector

class DecisionFusionEngine:
    def __init__(self):
        self.rule_evaluator = PolicyRuleEvaluator()

    def evaluate_full_claim(
        self,
        claim: Dict[str, Any],
        python_result: Dict[str, Any],
        vision_result: Dict[str, Any],
        existing_claims: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        # 1. Dual Model Comparison
        comparison = DualModelComparator.compare_models(python_result, vision_result)

        # 2. Business Rule Evaluation
        rule_eval = self.rule_evaluator.evaluate_claim(claim)

        # 3. Contradiction & Duplicate Detection
        contradiction_eval = ContradictionAndDuplicateDetector.detect_contradictions(claim)
        duplicate_eval = ContradictionAndDuplicateDetector.check_duplicate(claim, existing_claims)

        supporting_factors: List[str] = []
        opposing_factors: List[str] = []
        required_actions: List[str] = []

        # Start Decision Logic
        if rule_eval["hard_fail"]:
            final_decision = "Likely Invalid"
            opposing_factors.extend(rule_eval["failed_rules"])
        elif duplicate_eval["is_duplicate"] or contradiction_eval["has_contradictions"]:
            final_decision = "Manual Review Required"
            if duplicate_eval["is_duplicate"]:
                opposing_factors.extend(duplicate_eval["duplicate_reasons"])
                required_actions.append("Verify potential duplicate claim details with claimant.")
            if contradiction_eval["has_contradictions"]:
                opposing_factors.extend(contradiction_eval["contradictions"])
                required_actions.append("Inspect timeline inconsistencies and request revised invoice.")
        elif rule_eval["manual_review_required"]:
            final_decision = "Manual Review Required"
            opposing_factors.extend(rule_eval["manual_review_triggers"])
            if rule_eval["missing_documents"]:
                required_actions.append(f"Request missing documentation: {', '.join(rule_eval['missing_documents'])}")
        elif comparison["consistency_status"] in ["Model Disagreement", "Uncertain Result", "Weak Match"]:
            final_decision = "Manual Review Required"
            opposing_factors.append(f"AI Disagreement / Uncertainty ({comparison['consistency_status']}): {comparison['status_description']}")
            required_actions.append("Manual reviewer audit required due to model confidence discrepancy.")
        else:
            # Models agree and rules pass
            py_pred = python_result["predicted_class"]
            vis_pred = vision_result["predicted_class"]

            if py_pred == "Valid Claim" and vis_pred == "Valid Claim":
                final_decision = "Likely Valid"
                supporting_factors.append("Python ML model & Vision Classifier both predict 'Valid Claim' with strong confidence.")
                supporting_factors.extend(rule_eval["passed_rules"])
            elif py_pred == "Invalid Claim" and vis_pred == "Invalid Claim":
                final_decision = "Likely Invalid"
                opposing_factors.append("Python ML model & Vision Classifier both predict 'Invalid Claim'.")
                opposing_factors.extend(rule_eval["failed_rules"])
            else:
                final_decision = "Manual Review Required"
                opposing_factors.append(f"Borderline model predictions (Python: {py_pred}, Vision: {vis_pred}).")
                required_actions.append("Conduct manual inspection of claim dossier.")

        # Default action for valid claims
        if final_decision == "Likely Valid" and not required_actions:
            required_actions.append("Proceed with claim approval and service authorization.")
        elif final_decision == "Likely Invalid" and not required_actions:
            required_actions.append("Issue rejection notice specifying non-compliance reasons.")

        return {
            "claim_id": claim.get("claim_id", "CLM-UNKNOWN"),
            "final_decision": final_decision,
            "comparison": comparison,
            "rule_evaluation": rule_eval,
            "contradictions": contradiction_eval,
            "duplicates": duplicate_eval,
            "claim_dict": claim,
            "explanation": {
                "supporting_factors": supporting_factors,
                "opposing_factors": opposing_factors,
                "required_actions": required_actions
            }
        }

if __name__ == "__main__":
    fusion = DecisionFusionEngine()
    sample_claim = {
        "claim_id": "CLM-2026-0001",
        "product_category": "electronics",
        "has_receipt": True,
        "has_warranty_card": True,
        "has_product_photo": True,
        "has_serial_photo": True,
        "remaining_warranty_days": 180,
        "damage_type": "none",
        "fault_category": "motherboard_failure",
        "has_unauthorized_repairs": False,
        "serial_match_status": "Exact",
        "purchase_date": "2025-01-01",
        "fault_occurrence_date": "2026-05-01",
        "claim_submission_date": "2026-05-05"
    }
    py_res = {"predicted_class": "Valid Claim", "top_confidence": 0.96, "probabilities": {"Valid Claim": 0.96, "Invalid Claim": 0.02, "Manual Review": 0.02}}
    vis_res = {"predicted_class": "Valid Claim", "top_confidence": 0.92, "probabilities": {"Valid Claim": 0.92, "Invalid Claim": 0.05, "Manual Review": 0.03}}

    decision = fusion.evaluate_full_claim(sample_claim, py_res, vis_res)
    print("Fused Decision Result:")
    print(decision["final_decision"])
    print(decision["explanation"])
