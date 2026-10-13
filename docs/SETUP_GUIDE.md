# 🛠️ Smart Jasmine Farming Assistant: Setup & Installation Guide

**Crop:** *Jasminum sambac* (Gundu Malli / குண்டு மல்லி)  
**Target Environment:** Windows 10 / Windows 11 (64-bit)  
**Application Architecture:** Streamlit Web Application + SQLite ACID Storage + TensorFlow/Keras MobileNetV2  

---

## 1. System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit).
- **Python:** Python 3.10 to 3.14 (64-bit).
- **RAM:** 4 GB minimum (8 GB recommended for deep learning training).
- **Disk Space:** 500 MB for code and virtual environment; 2 GB+ for image datasets.
- **Web Browser:** Google Chrome, Microsoft Edge, Firefox, or Safari (Desktop & Mobile).

---

## 2. Automated Installation (Recommended)

Two automated scripts are provided in the root directory:

### Option A: Windows PowerShell
1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd C:\Users\m.sathish\.gemini\antigravity-ide\scratch\smart-jasmine-assistant
   ```
2. Execute the setup script:
   ```powershell
   .\setup_env.ps1
   ```

### Option B: Windows Command Prompt (CMD)
1. Open Command Prompt and navigate to the project directory:
   ```cmd
   cd C:\Users\m.sathish\.gemini\antigravity-ide\scratch\smart-jasmine-assistant
   ```
2. Execute the batch script:
   ```cmd
   setup_env.bat
   ```

---

## 3. Manual Step-by-Step Installation

If you prefer installing manually or configuring a customized environment:

### Step 1: Create the Virtual Environment
```powershell
python -m venv .venv
```

### Step 2: Activate the Virtual Environment
- **PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If script execution is disabled in PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*
- **Command Prompt (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### Step 3: Upgrade Pip & Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Environment Integrity
Run the built-in diagnostic script:
```powershell
python check_environment.py
```
This confirms directory structure, write permissions, and library imports.

---

## 4. Running the Web Application

Launch the Streamlit server from the active virtual environment:

```powershell
streamlit run app.py
```

Once running, access the application in your browser:
- **Local Access:** `http://localhost:8501`
- **Network Access (Mobile Devices on Same Wi-Fi):** `http://<YOUR_LOCAL_IP>:8501`

To run in headless background mode:
```powershell
streamlit run app.py --server.headless true --server.port 8501
```

---

## 5. Running the Automated Test Suite

Run the full pytest suite (62 tests):

```powershell
pytest -v
```

To run individual test modules:
- Agronomy & Decision Support: `pytest tests/test_agronomy.py -v`
- Database CRUD: `pytest tests/test_database.py -v`
- Dataset Partitioner: `pytest tests/test_dataset.py -v`
- MobileNetV2 Pipeline: `pytest tests/test_model.py -v`
- End-to-End Delivery: `pytest tests/test_delivery.py -v`

---

## 6. Troubleshooting Common Windows Issues

| Issue | Root Cause | Solution |
|---|---|---|
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Windows PowerShell execution policy | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal window. |
| `oneDNN custom operations are on` hang | TensorFlow AVX/oneDNN CPU driver initialization on Windows | Set `TF_ENABLE_ONEDNN_OPTS=0` and `TF_CPP_MIN_LOG_LEVEL=3` in environment variables. |
| `sqlite3.OperationalError: database is locked` | Concurrent database access | SQLite is configured in WAL mode (`PRAGMA journal_mode=WAL`). Ensure all connections use the connection context manager. |
| Port 8501 already in use | Another Streamlit instance is running | Specify an alternative port: `streamlit run app.py --server.port 8502`. |
