# 🏗️ Smart Jasmine Farming Assistant: System Architecture

**Crop:** *Jasminum sambac* (Gundu Malli / குண்டு மல்லி)  
**Architecture Pattern:** 4-Tier Layered Architecture with ACID Relational Persistence and Edge Inference  

---

## 1. High-Level Architectural Diagram

```
+-----------------------------------------------------------------------------------+
|                           1. PRESENTATION LAYER (Streamlit)                       |
|   - Multi-Page Router (app.py)                   - Bilingual Engine (EN / TA)    |
|   - Mobile-First Responsive CSS                  - Session State Synchronizer     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       2. DOMAIN & AGRONOMIC REASONING LAYER                       |
|   - Fertilizer Calculator (src/agronomy/fertilizer_calculator.py)                 |
|   - Plant Health Symptom Engine (src/agronomy/plant_health_engine.py)             |
|   - Integrated Decision Support (src/agronomy/decision_support.py)                |
|   - Input Validation & Guardrails (src/core/validation.py)                        |
+-----------------------------------------------------------------------------------+
                      |                                           |
                      v                                           v
+-------------------------------------------+   +-----------------------------------+
|    3. MACHINE LEARNING / CV LAYER         |   |    4. RELATIONAL PERSISTENCE      |
| - MobileNetV2 Transfer Learning           |   | - SQLite 3 with WAL Mode          |
| - In-Graph Augmentation Pipeline          |   | - 11 Relational Tables with FKs   |
| - Model Caching & Memory Manager          |   | - Query Optimization Indexes      |
| - Uncertainty Estimation (1 - top_conf)   |   | - Privacy Isolation (No GPS)      |
+-------------------------------------------+   +-----------------------------------+
```

---

## 2. Layer Descriptions

### Tier 1: Presentation Layer
- **Framework:** Streamlit (Python-based reactive web application).
- **Component Design System:** Located in [src/ui/components.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/ui/components.py). Injects CSS variables for high-contrast agricultural accessibility (`#1b4332`, `#2d6a4f`, `#52b788`, `#e9d8a6`), 12-column grid metrics, and mobile viewport breakpoints (`@media (max-width: 768px)`).
- **Bilingual Engine:** Synchronized via `st.session_state.language`. Renders native Tamil (`தமிழ்`) alongside English across all 8 modules without resetting form inputs.

### Tier 2: Domain Core & Agronomic Reasoning Layer
- **Fertilizer Accounting Engine ([src/agronomy/fertilizer_calculator.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/agronomy/fertilizer_calculator.py)):** Encapsulates the Fertilizer Control Order (FCO) guaranteed analyses, elemental stoichiometric conversions, per-bush dosage calculations, and TNAU Jasmine Package of Practices split thresholds.
- **Plant Health Engine ([src/agronomy/plant_health_engine.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/agronomy/plant_health_engine.py)):** Enforces strict separation between observational physical symptoms and causal diagnostic hypotheses. Calculates contextual weights based on soil pH, drainage, and ambient temperatures, and executes expert referral evaluations.
- **Integrated Decision Support ([src/agronomy/decision_support.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/agronomy/decision_support.py)):** Synthesizes multi-factor relationships: rain forecasts vs nitrogen topdressing hazards; daytime heat vs shallow root scalding; alkaline soil pH vs iron precipitation.

### Tier 3: Machine Learning & Computer Vision Layer
- **Framework:** TensorFlow 2.x / Keras Functional API.
- **Backbone Architecture:** MobileNetV2 with ImageNet pretrained feature extractors. Base weights are frozen during early transfer learning to prevent destructive gradient updates on small agricultural datasets.
- **In-Graph Data Augmentation:** `RandomFlip`, `RandomRotation(0.15)`, `RandomZoom(0.1)`, `RandomContrast(0.15)` executed in-graph for field lighting and angle robustness.
- **Inference Engine ([src/models/inference.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/models/inference.py)):** Employs global model caching to prevent re-instantiation overhead on Streamlit re-renders. Generates predicted stage, confidence %, uncertainty score ($1.0 - \text{confidence}$), and complete 4-class distributions.

### Tier 4: Relational Persistence Layer
- **Engine:** SQLite 3 configured with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`).
- **Concurrency & Integrity:** Enforces `PRAGMA foreign_keys = ON;` and `PRAGMA synchronous = NORMAL;`.
- **Database Schema ([src/database/schema.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/database/schema.py)):** 11 relational tables:
  1. `farm_profiles`: Farm metadata, acreage, and grower privacy protection.
  2. `garden_sections`: Beds, plant counts, drainage, and planting year.
  3. `fertilizer_products`: FCO guaranteed formulations ($N\%, P_2O_5\%, K_2O\%$).
  4. `fertilizer_applications`: Treatment logs with calculated elemental NPK inputs.
  5. `soil_tests`: Laboratory pH, EC, texture, and organic carbon records.
  6. `irrigation_records`: Irrigation events, root depth moisture, and local weather.
  7. `pruning_records`: Annual winter pruning, defoliation, and withholding periods.
  8. `image_labels`: Staged photographs with verified grower ground truth.
  9. `plant_observations`: Field symptoms, differential hypotheses, and confirmation statuses.
  10. `harvest_records`: Commercial bud counts, kilograms, and market quality grades.
  11. `recommendations`: Actionable cultural guidance with evidence sources.

---

## 3. Privacy & Non-Prescription Safety Architecture

- **Grower Privacy Protection:** The database and UI strictly exclude exact GPS latitude/longitude coordinates to protect family farm privacy. Weather is resolved at the regional taluk/city level (`Madurai / Tamil Nadu`).
- **Non-Prescription Safeguard:** The application prohibits prescribing chemical insecticides, fungicides, or synthetic fertilizer rates from photographs alone. Visual signs produce differential hypotheses that explicitly prompt growers to verify physical root depth, perform 10x lens underleaf checks, and consult certified agricultural extension officers.
