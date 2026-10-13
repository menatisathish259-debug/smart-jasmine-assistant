# 🎓 Academic Project Report Outline
## Smart Jasmine: An AI-Powered Decision Support and Computer Vision Assistant for Smallholder Jasminum sambac Cultivation

---

### Abstract
Brief summary (250–300 words) detailing the socio-economic significance of *Jasminum sambac* (Gundu Malli) in Tamil Nadu, the agricultural challenges of smallholder farms (premature harvesting penalties, excessive nitrogen application, visual pest misdiagnosis), the proposed 4-tier system (Streamlit mobile UI, SQLite relational persistence, MobileNetV2 transfer learning, multi-factor agronomic reasoning), key findings, ethical safeguards, and experimental results.

---

### Chapter 1: Introduction
1.1 **Background & Agronomic Context:** *Jasminum sambac* cultivation in South India; fragrance industry and fresh flower garland markets.  
1.2 **Problem Statement:**  
  - Commercial revenue loss from premature bud picking and defective bud packing.  
  - Over-fertilization with Urea leading to excessive vegetative growth and pest vulnerability.  
  - Dangers of chemical pest prescriptions from photographs without physical root and soil verification.  
1.3 **Project Objectives:** Multi-phase smart assistant combining edge vision, nutrient accounting, and bilingual decision support.  
1.4 **Scope & Target Audience:** 1/4 to 1-acre ground soil family farms.  
1.5 **Report Organization.**

---

### Chapter 2: Literature Review & Agronomic Foundations
2.1 **Deep Learning in Precision Horticulture:** Survey of CNN architectures; lightweight edge models (MobileNetV2 vs ResNet vs EfficientNet).  
2.2 **Data Leakage in Agricultural Computer Vision:** Perceptual burst-shot similarities and the necessity of hashing-based partition grouping.  
2.3 **Tamil Nadu Agricultural University (TNAU) Package of Practices:**  
  - Annual nutrient recommendations ($60:120:120\text{ g NPK/bush/year}$ + FYM).  
  - Split application schedules (post-pruning basal vs flowering flush).  
2.4 **Fertilizer Control Order (FCO) Standards & Nutrient Stoichiometry:** Guaranteed analysis conversion to elemental inputs.  
2.5 **Entomological & Pathological Keys:** *Hendecasis duplifascialis* (Bud worm), *Contarinia maculipennis* (Midge), *Tetranychus urticae* (Mites), and *Sclerotium rolfsii* (Collar rot).

---

### Chapter 3: System Architecture & Database Design
3.1 **Architectural Paradigm:** 4-Tier layered architecture (Presentation, Agronomic Reasoning, Deep Learning, Relational Persistence).  
3.2 **Relational Data Model:** 11-table ACID schema in SQLite with Write-Ahead Logging (WAL).  
3.3 **Entity-Relationship (ER) Diagram & Constraint Design:** Foreign key cascades, check constraints, and query indexes.  
3.4 **Grower Privacy & Security Architecture:** Intentional omission of GPS coordinates; taluk-level weather aggregation.

---

### Chapter 4: Computer Vision & Transfer Learning Pipeline
4.1 **Flower Maturity Taxonomy:** 4 discrete commercial classes (`READY_TO_PLUCK`, `NOT_READY`, `TOO_OPEN`, `DAMAGED_OR_ABNORMAL`).  
4.2 **Dual-Layer Duplicate & Leakage Detector:** Exact SHA-256 cryptographic hashing and 64-bit perceptual difference hashing (dHash).  
4.3 **MobileNetV2 Architecture:** Feature extractor freezing, depthwise separable convolutions, in-graph data augmentation, and regularized classification head.  
4.4 **Mathematical Uncertainty & Probability Vector Calibration:** $U = 1.0 - \max(P(C_i))$ and global memory caching.  
4.5 **Segregated Whole-Plant Queue:** Exclusion of multi-bud canopy images from single-bud training.

---

### Chapter 5: Multi-Factor Agronomic Decision Support Engine
5.1 **Separation of Visible Symptoms from Causal Diagnoses:** Physical observations as evidence vs differential diagnostic hypotheses.  
5.2 **Contextual Diagnostic Weighting:** Differentiating Iron chlorosis from Nitrogen deficiency via soil pH and leaf age context.  
5.3 **Fertilizer Label Verification & Nutrient Accounting:** Bag label input validation, per-bush dosage calculation, and TNAU split alignment.  
5.4 **Soil, Irrigation & Weather Synthesis Rules:** Leaching hazards during rainfall; heat stress thresholds during daytime irrigation; calcareous soil buffering.  
5.5 **Non-Prescription Safeguard & Expert Referral Engine:** KVK / ADH referral triggers and standardized sample collection protocol.

---

### Chapter 6: Implementation, User Experience & Testing
6.1 **Responsive Bilingual User Interface:** Streamlit multi-page router with English and native Tamil (`தமிழ்`) support.  
6.2 **Mobile Usability & CSS Design Tokens:** Responsive vertical column collapsing, touch targets, and accessible color palettes.  
6.3 **Automated Verification Suite:** 62 pytest unit and integration tests covering agronomy, database, validation, models, and delivery.  
6.4 **Commercial Harvest Risk Matrix Evaluation:** Quantitative analysis of premature plucking false positives and defective packing false positives.

---

### Chapter 7: Limitations & Future Enhancements
7.1 **Current Limitations:** Visual non-specificity of foliar chlorosis, experimental small-dataset boundary, absence of automated sensor telemetry.  
7.2 **Planned Future Work:**  
  - Phase 7: YOLO multi-bud real-time canopy detection.  
  - Phase 11: Automated multi-sensor IoT integration (soil moisture probes).  
  - Edge Deployment: TFLite quantization for offline smartphone app deployment.

---

### Chapter 8: Conclusion
Summary of engineering contributions, agricultural impact on family farming productivity, and final remarks.

---

### References
- Tamil Nadu Agricultural University (TNAU) Agritech Portal Floriculture Guidelines.
- ICAR - Indian Institute of Horticultural Research (IIHR) Jasmine Production Manuals.
- Sandler, M., et al. "MobileNetV2: Inverted Residuals and Linear Bottlenecks." CVPR 2018.
- Fertilizer (Inorganic, Organic or Mixed) (Control) Order, 1985, Government of India.
