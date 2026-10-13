"""
Smart Jasmine Farming Assistant (ஸ்மார்ட் மல்லி விவசாய உதவியாளர்)
Main Application Entry Point & Responsive Multi-Page Router.
Crop: Jasminum sambac (Gundu Malli / குண்டு மல்லி).
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import (
    CROP_NAME_EN,
    CROP_NAME_TA,
    SOIL_PH_RANGE,
)
from src.ui.state import init_session_state
from src.ui.components import inject_custom_css
from src.ui.pages.dashboard_page import render_dashboard
from src.ui.pages.flower_analysis_page import render_flower_analysis
from src.ui.pages.plant_health_page import render_plant_health
from src.ui.pages.fertilizer_page import render_fertilizer_records
from src.ui.pages.soil_health_page import render_soil_health
from src.ui.pages.weather_page import render_weather_irrigation
from src.ui.pages.farm_history_page import render_farm_history
from src.ui.pages.dataset_page import render_dataset_page

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Jasmine Farming Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize in-memory session records
init_session_state()

# Inject shared styling
inject_custom_css()

# ---------------------------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">
            <span style="font-size:2rem;">🌿</span>
            <div>
                <h3 style="margin:0; font-size:1.2rem; color:#1b4332; font-weight:800; line-height:1.1;">Smart Jasmine</h3>
                <span style="font-size:0.8rem; color:#52b788; font-weight:600;">குண்டு மல்லி உதவியாளர்</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Language Toggle
    lang = st.radio(
        "Display Language / மொழி:",
        options=["English", "தமிழ் (Tamil)"],
        index=0 if st.session_state.language == "English" else 1,
        key="app_language_selector",
    )
    is_tamil = lang.startswith("தமிழ்")
    st.session_state.language = "Tamil" if is_tamil else "English"

    st.markdown("---")

    # Navigation Options
    pages_en = [
        "Dashboard",
        "Flower Analysis",
        "Dataset and Labeling",
        "Plant Health",
        "Fertilizer Records",
        "Soil Health",
        "Weather and Irrigation",
        "Farm History",
    ]

    pages_ta = [
        "Dashboard (டாஷ்போர்டு)",
        "Flower Analysis (மலர் பகுப்பாய்வு)",
        "Dataset and Labeling (தரவுத்தொகுப்பு)",
        "Plant Health (பயிர் நலம்)",
        "Fertilizer Records (உர மேலாண்மை)",
        "Soil Health (மண் நலம்)",
        "Weather and Irrigation (வானிலை & பாசனம்)",
        "Farm History (பண்ணை வரலாறு)",
    ]

    page_icons = {
        "Dashboard": "🌾",
        "Flower Analysis": "🌸",
        "Dataset and Labeling": "📁",
        "Plant Health": "🍃",
        "Fertilizer Records": "🧪",
        "Soil Health": "🔬",
        "Weather and Irrigation": "🌦️",
        "Farm History": "📋",
    }

    display_options = pages_ta if is_tamil else pages_en

    # Sync selection with session state active_page
    current_idx = 0
    if st.session_state.active_page in pages_en:
        current_idx = pages_en.index(st.session_state.active_page)

    selected_display = st.radio(
        "Navigate Modules / வழிசெலுத்தல்:",
        options=display_options,
        index=current_idx,
        key="app_nav_radio",
    )

    # Determine internal page key
    selected_page_key = pages_en[display_options.index(selected_display)]
    st.session_state.active_page = selected_page_key

    st.markdown("---")

    # Garden Context Card
    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:0.8rem; font-size:0.82rem; color:#334155;">
            <b>Garden:</b> {CROP_NAME_EN}<br>
            <b>Tamil:</b> {CROP_NAME_TA}<br>
            <b>Method:</b> Ground Soil Cultivation<br>
            <b>Target pH:</b> {SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}<br>
            <b>Build Phase:</b> Phase 4 (Dataset & Labeling)
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Content Router
# ---------------------------------------------------------------------------
active_page = st.session_state.active_page

if active_page == "Dashboard":
    render_dashboard(is_tamil=is_tamil)
elif active_page == "Flower Analysis":
    render_flower_analysis(is_tamil=is_tamil)
elif active_page == "Dataset and Labeling":
    render_dataset_page(is_tamil=is_tamil)
elif active_page == "Plant Health":
    render_plant_health(is_tamil=is_tamil)
elif active_page == "Fertilizer Records":
    render_fertilizer_records(is_tamil=is_tamil)
elif active_page == "Soil Health":
    render_soil_health(is_tamil=is_tamil)
elif active_page == "Weather and Irrigation":
    render_weather_irrigation(is_tamil=is_tamil)
elif active_page == "Farm History":
    render_farm_history(is_tamil=is_tamil)
else:
    st.error(f"Unknown page: {active_page}")

