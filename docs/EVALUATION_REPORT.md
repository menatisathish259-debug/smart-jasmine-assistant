# 📈 Smart Jasmine Farming Assistant: Evaluation Report & Limitations

**Crop:** *Jasminum sambac* (Gundu Malli / குண்டு மல்லி)  
**Model Architecture:** MobileNetV2 Transfer Learning  
**Evaluation Methodology:** Leakage-Safe Held-Out Test Split with Commercial Risk Analysis  

---

## 1. Ground Truth Dataset Audit

An audit of the raw dataset directories was conducted prior to model deployment:

```
data/raw/single_buds/
├── READY_TO_PLUCK/          (0 real grower photographs)
├── NOT_READY/               (0 real grower photographs)
├── TOO_OPEN/                (0 real grower photographs)
└── DAMAGED_OR_ABNORMAL/     (0 real grower photographs)
```

### Status & Ethical Principle:
- **Dataset Sufficiency Status:** 🔴 **INSUFFICIENT FOR COMMERCIAL PRODUCTION TRAINING**.
- **Engineering Ethics Enforcement:** In strict compliance with scientific honesty and user safety rules, the system **never hallucinates or invents fake accuracy percentages**.
- **Defensive Gatekeeper Verification:** Invoking the training pipeline on empty directories halts gracefully with status `ABORTED_INSUFFICIENT_DATA` and outputs:
  > *"Cannot train: Classes have 0 labeled photos. Please label at least 15-20 photos per stage before running exploratory training."*

---

## 2. Evaluation Pipeline Verification (Mock Checkpoint)

To verify the mathematical and structural correctness of the inference and evaluation engines before large-scale field data collection, an isolated MobileNetV2 checkpoint was compiled and tested:

### Mathematical Distribution Verification:
- **Output Dimensions:** $1 \times 4$ Softmax probability vector corresponding to `[READY_TO_PLUCK, NOT_READY, TOO_OPEN, DAMAGED_OR_ABNORMAL]`.
- **Probability Summation:** $\sum_{i=1}^{4} P(C_i) = 100.00\%$ (verified within $\pm 0.05\%$).
- **Uncertainty Calibration:** Computed as $U = 1.0 - \max(P(C_i))$. For a top confidence of $82.4\%$, uncertainty is correctly estimated as $0.176$.
- **Mandatory Safety Disclaimer:** Verified on every inference output:
  > *"⚠️ EXPERIMENTAL AI PREDICTION: Model trained on small experimental dataset. Confidence reflects statistical image similarity, not guaranteed harvest readiness. The grower's field inspection is the ultimate ground truth."*

---

## 3. Commercial Harvest Risk Metrics ([src/models/evaluator.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/models/evaluator.py))

In commercial jasmine floriculture, overall classification accuracy is an incomplete metric because different misclassification errors carry drastically different economic penalties. The evaluator computes:

```
                       PREDICTED
                READY   NOT_READY  TOO_OPEN  DAMAGED
ACTUAL  READY     TP       E12       E13       E14
    NOT_READY   [E21]       TN       E23       E24    <-- Critical Risk 1 (Premature Plucking)
     TOO_OPEN    E31       E32        TN       E34
      DAMAGED   [E41]       E42       E43        TN    <-- Critical Risk 2 (Defective Packing)
```

1. **Risk 1: Premature Plucking False Positives ($E_{21}$):**
   - *Condition:* Actual `NOT_READY` bud predicted as `READY_TO_PLUCK`.
   - *Commercial Impact:* Immature green buds plucked prematurely suffer post-harvest desiccation, lose up to 35% weight during transit, and fail to open, resulting in direct revenue loss.
2. **Risk 2: Defective Packing False Positives ($E_{41}$):**
   - *Condition:* Actual `DAMAGED_OR_ABNORMAL` bud predicted as `READY_TO_PLUCK`.
   - *Commercial Impact:* Including bored or rotting buds in commercial Grade A flower parcels causes severe trader penalties and rejection at wholesale flower markets (e.g. Mattuthavani Flower Market, Madurai).

---

## 4. Test Suite Summary (62/62 Passing)

The entire software pipeline has been verified via 62 automated unit and integration tests:

| Test Module | Coverage Domain | Tests | Status |
|---|---|---|---|
| [tests/test_delivery.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_delivery.py) | End-to-end multi-page compilation, SQLite WAL, image upload validation, error bounds, uncertainty scoring, recommendation safeguards | 8 | ✅ PASSED |
| [tests/test_agronomy.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_agronomy.py) | FCO fertilizer formulation verification, nutrient stoichiometry, TNAU split doses, symptom-diagnosis separation, expert referral triggers | 19 | ✅ PASSED |
| [tests/test_database.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_database.py) | SQLite schema creation, foreign keys, privacy isolation (no GPS), CRUD operations across all tables | 8 | ✅ PASSED |
| [tests/test_dataset.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_dataset.py) | SHA-256 exact matching, perceptual dHash duplicate detection, leak-free stratified splits, whole-plant segregation | 7 | ✅ PASSED |
| [tests/test_model.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_model.py) | MobileNetV2 architecture, layer freezing/unfreezing, empty dataset aborts, evaluator error handling, cached inference | 5 | ✅ PASSED |
| [tests/test_validation.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_validation.py) | Soil pH validation, fertilizer thresholds, harvest inputs, image format and dimension verification | 8 | ✅ PASSED |
| [tests/test_setup.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/tests/test_setup.py) | Directory structure, settings constants, TNAU harvest guidance, logger initialization, app compilation | 7 | ✅ PASSED |
| **Total** | **Full System Integration** | **62** | **100% PASSED** |

---

## 5. Known Limitations

1. **Visual Non-Specificity of Foliar Symptoms:**
   - Visual symptoms alone cannot differentiate between iron deficiency chlorosis, waterlogging root suffocation, and nematode galling. Visual analysis must be supplemented by soil pH tests and root inspection.
2. **Absence of Direct Chemical Prescriptions:**
   - By engineering design, the system prohibits automated chemical pesticide or fungicide dose recommendations from images. Growers must consult local horticulture officers or KVK scientists for authorized chemical formulations.
3. **Small-Dataset Experimental Status:**
   - Until the family farm gathers at least 150+ verified photographs per maturity stage, all vision classifications are classified as experimental software verification only.
4. **Microclimate & Sensor Gaps:**
   - Regional weather forecasts represent city-level metrics (`Madurai`). On-site ground microclimates and subsoil drainage must be verified manually at the bed level.
