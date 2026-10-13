# 📖 Smart Jasmine Farming Assistant: User & Grower Guide
### விவசாய வழிகாட்டி — குண்டு மல்லி சாகுபடி உதவியாளர்

**Crop:** *Jasminum sambac* (Gundu Malli / குண்டு மல்லி)  
**Target Farm Size:** 1/4 to 1 Acre Ground Soil  
**Language Support:** English & தமிழ் (Tamil)  

---

## 1. Getting Started & Dashboard Navigation

1. **Language Selection:**
   - In the left sidebar, toggle between **English** and **தமிழ் (Tamil)**.
   - All module titles, metric descriptions, harvest guidelines, and diagnostic tips translate immediately without losing unsaved form data.
2. **Dashboard Overview (Module A):**
   - **Today's Weather & Rain Preview:** Displays current temperature, relative humidity, and 24h rainfall forecasts for your growing cluster.
   - **Harvest Guidance Banner:** Displays optimal morning plucking windows (**6:00 AM – 8:30 AM**) to preserve floral essential oils and prevent petal bruising.
   - **Cumulative Nutrients:** Quick-glance counters of Nitrogen, Phosphorus, and Potassium delivered to your soil this season.

---

## 2. Flower Maturity Inspection & Harvest Staging (Module B)

### Maturity Stages Reference
| Stage Key | Tamil Term | Physical Signs | Harvesting Action |
|---|---|---|---|
| `READY_TO_PLUCK` | பறிக்கத் தயார் | Firm, unopened white bud with elongated corolla tube | Pluck early morning with stalk attached; wrap in shade/moist cloth for market. |
| `NOT_READY` | முதிரவில்லை | Small, tight greenish or compact bud | Do not pick today. Allow 24–48 hours for elongation. |
| `TOO_OPEN` | மலர்ந்துவிட்டது | Petals open, interior reproductive parts visible | Pick immediately to avoid plant drain; use for home puja or garlands. |
| `DAMAGED_OR_ABNORMAL` | சேதமடைந்தது | Pinhead bore holes, dark frass, webbing, or rot | Destroy in separate container; inspect for Jasmine Bud Worm or Midge. |

### How to Inspect a Bud:
1. Navigate to **Flower Analysis**.
2. Select your inspection mode:
   - **Single Bud Closeup:** Inspect individual bud maturity and quality.
   - **Whole Flower Cluster:** Inspect canopy flush density.
3. Upload a photo taken in natural morning light.
4. If a trained model checkpoint exists, view predicted stage, confidence %, uncertainty score, and complete 4-class distribution.
5. In the right panel, record your confirmed **Grower Ground Truth** assessment to build your farm's verified dataset.

---

## 3. Dataset Staging & Photography Protocol (Module D)

### How to Stage Photos for AI Training:
1. Navigate to **Dataset and Labeling**.
2. Choose **Single Flower Bud Close-up** or **Whole-Plant Bush Photo**:
   - Single buds are routed to `data/raw/single_buds/<STAGE>/` for classification training.
   - Whole-plant photos are routed to `data/raw/whole_plant/incoming/` and strictly segregated to prevent noise in single-bud classification.
3. **Duplicate Detection:** In the **Duplicate Audit** tab, run an audit before generating dataset splits. The system detects exact byte duplicates (SHA-256) and burst-shot near-duplicates (perceptual dHash) to ensure zero data leakage across training, validation, and test splits.

---

## 4. Fertilizer Accounting & Bag Label Verification (Module E)

### TNAU Recommended Annual Nutrient Budget:
For mature bearing bushes (*Jasminum sambac*):
- **Annual Target per Bush:** **60 g N : 120 g $P_2O_5$ : 120 g $K_2O$**, plus **10 to 20 kg Farmyard Manure (FYM)**.
- **Split 1 (Post-Pruning Basal Dose - Dec/Jan):** Full FYM + 100% P ($120\text{ g}$) + 50% N ($30\text{ g}$) + 50% K ($60\text{ g}$).
- **Split 2 (Peak Flowering Flush - Mar/Apr):** Remaining 50% N ($30\text{ g}$) + 50% K ($60\text{ g}$).

### How to Log Fertilizer Applications:
1. Navigate to **Fertilizer Records** $\rightarrow$ **Log Application & Calculate NPK**.
2. Select your garden section (the system loads your bush count automatically).
3. Select your fertilizer product (Urea, MOP, DAP, 17-17-17, FYM, Vermicompost).
4. Enter the quantity in kilograms.
5. Review the live calculation card:
   - Total elemental kg delivered.
   - **Grams per bush ($g/\text{plant}$)** delivered.
   - TNAU alignment feedback (alerts if single N dose exceeds $40\text{ g/bush}$).
6. Click **Record Fertilizer Application** to save permanently to your SQLite database.

### How to Verify a New Fertilizer Bag Label:
1. Navigate to **Formulation Verifier & Label Entry**.
2. Enter the brand name, manufacturer, and printed guaranteed analysis ($N\%, P_2O_5\%, K_2O\%$, Secondary S, Ca, Mg, Zn, Fe).
3. The engine verifies the formulation against Fertilizer Control Order (FCO) benchmarks and registers it in your farm database.

---

## 5. Plant Health Scouting & Differential Diagnoses (Module C)

### Physical Observations vs Confirmed Diagnoses:
Never assume a disease diagnosis from an image alone. Pale yellow leaves can be caused by nitrogen shortage, iron chlorosis, poor drainage, root suffocation, or nematodes.

### How to Log Crop Health Issues:
1. Navigate to **Plant Health**.
2. Check the visible physical signs you observe:
   - *Yellowing of Older Lower Leaves*
   - *Interveinal Yellowing on Young Tender Leaves*
   - *Bore Holes with Frass in Flower Buds*
   - *Silken Webbing Binding Flower Clusters*
   - *Premature Pale/Pinkish Bud Drop*
   - *Stunted Shoots & Daytime Foliar Wilting*
3. The engine instantly evaluates your soil test pH, drainage, and weather to generate **Ranked Differential Hypotheses**.
4. Read the **Required Field Verification Steps** (e.g. slice 10 fallen buds with a razor to check for yellow-orange midge maggots).
5. If damage exceeds 30% or systemic collar rot is suspected, review the **Expert Referral Alert** for KVK contact info and plant tissue sample collection instructions.
6. Once lab or field inspection confirms the cause, update the record in the **Observation History & Confirmation** tab.

---

## 6. Soil Health & Irrigation Management (Modules F & G)

1. **Soil pH Evaluation (Target: 6.0 – 7.0):**
   - Record soil test reports in **Soil Health**.
   - If $\text{pH} > 7.5$ (Alkaline/Calcareous): Do not apply iron to soil; use foliar $0.5\%\text{ } FeSO_4 + 0.5\%\text{ } ZnSO_4$ and organic compost.
   - If $\text{pH} < 6.0$ (Acidic): Request lime dosage recommendations from an official soil test lab.
2. **Weather & Irrigation Scheduling:**
   - Log irrigation and root moisture at $15\text{--}20\text{ cm}$ depth in **Weather and Irrigation**.
   - If 24h forecast rain $\ge 15\text{ mm}$, the system alerts you to **delay topdressing Urea or foliar spraying** to prevent nutrient runoff and leaching.
   - If temperature $\ge 36^\circ\text{C}$, avoid midday irrigation to prevent root scalding.
