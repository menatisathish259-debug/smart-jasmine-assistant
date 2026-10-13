"""
Farm History and Unified Farm Log Page (Module H).
Provides a consolidated chronological history of harvests, health observations, fertilizers, and soil tests.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

import pandas as pd
import streamlit as st

from src.core.i18n import (
    normalize_lang,
    t,
)
from src.ui.components import render_page_header, render_ai_status


def render_farm_history(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the comprehensive farm history and data export page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Farm History & Integrated Logs (Module H)",
        title_ta="பண்ணை வரலாற்றுப் பதிவுகள் மற்றும் மேலாண்மை (பகுதி H)",
        title_te="తోట సమగ్ర చరిత్ర మరియు రికార్డులు (విభాగం H)",
        subtitle_en="Review chronological farm management logs, inspect trends, and export dataset records",
        subtitle_ta="அனைத்து பதிவுகளையும் ஒரே இடத்தில் ஆராய்ந்து, தரவுகளைப் பதிவிறக்கம் செய்துகொள்ளுங்கள்",
        subtitle_te="గత నిర్వహణ రికార్డులను సమీక్షించి, పోకడలను గమనించండి మరియు డేటాను డౌన్‌లోడ్ చేయండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Persistent Database Active. All records are saved in ACID-compliant tables.",
        desc_ta="நிரந்தர தரவுத்தளம் செயலில் உள்ளது. அனைத்து தகவல்களும் முறையாக சேமிக்கப்படுகின்றன.",
        desc_te="శాశ్వత డేటాబేస్ సిద్ధంగా ఉంది. అన్ని రికార్డులు సురక్షితంగా భద్రపరచబడ్డాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    if current_lang == "ta":
        tabs_labels = [
            "🌸 மலர் அறுவடை",
            "🍃 பயிர் நலம்",
            "🧪 உரப் பதிவுகள்",
            "🔬 மண் பரிசோதனை",
            "🌦️ வானிலை மற்றும் பாசனம்",
            "✂️ கவாத்து பதிவுகள்",
            "🗺️ பாத்திகள் மற்றும் பண்ணை",
        ]
        btn_exp_harvest = "📥 அறுவடைப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        btn_exp_health = "📥 பயிர் நலப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        btn_exp_fert = "📥 உரப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        btn_exp_soil = "📥 மண் பரிசோதனைப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        btn_exp_weath = "📥 வானிலைப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        btn_exp_prun = "📥 கவாத்துப் பதிவுகளைப் பதிவிறக்கு (CSV)"
        empty_lbl = "பதிவுகள் எதுவும் இல்லை."
    elif current_lang == "te":
        tabs_labels = [
            "🌸 పూల కోత",
            "🍃 మొక్కల ఆరోగ్యం",
            "🧪 ఎరువుల రికార్డులు",
            "🔬 నేల పరీక్షలు",
            "🌦️ వాతావరణం మరియు నీటిపారుదల",
            "✂️ కత్తిరింపు రికార్డులు",
            "🗺️ మడులు మరియు తోట",
        ]
        btn_exp_harvest = "📥 కోత రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        btn_exp_health = "📥 ఆరోగ్య రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        btn_exp_fert = "📥 ఎరువుల రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        btn_exp_soil = "📥 నేల పరీక్ష రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        btn_exp_weath = "📥 వాతావరణ రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        btn_exp_prun = "📥 కత్తిరింపు రికార్డులను డౌన్‌లోడ్ చేయి (CSV)"
        empty_lbl = "ఇంకా వివరాలు నమోదు కాలేదు."
    else:
        tabs_labels = [
            "🌸 Flower Harvests",
            "🍃 Plant Health",
            "🧪 Fertilizer Logs",
            "🔬 Soil Tests",
            "🌦️ Weather & Irrigation",
            "✂️ Pruning",
            "🗺️ Farm & Sections",
        ]
        btn_exp_harvest = "📥 Export Harvest Records (CSV)"
        btn_exp_health = "📥 Export Health Records (CSV)"
        btn_exp_fert = "📥 Export Fertilizer Records (CSV)"
        btn_exp_soil = "📥 Export Soil Test Records (CSV)"
        btn_exp_weath = "📥 Export Weather & Irrigation Logs (CSV)"
        btn_exp_prun = "📥 Export Pruning Records (CSV)"
        empty_lbl = "No records found in database."

    tab_harvest, tab_health, tab_fert, tab_soil, tab_weath, tab_prun, tab_sections = st.tabs(tabs_labels)

    with tab_harvest:
        h_title = "மலர் அறுவடைப் பதிவுகள்" if current_lang == "ta" else ("పూల కోత పరిశీలనలు" if current_lang == "te" else "Flower Harvest & Staging Observations")
        st.markdown(f"### 🌸 {h_title}")
        if st.session_state.harvest_records:
            df_h = pd.DataFrame(st.session_state.harvest_records)
            st.dataframe(df_h, use_container_width=True, hide_index=True)
            csv_h = df_h.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_harvest, data=csv_h, file_name="jasmine_harvest_records.csv", mime="text/csv", key="dl_harvest")
        else:
            st.info(empty_lbl)

    with tab_health:
        hl_title = "பயிர் நலம் மற்றும் சேத ஆய்வுகள்" if current_lang == "ta" else ("మొక్కల ఆరోగ్యం మరియు నష్టాల పరిశీలనలు" if current_lang == "te" else "Plant Health & Damage Observations")
        st.markdown(f"### 🍃 {hl_title}")
        if st.session_state.plant_health_records:
            df_health = pd.DataFrame(st.session_state.plant_health_records)
            st.dataframe(df_health, use_container_width=True, hide_index=True)
            csv_hl = df_health.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_health, data=csv_hl, file_name="jasmine_plant_health_records.csv", mime="text/csv", key="dl_health")
        else:
            st.info(empty_lbl)

    with tab_fert:
        f_title = "உரமிடுதல் பதிவுகள்" if current_lang == "ta" else ("ఎరువుల వినియోగ రికార్డులు" if current_lang == "te" else "Fertilizer & Nutrient Applications")
        st.markdown(f"### 🧪 {f_title}")
        if st.session_state.fertilizer_records:
            df_f = pd.DataFrame(st.session_state.fertilizer_records)
            st.dataframe(df_f, use_container_width=True, hide_index=True)
            csv_f = df_f.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_fert, data=csv_f, file_name="jasmine_fertilizer_records.csv", mime="text/csv", key="dl_fert")
        else:
            st.info(empty_lbl)

    with tab_soil:
        s_title = "மண் பரிசோதனை அறிக்கைகள்" if current_lang == "ta" else ("నేల పరీక్ష నివేదికలు" if current_lang == "te" else "Soil Health Reports")
        st.markdown(f"### 🔬 {s_title}")
        if st.session_state.soil_test_records:
            df_s = pd.DataFrame(st.session_state.soil_test_records)
            st.dataframe(df_s, use_container_width=True, hide_index=True)
            csv_s = df_s.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_soil, data=csv_s, file_name="jasmine_soil_tests.csv", mime="text/csv", key="dl_soil")
        else:
            st.info(empty_lbl)

    with tab_weath:
        w_title = "வானிலை மற்றும் பாசன பதிவுகள்" if current_lang == "ta" else ("వాతావరణ మరియు నీటిపారుదల రికార్డులు" if current_lang == "te" else "Weather & Irrigation Logs")
        st.markdown(f"### 🌦️ {w_title}")
        if st.session_state.weather_irrigation_records:
            df_w = pd.DataFrame(st.session_state.weather_irrigation_records)
            st.dataframe(df_w, use_container_width=True, hide_index=True)
            csv_w = df_w.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_weath, data=csv_w, file_name="jasmine_weather_irrigation.csv", mime="text/csv", key="dl_weath")
        else:
            st.info(empty_lbl)

    with tab_prun:
        p_title = "கவாத்து பதிவுகள்" if current_lang == "ta" else ("కత్తిరింపు రికార్డులు" if current_lang == "te" else "Pruning Interventions")
        st.markdown(f"### ✂️ {p_title}")
        if st.session_state.pruning_records:
            df_p = pd.DataFrame(st.session_state.pruning_records)
            st.dataframe(df_p, use_container_width=True, hide_index=True)
            csv_p = df_p.to_csv(index=False).encode("utf-8")
            st.download_button(btn_exp_prun, data=csv_p, file_name="jasmine_pruning_records.csv", mime="text/csv", key="dl_prun")
        else:
            st.info(empty_lbl)

    with tab_sections:
        sec_title = "பாத்திகள் மற்றும் பண்ணை விவரம்" if current_lang == "ta" else ("మడులు మరియు తోట వివరాలు" if current_lang == "te" else "Garden Sections & Farm Profile")
        st.markdown(f"### 🗺️ {sec_title}")
        if st.session_state.farm_profile:
            fp = st.session_state.farm_profile
            st.markdown(
                f"""
                <div class="farm-card">
                    <b>{t('garden_context_title', current_lang)}:</b> {fp.get('farm_name', '')}<br>
                    <b>{t('cultivation_method', current_lang)}:</b> {fp.get('cultivation_method', '')}<br>
                    <b>{t('garden_crop', current_lang)}:</b> {fp.get('crop_variety', '')}<br>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.session_state.garden_sections:
            df_sec = pd.DataFrame(st.session_state.garden_sections)
            st.dataframe(df_sec, use_container_width=True, hide_index=True)
