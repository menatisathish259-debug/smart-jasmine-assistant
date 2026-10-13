"""
Smart Jasmine Farming Assistant (ஸ்மார்ட் மல்லி விவசாய உதவியாளர்)
Phase 1: Minimal Streamlit Web Application & System Verification
Crop: Jasminum sambac (Gundu Malli / குண்டு மல்லி)
"""

import sys
import platform
from pathlib import Path
import streamlit as st

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import (
    CROP_NAME_EN,
    CROP_NAME_TA,
    FLOWER_STAGES,
    TAMIL_STAGE_TRANSLATIONS,
    SOIL_PH_RANGE,
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    DB_DIR,
    MODELS_DIR,
)
from src.core.constants import HARVEST_GUIDANCE, FlowerMaturityStage

# ---------------------------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Jasmine Farming Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Premium Agricultural UI Styling (Emerald botanical palette & responsive cards)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Tamil', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #081c15 0%, #1b4332 50%, #2d6a4f 100%);
        padding: 2rem 2.5rem;
        border-radius: 18px;
        color: #f8f9fa;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(8, 28, 21, 0.25);
        border: 1px solid rgba(82, 183, 136, 0.25);
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #d8f3dc;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #b7e4c7;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }

    .badge-tag {
        display: inline-block;
        background: rgba(82, 183, 136, 0.2);
        border: 1px solid #52b788;
        color: #d8f3dc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(45, 106, 79, 0.12);
    }

    .stage-card {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        margin-bottom: 1rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .stage-card.ready {
        border-top: 5px solid #2d6a4f;
    }
    .stage-card.not-ready {
        border-top: 5px solid #d4a373;
    }
    .stage-card.too-open {
        border-top: 5px solid #e76f51;
    }
    .stage-card.damaged {
        border-top: 5px solid #d90429;
    }

    .stage-badge {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 6px;
        width: fit-content;
        margin-bottom: 0.5rem;
    }

    .badge-ready { background: #d8f3dc; color: #1b4332; }
    .badge-not-ready { background: #faedcd; color: #7f4f24; }
    .badge-too-open { background: #fde2e4; color: #9d0208; }
    .badge-damaged { background: #ffe3e3; color: #9b2226; }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        background: #e8f5e9;
        color: #2e7d32;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar: Controls & Farm Profile
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌾 Farm Setup (தோட்ட அமைப்பு)")
    
    lang = st.radio(
        "Display Language / மொழி:",
        options=["English", "தமிழ் (Tamil)"],
        index=0,
        key="lang_toggle",
    )
    is_tamil = lang.startswith("தமிழ்")

    st.markdown("---")
    st.markdown(
        f"""
        **Crop:** {CROP_NAME_EN}  
        **தமிழ்:** {CROP_NAME_TA}  
        **Soil Method:** Ground Soil (தரை மண்)  
        **Typical Area:** 0.25 - 1.0 Acre  
        **Optimal pH Range:** {SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}  
        """
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.8rem; color:#64748b;">
        <b>Phase 1 Build Status:</b><br>
        ✓ Environment: Python 3.14 (64-bit)<br>
        ✓ Workspace: Active<br>
        ✓ Database: Ready for Phase 3<br>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Header Banner
# ---------------------------------------------------------------------------
header_title = (
    "ஸ்மார்ட் மல்லி விவசாய உதவியாளர்"
    if is_tamil
    else "Smart Jasmine Farming Assistant"
)
header_sub = (
    "AI-அடிப்படையிலான அறுவடை நிலை, பயிர் பாதுகாப்பு மற்றும் ஊட்டச்சத்து வழிகாட்டி"
    if is_tamil
    else "AI Decision Support for Jasminum sambac Harvest Readiness, Plant Health & Nutrition"
)

st.markdown(
    f"""
    <div class="main-header">
        <h1 class="main-title">{header_title}</h1>
        <p class="subtitle">{header_sub}</p>
        <span class="badge-tag">🌱 Ground Cultivation • 1/4 - 1 Acre • Jasminum sambac</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Section 1: System Health & Diagnostic Verification
# ---------------------------------------------------------------------------
st.subheader("System Status & Phase 1 Environment" if not is_tamil else "கணினி நிலை & கட்டம் 1 அமைப்பு")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#64748b; font-weight:600;">PYTHON RUNTIME</span>
            <h3 style="margin:4px 0 0 0; color:#1b4332;">v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}</h3>
            <span class="status-pill" style="margin-top:6px;">● Windows 64-bit</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#64748b; font-weight:600;">ACTIVE PHASE</span>
            <h3 style="margin:4px 0 0 0; color:#1b4332;">Phase 1 / 12</h3>
            <span class="status-pill" style="margin-top:6px;">● Verified Setup</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#64748b; font-weight:600;">TARGET CROP</span>
            <h3 style="margin:4px 0 0 0; color:#1b4332;">J. sambac</h3>
            <span class="status-pill" style="margin-top:6px;">● குண்டு மல்லி</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#64748b; font-weight:600;">SOIL PH BASELINE</span>
            <h3 style="margin:4px 0 0 0; color:#1b4332;">{SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}</h3>
            <span class="status-pill" style="margin-top:6px;">● TNAU Reference</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Section 2: Flower Maturity Criteria (Module A Definition)
# ---------------------------------------------------------------------------
st.subheader(
    "Flower Maturity Classes & Harvesting Standards"
    if not is_tamil
    else "மல்லி அறுவடை நிலைகள் மற்றும் வழிகாட்டுதல்"
)
st.caption(
    "Ground truth criteria defined for our family garden dataset collection (Module A):"
    if not is_tamil
    else "நமது தோட்டப் புகைப்படத் தொகுப்பிற்காக வரையறுக்கப்பட்ட அறுவடை நிலைகள்:"
)

c1, c2, c3, c4 = st.columns(4)

stages_meta = [
    (
        c1,
        FlowerMaturityStage.READY_TO_PLUCK.value,
        "ready",
        "badge-ready",
        "🟢 READY TO PLUCK",
        TAMIL_STAGE_TRANSLATIONS["READY_TO_PLUCK"],
    ),
    (
        c2,
        FlowerMaturityStage.NOT_READY.value,
        "not-ready",
        "badge-not-ready",
        "🟡 NOT READY",
        TAMIL_STAGE_TRANSLATIONS["NOT_READY"],
    ),
    (
        c3,
        FlowerMaturityStage.TOO_OPEN.value,
        "too-open",
        "badge-too-open",
        "🟠 TOO OPEN",
        TAMIL_STAGE_TRANSLATIONS["TOO_OPEN"],
    ),
    (
        c4,
        FlowerMaturityStage.DAMAGED_OR_ABNORMAL.value,
        "damaged",
        "badge-damaged",
        "🔴 DAMAGED / ABNORMAL",
        TAMIL_STAGE_TRANSLATIONS["DAMAGED_OR_ABNORMAL"],
    ),
]

for col, stage_key, card_cls, badge_cls, en_title, ta_title in stages_meta:
    guidance = HARVEST_GUIDANCE[stage_key]
    with col:
        st.markdown(
            f"""
            <div class="stage-card {card_cls}">
                <div>
                    <span class="stage-badge {badge_cls}">{en_title}</span>
                    <h4 style="margin: 4px 0 6px 0; color:#0f172a; font-size:1.05rem;">{ta_title if is_tamil else guidance['status_title']}</h4>
                    <p style="font-size:0.85rem; color:#475569; margin-bottom:0.75rem;">{guidance['description']}</p>
                </div>
                <div style="background:#f8fafc; border-radius:8px; padding:0.6rem; font-size:0.8rem; color:#334155; border-left:3px solid #64748b;">
                    <b>Action:</b> {guidance['recommended_action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Section 3: Next Phase Workflow Preview
# ---------------------------------------------------------------------------
with st.expander("📋 View Project Roadmap (12 Phases)", expanded=False):
    st.markdown(
        """
        - **Phase 1 (Current):** Project structure, Windows setup, and minimal Streamlit app.
        - **Phase 2:** Responsive multi-tab Streamlit interface (Harvest, Diagnostics, Soil, Weather).
        - **Phase 3:** SQLite database persistence for harvest logs, garden sections, and fertilizer records.
        - **Phase 4:** Image labeling tool & dataset organization for the family's jasmine photos.
        - **Phase 5:** Flower classification model training (MobileNetV2 / Transfer Learning).
        - **Phase 6:** Model validation, confusion matrix & uncertainty estimates.
        - **Phase 7:** Multi-bud whole-plant detection with YOLO.
        - **Phase 8:** Plant health & symptom analysis (yellowing leaves, curled foliage, bud borer).
        - **Phase 9:** Fertilizer label recognition & NPK nutrient balance calculator.
        - **Phase 10:** Soil test data integration & local weather API connection.
        - **Phase 11:** Evidence-based growth improvement recommendation engine.
        - **Phase 12:** Production farm dashboard, evaluation report & mobile deployment.
        """
    )

st.caption("🌱 Smart Jasmine Farming Assistant • Jasminum sambac Research & Development")
