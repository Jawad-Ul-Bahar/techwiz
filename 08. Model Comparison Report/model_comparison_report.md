# AssureX Claim Engine - 30-Claim Model Comparison Report

> **Evaluation Date:** 2026-09-25 14:47:26  
> **Total Test Claims Analyzed:** 30 Unseen Records  

---

## Executive Summary Metrics

| Metric Name | Value / Result |
| :--- | :--- |
| **Total Claims Evaluated** | 30 Claims |
| **Model Predictions Match Rate** | 19 / 30 (63.3%) |
| **Model Disagreements** | 11 Claims |
| **Final Decisions Breakdown** | Valid: 6 | Invalid: 6 | Manual Review: 18 |

---

## Detailed 30-Claim Adjudication Log

| Claim ID | Actual Class | Python ML Class (Conf) | Vision Model Class (Conf) | Match Status | Conf Diff | Consistency Status | Missing Docs | Final Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CLM-2026-0148` | Valid Claim | Valid Claim (0.82/0.02/0.16) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1669 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-0591` | Manual Review | Manual Review (0.11/0.00/0.88) | Manual Review (0.00/0.00/1.00) | **MATCH** | 0.1171 | Acceptable Match | purchase_receipt | `Manual Review Required` |
| `CLM-2026-0834` | Invalid Claim | Invalid Claim (0.01/0.97/0.02) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.0291 | Strong Match | None | `Likely Invalid` |
| `CLM-2026-1124` | Manual Review | Manual Review (0.04/0.06/0.90) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.0891 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-1260` | Invalid Claim | Invalid Claim (0.01/0.93/0.06) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.0659 | Strong Match | None | `Likely Invalid` |
| `CLM-2026-1400` | Manual Review | Manual Review (0.14/0.15/0.71) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2777 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0599` | Manual Review | Manual Review (0.14/0.16/0.70) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2881 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0784` | Invalid Claim | Invalid Claim (0.00/0.89/0.11) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.1093 | Acceptable Match | None | `Likely Invalid` |
| `CLM-2026-0157` | Manual Review | Manual Review (0.14/0.15/0.71) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2807 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0761` | Manual Review | Manual Review (0.07/0.37/0.55) | Manual Review (0.00/0.00/1.00) | **MATCH** | 0.4471 | Uncertain Result | None | `Manual Review Required` |
| `CLM-2026-0569` | Valid Claim | Valid Claim (0.82/0.02/0.15) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1649 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-0262` | Valid Claim | Valid Claim (0.80/0.02/0.18) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1891 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-1281` | Manual Review | Manual Review (0.11/0.12/0.77) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2183 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0722` | Valid Claim | Valid Claim (0.88/0.05/0.07) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1070 | Acceptable Match | None | `Manual Review Required` |
| `CLM-2026-0534` | Valid Claim | Valid Claim (0.82/0.02/0.16) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1667 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-0814` | Valid Claim | Valid Claim (0.91/0.02/0.07) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.0798 | Strong Match | None | `Manual Review Required` |
| `CLM-2026-0260` | Valid Claim | Valid Claim (0.82/0.02/0.16) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1680 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-0164` | Manual Review | Manual Review (0.13/0.15/0.72) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2702 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0179` | Invalid Claim | Manual Review (0.08/0.35/0.57) | Manual Review (0.00/0.00/1.00) | **MATCH** | 0.4309 | Uncertain Result | None | `Manual Review Required` |
| `CLM-2026-0273` | Manual Review | Manual Review (0.12/0.07/0.81) | Invalid Claim (0.00/1.00/0.00) | **DISAGREEMENT** | 0.1862 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-1245` | Invalid Claim | Invalid Claim (0.03/0.95/0.02) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.0491 | Strong Match | None | `Likely Invalid` |
| `CLM-2026-0507` | Valid Claim | Valid Claim (0.80/0.02/0.18) | Valid Claim (0.99/0.00/0.01) | **MATCH** | 0.1836 | Acceptable Match | None | `Likely Valid` |
| `CLM-2026-0830` | Manual Review | Manual Review (0.15/0.04/0.81) | Manual Review (0.00/0.00/1.00) | **MATCH** | 0.1883 | Acceptable Match | None | `Manual Review Required` |
| `CLM-2026-0105` | Manual Review | Manual Review (0.07/0.04/0.89) | Invalid Claim (0.00/1.00/0.00) | **DISAGREEMENT** | 0.1108 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0379` | Invalid Claim | Invalid Claim (0.01/0.95/0.05) | Manual Review (0.00/0.00/1.00) | **DISAGREEMENT** | 0.0532 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0991` | Invalid Claim | Invalid Claim (0.02/0.97/0.02) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.0340 | Strong Match | None | `Likely Invalid` |
| `CLM-2026-1382` | Manual Review | Manual Review (0.11/0.12/0.77) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.2228 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0933` | Manual Review | Manual Review (0.12/0.01/0.87) | Valid Claim (0.99/0.00/0.01) | **DISAGREEMENT** | 0.1185 | Model Disagreement | None | `Manual Review Required` |
| `CLM-2026-0331` | Manual Review | Manual Review (0.12/0.01/0.87) | Manual Review (0.00/0.00/1.00) | **MATCH** | 0.1322 | Acceptable Match | purchase_receipt | `Manual Review Required` |
| `CLM-2026-1356` | Invalid Claim | Invalid Claim (0.02/0.96/0.02) | Invalid Claim (0.00/1.00/0.00) | **MATCH** | 0.0361 | Strong Match | None | `Likely Invalid` |


---

## Major Disagreements & Edge Case Analysis

1. **Model Disagreements:**  
   Claims where the Python tabular model and Vision Summary Card model predict different classes are automatically flagged and routed to the **Manual Review Queue** to prevent false automated decisions.

2. **Rule Hard Fails vs AI Predictions:**  
   If business rules detect expired warranties, excluded damages, or unauthorized repairs, the **Decision Fusion Engine** overrides positive model confidence and enforces `Likely Invalid` or `Manual Review Required`.

---
*Report generated automatically by AssureX Claim Engine Verification Suite.*
