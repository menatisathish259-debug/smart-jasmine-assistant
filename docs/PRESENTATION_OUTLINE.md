# 🎯 Smart Jasmine Farming Assistant: Presentation Outline
## Slide-by-Slide Deck Outline for Project Defense / Agritech Showcase

---

### Slide 1: Title & Overview
- **Title:** Smart Jasmine Farming Assistant (ஸ்மார்ட் மல்லி விவசாய உதவியாளர்)
- **Subtitle:** An AI-Powered Decision Support and Computer Vision System for Smallholder *Jasminum sambac* Cultivation
- **Presenter & Role:** AI Engineer & Agricultural Technology Advisor
- **Key Highlight:** Combining Edge Deep Learning with Verified TNAU Agronomy for Ground-Soil Jasmine Farms (1/4 to 1 Acre).

---

### Slide 2: Problem Statement & Field Motivation
- **The Crop:** *Jasminum sambac* (Gundu Malli) — delicate commercial crop with fragile daily market economics.
- **Key Field Challenges:**
  1. *Premature Harvesting:* Green buds lose 35% weight and fail to open, triggering price cuts at market.
  2. *Defective Packing:* Damaged/bored buds packed into Grade A hampers ruin wholesale market reputation.
  3. *Over-Fertilization with Urea:* Promotes rank vegetative shoots, bud shedding, and bud worm flare-ups.
  4. *Visual Misdiagnosis Hazards:* Treating nutrient chlorosis as a fungal disease leads to unnecessary chemical spraying.

---

### Slide 3: System Architecture (4-Tier Design)
- **Presentation:** Responsive Streamlit web app with native English and Tamil (`தமிழ்`) toggling.
- **Domain & Agronomy:** FCO fertilizer calculations, TNAU Jasmine Package of Practices, and multi-factor decision logic.
- **Machine Learning:** MobileNetV2 transfer learning with in-graph data augmentation and uncertainty calibration.
- **Persistence:** Local SQLite database with Write-Ahead Logging (WAL), 11 relational tables, and zero cloud lock-in.

---

### Slide 4: Computer Vision Pipeline: Flower Maturity Classification
- **4-Class Botanical & Market Taxonomy:**
  - `READY_TO_PLUCK` (Grade A Commercial White Bud)
  - `NOT_READY` (Immature Green Tight Bud)
  - `TOO_OPEN` (Bloomed Over-Open Flower)
  - `DAMAGED_OR_ABNORMAL` (Bored, Webbed, or Rotting Bud)
- **Data Leakage Defense:**
  - Cryptographic SHA-256 hash (exact duplicate removal).
  - 64-bit Perceptual dHash (burst-shot clustering with Hamming distance $\le 4$).
  - Strict segregation of whole-plant canopy photos for Phase 7 YOLO detection.

---

### Slide 5: Scientific Integrity & Evaluation Metrics
- **Engineering Honesty:** 0 real field samples = 🔴 **Insufficient for Production Training**.
- **No Hallucinated Accuracy:** The pipeline defensively halts with `ABORTED_INSUFFICIENT_DATA`.
- **Mathematical Uncertainty:** Returns full 4-class Softmax vectors + Uncertainty Score ($1.0 - \text{top\_confidence}$).
- **Commercial Risk Matrix:** Evaluates Premature Plucking False Positives ($E_{21}$) and Defective Packing False Positives ($E_{41}$).

---

### Slide 6: Plant Health Engine: Separating Symptoms from Causes
- **The Core Rule:** *Physical observation $\neq$ Confirmed clinical diagnosis.*
- **Visible Signs Checklist:** Older leaf yellowing, interveinal chlorosis, bud boreholes with frass, leaf curling, branch wilting.
- **Differential Hypotheses:** Evaluates contextual soil pH (alkaline soil weights iron chlorosis; poor drainage weights root suffocation).
- **Physical Verification Protocols:** Step-by-step guidance for grower physical testing (10x lens underleaf check, bud slicing).

---

### Slide 7: Fertilizer Accounting & Decision Support Engine
- **FCO Bag Label Verifier:** Checks guaranteed analyses ($N\%, P_2O_5\%, K_2O\%$) against government standards.
- **Elemental Stoichiometry:** Calculates total kilograms and **grams per bush ($g/\text{bush}$)** applied.
- **TNAU Annual Budget Alignment:** Tracks cumulative inputs against TNAU standards ($60\text{g N} : 120\text{g } P_2O_5 : 120\text{g } K_2O$).
- **Excess Nitrogen Safeguard:** Prominently warns against single applications $> 40\text{ g N/bush}$.

---

### Slide 8: Multi-Factor Agronomic Weather Advisory
- **Cross-Layer Synthesis:**
  - *Rain Hazard Rule:* 24h forecast rain $\ge 15\text{ mm} \rightarrow$ Hold Urea topdressing to prevent groundwater leaching.
  - *Heat Stress Rule:* Temperature $\ge 36^\circ\text{C} \rightarrow$ Avoid midday watering to prevent root scalding.
  - *Alkaline Soil Rule:* Soil $\text{pH} > 7.5 \rightarrow$ Foliar iron/zinc sprays rather than ineffective soil drenching.
- **Non-Prescription Safeguard:** Explicitly prohibits automated chemical pesticide dose prescriptions from photos.

---

### Slide 9: Verification, Testing & Mobile Usability
- **62 Automated Pytest Tests:** 100% passing across agronomy, database, validation, models, and delivery.
- **Mobile Usability:** Validated at $390\text{px} \times 844\text{px}$ viewport dimensions (collapsing grids, touch targets).
- **Expert Referral Triggers:** Automated referral to Krishi Vigyan Kendra (KVK) and block horticultural officers when damage exceeds 30%.

---

### Slide 10: Implemented Features vs Future Roadmap & Conclusion
- **Completed Today:**
  - Phases 1–5: Architecture, UI, SQLite, Dataset Partitioner, MobileNetV2 Pipeline.
  - Phases 8–10: Plant Health Engine, Fertilizer Accounting, Weather & Soil Integration.
  - End-to-End Delivery: 62 automated tests, user guides, setup scripts.
- **Planned Next Steps:**
  - Phase 6: Field Data Gathering (150+ photos/class) & Model Calibration.
  - Phase 7: Whole-Plant Multi-Bud Object Detection (YOLO).
  - Phase 11: IoT Soil Moisture Probe Telemetry.
- **Final Takeaway:** Smart Jasmine bridges state-of-the-art computer vision with grounded, responsible agronomic science to empower smallholder family farmers.
