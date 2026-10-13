# 🌿 Smart Jasmine Farming Assistant (ஸ்மார்ட் மல்லி விவசாய உதவியாளர்)

An AI-powered decision support and computer-vision assistant specifically designed for **Jasminum sambac** (*Gundu Malli / குண்டு மல்லி*) cultivation in ground-soil family farms (1/4 to 1 acre).

---

## 🎯 Project Overview & Objectives

Jasmine farming faces delicate harvest timing, bud rot, bud-worm damage, flower drop, and uncertainty around fertilizer nutrition. This project provides a step-by-step, evidence-based digital assistant to help:

1. **Classify Flower Maturity (Module A):** Identify whether individual buds are `READY_TO_PLUCK`, `NOT_READY`, `TOO_OPEN`, or `DAMAGED_OR_ABNORMAL`.
2. **Whole-Plant Bud Detection (Module B):** Count and map buds across whole-plant photographs.
3. **Plant Health & Damage Analysis (Module C):** Systematically analyze yellowing/curled leaves and bud rot, distinguishing observations from confirmed causes.
4. **Growth Improvement Advisor (Module D):** Multi-factor guidance combining pruning history, sunlight, irrigation, and weather.
5. **Fertilizer Identification & Nutrient Tracking (Module E):** Record organic manure, urea, potash, and NPK complexes with label extraction and nutrient balance calculations.
6. **Soil Health Monitoring (Module F):** Log and interpret pH (baseline 6.0–7.0), texture, drainage, and NPK test values.
7. **Weather Integration (Module G):** Connect to weather forecasts for smart irrigation planning.
8. **Farm Dashboard & History (Module H):** Persistent farm logs in SQLite with mobile-friendly UI and Tamil-language localization.

---

## 📂 Project Directory Structure

```text
smart-jasmine-assistant/
├── app.py                    # Minimal responsive Streamlit web application
├── .env.example              # Environment variables template (Weather API, etc.)
├── .gitignore                # Windows, Python, and dataset gitignore rules
├── check_environment.py      # Automated Windows environment diagnostic tool
├── requirements.txt          # Python dependencies (Streamlit, Pandas, Pillow, etc.)
├── setup_env.bat             # 1-click Windows Command Prompt setup script
├── setup_env.ps1             # Windows PowerShell setup script
├── README.md                 # Project documentation and roadmap
├── config/
│   ├── __init__.py
│   └── settings.py           # Paths, domain parameters (pH 6.0-7.0, stages, Tamil)
├── data/
│   ├── raw/                  # Original unprocessed garden & flower photographs
│   ├── processed/            # Partitioned datasets (train/val/test splits)
│   └── db/                   # SQLite databases (jasmine_farm.db)
├── models/                   # Saved vision models (.keras, .tflite, weights)
├── reports/                  # Evaluation logs, confusion matrices, farm exports
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── constants.py      # Flower stages, harvest advice, symptoms, NPK reference
│   └── utils/
│       ├── __init__.py
│       └── logger.py         # Timestamped application logger
└── tests/
    ├── __init__.py
    └── test_setup.py         # Pytest verification for paths, settings, and constants
```

---

## 🚀 Windows Setup & Quick Start

### Prerequisites
- **Operating System:** Windows 10 or Windows 11 (64-bit).
- **Python:** Python 3.10 to 3.14 (64-bit).

### Method 1: Automated Script (Recommended)

In Windows PowerShell or Command Prompt, navigate to the project directory and run:

**PowerShell:**
```powershell
.\setup_env.ps1
```

**Command Prompt (cmd):**
```cmd
setup_env.bat
```

---

### Method 2: Manual Setup Step-by-Step

1. **Create the Python Virtual Environment:**
   ```powershell
   python -m venv .venv
   ```

2. **Activate the Environment:**
   - PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```

3. **Install Dependencies:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Environment Integrity:**
   ```powershell
   python check_environment.py
   ```

5. **Run Automated Unit Tests:**
   ```powershell
   pytest tests -v
   ```

6. **Launch the Streamlit Web Application:**
   ```powershell
   streamlit run app.py
   ```


---

## 🗺️ 12-Phase Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Project structure, constants, and Windows setup | ✅ Completed |
| **Phase 2** | Responsive Streamlit interface & mobile layout | ⏳ Next |
| **Phase 3** | SQLite database and farm record management | 📅 Planned |
| **Phase 4** | Dataset organization & image labeling workflow | 📅 Planned |
| **Phase 5** | Flower-stage classification model (MobileNetV2 / CNN) | 📅 Planned |
| **Phase 6** | Model evaluation, error analysis & uncertainty | 📅 Planned |
| **Phase 7** | Whole-plant bud detection (YOLO) | 📅 Planned |
| **Phase 8** | Plant health observations & damage analysis | 📅 Planned |
| **Phase 9** | Fertilizer identification & nutrient calculations | 📅 Planned |
| **Phase 10** | Soil health & weather API integration | 📅 Planned |
| **Phase 11** | Evidence-based recommendation engine | 📅 Planned |
| **Phase 12** | Integrated dashboard, testing & deployment | 📅 Planned |
