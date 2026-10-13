"""
Dashboard Page for Smart Jasmine Farming Assistant.
Overview of farm status, harvest metrics, and field management tasks.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

import streamlit as st
from config.settings import SOIL_PH_RANGE
from src.core.i18n import (
    normalize_lang,
    get_nav_name,
    get_crop_name,
    t,
)
from src.ui.components import render_page_header, render_ai_status


def render_dashboard(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the main farm operations dashboard in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Jasmine Garden Dashboard",
        title_ta="மல்லி பண்ணை முகப்பு",
        title_te="మల్లె తోట డాష్‌బోర్డ్",
        subtitle_en="Real-time farm overview, harvest readiness, and crop management tasks",
        subtitle_ta="நிகழ்நேர தோட்ட மேற்பார்வை, அறுவடை நிலவரம் மற்றும் பயிர் மேலாண்மை பணிகள்",
        subtitle_te="తోట ప్రస్తుత స్థితి, కోత సంసిద్ధత మరియు పంట నిర్వహణ పనులు",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="System Active. Data entry and agronomic validation verified.",
        desc_ta="அமைப்பு செயலில் உள்ளது. களத் தரவு மற்றும் வேளாண் விதிகள் சரிபார்க்கப்பட்டன.",
        desc_te="వ్యవస్థ సిద్ధంగా ఉంది. క్షేత్ర స్థాయి డేటా నమోదు మరియు వ్యవసాయ నియమాలు ధృవీకరించబడ్డాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
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
                <div class="metric-label">{t('kpi_harvests', current_lang)}</div>
                <div class="metric-value">{harvest_count}</div>
                <div class="metric-sub">● {t('sub_staged', current_lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">{t('kpi_health', current_lang)}</div>
                <div class="metric-value">{health_count}</div>
                <div class="metric-sub">● {t('sub_investigation', current_lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">{t('kpi_fertilizers', current_lang)}</div>
                <div class="metric-value">{fert_count}</div>
                <div class="metric-sub">● {t('sub_applications', current_lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-tile">
                <div class="metric-label">{t('kpi_soil', current_lang)}</div>
                <div class="metric-value">{soil_count}</div>
                <div class="metric-sub">● {t('target_ph', current_lang)}: {SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}</div>
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
        st.markdown(f"### 🌾 {t('garden_context_title', current_lang)}")
        crop_name = get_crop_name(current_lang)
        method_label = t("cultivation_method", current_lang)
        method_val = t("cultivation_val", current_lang)
        crop_label = t("garden_crop", current_lang)

        st.markdown(
            f"""
            <div class="farm-card">
                <b>{crop_label}:</b> {crop_name}<br>
                <b>{method_label}:</b> {method_val}<br>
                <b>{t('profile_plot_size', current_lang)}</b><br>
                <b>{t('profile_pruning', current_lang)}</b><br>
                <b>{t('profile_sunlight', current_lang)}</b><br>
                <b>{t('profile_watering', current_lang)}</b><br>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"### ⚡ {t('quick_nav', current_lang)}")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(f"🌸 {get_nav_name('Flower Analysis', current_lang)}", use_container_width=True, key="dash_btn_flower"):
                st.session_state.active_page = "Flower Analysis"
                st.rerun()
            if st.button(f"🍃 {get_nav_name('Plant Health', current_lang)}", use_container_width=True, key="dash_btn_health"):
                st.session_state.active_page = "Plant Health"
                st.rerun()
        with btn_col2:
            if st.button(f"🧪 {get_nav_name('Fertilizer Records', current_lang)}", use_container_width=True, key="dash_btn_fert"):
                st.session_state.active_page = "Fertilizer Records"
                st.rerun()
            if st.button(f"🔬 {get_nav_name('Soil Health', current_lang)}", use_container_width=True, key="dash_btn_soil"):
                st.session_state.active_page = "Soil Health"
                st.rerun()

    with right_col:
        st.markdown(f"### 📋 {t('field_checklist_title', current_lang)}")
        st.markdown(
            f"""
            <div class="farm-card" style="border-left: 4px solid #2d6a4f;">
                <b>{t('checklist_1_title', current_lang)}:</b><br>
                {t('checklist_1_desc', current_lang)}<br><br>
                <b>{t('checklist_2_title', current_lang)}:</b><br>
                {t('checklist_2_desc', current_lang)}<br><br>
                <b>{t('checklist_3_title', current_lang)}:</b><br>
                {t('checklist_3_desc', current_lang)}<br><br>
                <b>{t('checklist_4_title', current_lang)}:</b><br>
                {t('checklist_4_desc', current_lang)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Recent Logged Records Summary
    # -----------------------------------------------------------------------
    st.markdown(f"### 🕒 {t('recent_activity', current_lang)}")
    if st.session_state.harvest_records:
        recent = st.session_state.harvest_records[0]
        st.info(
            f"**{t('latest_harvest', current_lang)}:** {recent['date']} | {recent['section']} | "
            f"{t('maturity_stage', current_lang)}: **{recent['stage']}** ({recent['quantity']} {recent['unit']}) — {recent['notes']}"
        )
    if st.session_state.fertilizer_records:
        recent_f = st.session_state.fertilizer_records[0]
        st.success(
            f"**{t('latest_fertilizer', current_lang)}:** {recent_f['date']} | {recent_f['product_name']} "
            f"({recent_f['quantity_kg']} kg) | {recent_f['section']} — {recent_f['reason']}"
        )
