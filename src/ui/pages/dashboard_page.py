"""
Dashboard Page for Smart Jasmine Farming Assistant.
Overview of farm status, harvest metrics, and field management tasks.
"""

import streamlit as st
from config.settings import CROP_NAME_EN, CROP_NAME_TA, SOIL_PH_RANGE
from src.ui.components import render_page_header, render_ai_status


def render_dashboard(is_tamil: bool) -> None:
    """Renders the main farm operations dashboard."""
    render_page_header(
        title_en="Jasmine Garden Dashboard",
        title_ta="மல்லி பண்ணை டாஷ்போர்டு",
        subtitle_en="Real-time farm overview, harvest readiness, and crop management tasks",
        subtitle_ta="நிகழ்நேர தோட்ட மேற்பார்வை, அறுவடை நிலவரம் மற்றும் பயிர் மேலாண்மை பணிகள்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Phase 2 Interface Active. Data entry & validation verified. (Image classification models will train in Phase 5).",
        is_tamil=is_tamil,
    )

    # -----------------------------------------------------------------------
    # Top KPI Cards
    # -----------------------------------------------------------------------
    harvest_count = len(st.session_state.harvest_records)
    health_count = len(st.session_state.plant_health_records)
    fert_count = len(st.session_state.fertilizer_records)
    soil_count = len(st.session_state.soil_test_records)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">Harvest Observations</div>
                <div class="metric-value">{harvest_count}</div>
                <div class="metric-sub">● Staged records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">Health Observations</div>
                <div class="metric-value">{health_count}</div>
                <div class="metric-sub">● Under investigation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">Fertilizer Inputs</div>
                <div class="metric-value">{fert_count}</div>
                <div class="metric-sub">● Active applications</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">Soil Test Records</div>
                <div class="metric-value">{soil_count}</div>
                <div class="metric-sub">● Target pH: {SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Two Columns: Garden Profile & Field Advisory Checklist
    # -----------------------------------------------------------------------
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown("### 🌾 Garden Profile (தோட்ட விபரம்)")
        st.markdown(
            f"""
            <div class="farm-card">
                <b>Botanical Crop:</b> {CROP_NAME_EN} ({CROP_NAME_TA})<br>
                <b>Cultivation Method:</b> Ground Soil Cultivation (தரை மண் பயிரிடுதல்)<br>
                <b>Plot Size:</b> Approximately 0.25 to 1.0 Acre<br>
                <b>Pruning Cycle:</b> Annual winter pruning (Late Nov - Dec) for spring-summer flush<br>
                <b>Sunlight Exposure:</b> Full Sun (Min. 6 hours direct daily)<br>
                <b>Watering Strategy:</b> Avoid waterlogging; check 15 cm soil depth before irrigation<br>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### ⚡ Quick Navigation (விரைவுச் செல்)")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🌸 Flower Analysis", use_container_width=True, key="dash_btn_flower"):
                st.session_state.active_page = "Flower Analysis"
                st.rerun()
            if st.button("🍃 Plant Health", use_container_width=True, key="dash_btn_health"):
                st.session_state.active_page = "Plant Health"
                st.rerun()
        with btn_col2:
            if st.button("🧪 Fertilizer Records", use_container_width=True, key="dash_btn_fert"):
                st.session_state.active_page = "Fertilizer Records"
                st.rerun()
            if st.button("🔬 Soil Health", use_container_width=True, key="dash_btn_soil"):
                st.session_state.active_page = "Soil Health"
                st.rerun()

    with right_col:
        st.markdown("### 📋 Daily Jasmine Field Checklist (தினசரி சரிபார்ப்பு)")
        st.markdown(
            """
            <div class="farm-card" style="border-left: 4px solid #2d6a4f;">
                <b>1. Morning Plucking Window:</b><br>
                Harvest between 6:00 AM and 8:30 AM before direct sunlight opens petals and evaporates volatile fragrance oils.<br><br>
                <b>2. Premature Bud Drop Inspection:</b><br>
                Inspect bushes for fallen buds. Split a fallen bud with a blade to check for yellow-orange blossom midge maggots.<br><br>
                <b>3. Moisture & Drainage Check:</b><br>
                Check soil at 15–20 cm depth. Jasmine roots suffocate quickly in waterlogged soil.<br><br>
                <b>4. Leaf Underside Scouting:</b><br>
                Check tender flush undersides for thrips or tiny webbing before assuming nutrient deficiency.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Recent Logged Records Summary
    # -----------------------------------------------------------------------
    st.markdown("### 🕒 Recent Activity (சமீபத்திய பதிவுகள்)")
    if st.session_state.harvest_records:
        recent = st.session_state.harvest_records[0]
        st.info(
            f"**Latest Harvest Observation:** {recent['date']} | {recent['section']} | "
            f"Stage: **{recent['stage']}** ({recent['quantity']} {recent['unit']}) — {recent['notes']}"
        )
    if st.session_state.fertilizer_records:
        recent_f = st.session_state.fertilizer_records[0]
        st.success(
            f"**Latest Fertilizer Application:** {recent_f['date']} | {recent_f['product_name']} "
            f"({recent_f['quantity_kg']} kg) on {recent_f['section']} — {recent_f['reason']}"
        )
