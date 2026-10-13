"""
Application Settings and Domain Configuration for Smart Jasmine Farming Assistant.
Crop: Jasminum sambac (Gundu Malli / குண்டு மல்லி).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# ---------------------------------------------------------------------------
# Base Directories
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DB_DIR = DATA_DIR / "db"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure all essential project directories exist
for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DB_DIR, MODELS_DIR, REPORTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------------------
DEFAULT_DB_PATH = Path(os.getenv("DB_PATH", str(DB_DIR / "jasmine_farm.db")))

# ---------------------------------------------------------------------------
# Jasminum sambac Domain Parameters & Constants
# ---------------------------------------------------------------------------
CROP_NAME_EN = "Jasminum sambac"
CROP_NAME_TA = "குண்டு மல்லி (Malli)"
DEFAULT_FARM_SIZE_ACRES = 0.5  # Typical 1/4 to 1 acre family plot

# Flower Maturity Classification Classes (Module A & B)
FLOWER_STAGES = [
    "READY_TO_PLUCK",
    "NOT_READY",
    "TOO_OPEN",
    "DAMAGED_OR_ABNORMAL",
]

# Mobile-friendly Tamil Translations for UI Localization
TAMIL_STAGE_TRANSLATIONS = {
    "READY_TO_PLUCK": "பறிக்கத் தயார் (Harvest Ready)",
    "NOT_READY": "இன்னும் முதிரவில்லை (Not Ready)",
    "TOO_OPEN": "அதிகம் விரிந்தது (Over-blown / Too Open)",
    "DAMAGED_OR_ABNORMAL": "சேதமடைந்தது / புழு தாக்குதல் (Damaged / Abnormal)",
}

# Soil Health Reference Parameters (Module F)
# Note: 6.0 - 7.0 is the proposed baseline according to TNAU/horticultural guidance
SOIL_PH_RANGE = {
    "min_optimal": 6.0,
    "max_optimal": 7.0,
    "min_tolerable": 5.5,
    "max_tolerable": 7.5,
}

# Fertilizer Categories (Module E)
FERTILIZER_CATEGORIES = [
    "Organic Manure / FYM",
    "Vermicompost",
    "Urea (46% N)",
    "Muriate of Potash - MOP (60% K2O)",
    "Single Super Phosphate - SSP (16% P2O5)",
    "DAP (18-46-0)",
    "Complex NPK (e.g., 17:17:17, 20:20:0:13, 19:19:19)",
    "Micronutrient Mixture (Zn, Fe, B)",
    "Neem Cake",
    "Other / Unidentified",
]

# Weather Settings (Module G)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Madurai")
WEATHER_LAT = float(os.getenv("WEATHER_LAT", "9.9252"))
WEATHER_LON = float(os.getenv("WEATHER_LON", "78.1198"))
