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
    CROP_NAME_TE,
    SOIL_PH_RANGE,
)
from src.core.i18n import (
    PAGE_KEYS,
    normalize_lang,
    get_page_display_names,
    get_page_key_from_display,
    get_crop_name,
    t,
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

# Determine language selection early from session_state
if "language_code" not in st.session_state:
    st.session_state.language_code = "en"

# ---------------------------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------------------------
with st.sidebar:
    # Language Toggle FIRST so entire sidebar updates cleanly
    lang_options = ["English", "தமிழ்", "తెలుగు"]
    cur_code = st.session_state.language_code
    if cur_code == "ta":
        default_lang_idx = 1
    elif cur_code == "te":
        default_lang_idx = 2
    else:
        default_lang_idx = 0

    lang_choice = st.radio(
        label=t("display_language", cur_code),
        options=lang_options,
        index=default_lang_idx,
        key="app_language_selector",
    )

    if lang_choice == "தமிழ்":
        lang_code = "ta"
    elif lang_choice == "తెలుగు":
        lang_code = "te"
    else:
        lang_code = "en"

    st.session_state.language_code = lang_code
    st.session_state.language = "Tamil" if lang_code == "ta" else ("Telugu" if lang_code == "te" else "English")
    is_tamil = (lang_code == "ta")

    st.markdown("---")

    # Pure localized branding header
    app_title = t("app_title", lang_code)
    app_sub = t("app_subtitle", lang_code)
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">
            <span style="font-size:2rem;">🌿</span>
            <div>
                <h3 style="margin:0; font-size:1.2rem; color:#1b4332; font-weight:800; line-height:1.1;">{app_title}</h3>
                <span style="font-size:0.8rem; color:#52b788; font-weight:600;">{app_sub}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Options in Pure Script
    display_options = get_page_display_names(lang_code)

    # Sync selection with session state active_page
    current_idx = 0
    if st.session_state.active_page in PAGE_KEYS:
        current_idx = PAGE_KEYS.index(st.session_state.active_page)

    nav_label = t("navigate_modules", lang_code)
    selected_display = st.radio(
        nav_label,
        options=display_options,
        index=current_idx,
        key="app_nav_radio",
    )

    # Determine internal page key
    selected_page_key = get_page_key_from_display(selected_display, lang_code)
    st.session_state.active_page = selected_page_key

    st.markdown("---")

    # Pure Garden Context Card
    crop_display = get_crop_name(lang_code)
    card_title = t("garden_context_title", lang_code)
    lbl_crop = t("garden_crop", lang_code)
    lbl_method = t("cultivation_method", lang_code)
    val_method = t("cultivation_val", lang_code)
    lbl_ph = t("target_ph", lang_code)
    lbl_status = t("system_status", lang_code)
    val_status = t("active", lang_code)

    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:0.8rem; font-size:0.82rem; color:#334155;">
            <b>{card_title}:</b><br>
            • {lbl_crop}: <b>{crop_display}</b><br>
            • {lbl_method}: <b>{val_method}</b><br>
            • {lbl_ph}: <b>{SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}</b><br>
            • {lbl_status}: <span style="color:#2d6a4f; font-weight:700;">{val_status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Content Router
# ---------------------------------------------------------------------------
active_page = st.session_state.active_page

if active_page == "Dashboard":
    render_dashboard(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Flower Analysis":
    render_flower_analysis(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Dataset and Labeling":
    render_dataset_page(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Plant Health":
    render_plant_health(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Fertilizer Records":
    render_fertilizer_records(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Soil Health":
    render_soil_health(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Weather and Irrigation":
    render_weather_irrigation(is_tamil=is_tamil, lang=lang_code)
elif active_page == "Farm History":
    render_farm_history(is_tamil=is_tamil, lang=lang_code)
else:
    st.error(f"Unknown page: {active_page}")

