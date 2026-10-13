"""
Soil Health and Nutrient Tracking Page (Module F).
Records soil test results, validates pH against the 6.0-7.0 baseline, and flags soil constraints.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

from datetime import date
import pandas as pd
import streamlit as st

from config.settings import SOIL_PH_RANGE
from src.core.validation import validate_soil_ph
from src.core.i18n import (
    normalize_lang,
    t,
)
from src.database.repository import add_soil_test, get_soil_tests
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_soil_record


def render_soil_health(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the soil health records and agronomic analysis page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Soil Health & Nutrient Analysis (Module F)",
        title_ta="மண் நலம் மற்றும் பரிசோதனை முடிவுகள் (பகுதி F)",
        title_te="నేల ఆరోగ్యం మరియు పోషకాల విశ్లేషణ (విభాగం F)",
        subtitle_en="Track soil test reports, evaluate pH constraints (6.0-7.0), and assess drainage conditions",
        subtitle_ta="மண் பரிசோதனை முடிவுகளைப் பதிவுசெய்து, கார அமில நிலை மற்றும் வடிகால் வசதியை ஆராய்க",
        subtitle_te="నేల పరీక్ష నివేదికలను నమోదు చేసి, పి.హెచ్ స్థాయి మరియు నీటి పారుదల సౌలభ్యాన్ని పరిశీలించండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Soil Rule Engine Active. Target pH range (6.0-7.0) based on horticultural standards.",
        desc_ta="மண் விதி அமைப்பு செயலில் உள்ளது. உகந்த கார அமில அளவு ஆறு முதல் ஏழு ஆகும்.",
        desc_te="నేల నియమాల ఇంజిన్ సిద్ధంగా ఉంది. మల్లెకు అనువైన పి.హెచ్ పరిధి ఆరు నుండి ఏడు.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="Sandy loam is not the only suitable soil; well-drained red loams and clay loams with ample organic matter are also productive. Never guess missing nutrient figures; verify with an official soil test laboratory.",
        message_ta="செம்மண் மற்றும் களிமண் கலந்த நல்ல வடிகால் வசதி கொண்ட நிலங்களும் மல்லிக்கு ஏற்றவை. விடுபட்ட தகவல்களை சுயமாக யூகிக்காமல் முறையான மண் பரிசோதனை அறிக்கையை பயன்படுத்தவும்.",
        message_te="ఎర్ర నేలలు మరియు సేంద్రీయ కర్బనం గల బంక నేలలు కూడా మల్లెకు ఎంతో అనుకూలం. అంచనాలతో కాకుండా అధికారిక నేల పరీక్ష నివేదిక ఆధారంగా నిర్ణయాలు తీసుకోండి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    col_form, col_eval = st.columns([1, 1])

    with col_form:
        form_title = (
            "மண் பரிசோதனைப் பதிவு" if current_lang == "ta"
            else ("నేల పరీక్ష నమోదు" if current_lang == "te"
            else "Record Soil Test Report")
        )
        st.markdown(f"### 🧪 1. {form_title}")

        with st.form("soil_test_form"):
            test_date = st.date_input(t("test_date", current_lang), value=date.today(), max_value=date.today(), key="soil_date")

            sample_loc_val = (
                "மேல்மண் மாதிரி (0-15 செ.மீ ஆழம்)" if current_lang == "ta"
                else ("పై నేల నమూనా (0-15 సెం.మీ లోతు)" if current_lang == "te"
                else "Composite topsoil sample (0-15 cm depth)")
            )
            sample_location = st.text_input(t("sample_location", current_lang), value=sample_loc_val, key="soil_loc")

            col_ph, col_ec = st.columns(2)
            with col_ph:
                ph_value = st.number_input(
                    t("soil_ph", current_lang),
                    min_value=3.0,
                    max_value=10.0,
                    value=6.8,
                    step=0.1,
                    format="%.1f",
                    key="soil_ph",
                )
            with col_ec:
                ec_value = st.number_input(
                    t("soil_ec", current_lang),
                    min_value=0.0,
                    max_value=10.0,
                    value=0.4,
                    step=0.05,
                    format="%.2f",
                    key="soil_ec",
                )

            if current_lang == "ta":
                texture_options = [
                    "செம்மண் மணற்பாங்கான நிலம்",
                    "செம்மண் களிப்பாங்கான நிலம்",
                    "மணற்பாங்கான வண்டல் மண்",
                    "வண்டல் களிமண்",
                    "கரிசல் மண்",
                    "மற்ற மண் வகை",
                ]
                drainage_options = [
                    "நல்ல வடிகால் வசதி (நீர் தேங்காது)",
                    "மிதமான வடிகால் வசதி",
                    "மோசமான வடிகால் / நீர் தேங்கும் அபாயம்",
                ]
                n_opts = ["குறைவு (<280 கிலோ/ஹெக்)", "நடுத்தரம் (280-560 கிலோ/ஹெக்)", "அதிகம் (>560 கிலோ/ஹெக்)"]
                p_opts = ["குறைவு (<11 கிலோ/ஹெக்)", "நடுத்தரம் (11-22 கிலோ/ஹெக்)", "அதிகம் (>22 கிலோ/ஹெக்)"]
                k_opts = ["குறைவு (<118 கிலோ/ஹெக்)", "நடுத்தரம் (118-280 கிலோ/ஹெக்)", "அதிகம் (>280 கிலோ/ஹெக்)"]
            elif current_lang == "te":
                texture_options = [
                    "ఎర్ర ఇసుక నేల",
                    "ఎర్ర బంక నేల",
                    "ఇసుక ఒండ్రు నేల",
                    "బంక ఒండ్రు నేల",
                    "నల్ల రేగడి నేల",
                    "ఇతర నేల రకం",
                ]
                drainage_options = [
                    "మంచి నీటి పారుదల సౌకర్యం (నీరు నిలవదు)",
                    "మధ్యస్థ నీటి పారుదల",
                    "పేలవమైన పారుదల / నీరు నిలిచే ప్రమాదం",
                ]
                n_opts = ["తక్కువ (<280 కిలో/హెక్)", "మధ్యస్థం (280-560 కిలో/హెక్)", "ఎక్కువ (>560 కిలో/హెక్)"]
                p_opts = ["తక్కువ (<11 కిలో/హెక్)", "మధ్యస్థం (11-22 కిలో/హెక్)", "ఎక్కువ (>22 కిలో/హెక్)"]
                k_opts = ["తక్కువ (<118 కిలో/హెక్)", "మధ్యస్థం (118-280 కిలో/హెక్)", "ఎక్కువ (>280 కిలో/హెక్)"]
            else:
                texture_options = [
                    "Red sandy loam",
                    "Red clay loam",
                    "Sandy loam",
                    "Clay loam",
                    "Black soil with drainage",
                    "Other soil texture",
                ]
                drainage_options = [
                    "Well-drained (No standing water)",
                    "Moderate drainage",
                    "Poor drainage / Risk of standing water",
                ]
                n_opts = ["Low (<280 kg/ha)", "Medium (280-560 kg/ha)", "High (>560 kg/ha)"]
                p_opts = ["Low (<11 kg/ha)", "Medium (11-22 kg/ha)", "High (>22 kg/ha)"]
                k_opts = ["Low (<118 kg/ha)", "Medium (118-280 kg/ha)", "High (>280 kg/ha)"]

            texture = st.selectbox(t("soil_texture", current_lang), options=texture_options, key="soil_texture")
            drainage = st.selectbox("வடிகால் நிலை:" if current_lang == "ta" else ("పారుదల స్థితి:" if current_lang == "te" else "Drainage Condition:"), options=drainage_options, key="soil_drainage")

            col_n, col_p, col_k = st.columns(3)
            with col_n:
                n_status = st.selectbox("N:", n_opts, index=1, key="soil_n")
            with col_p:
                p_status = st.selectbox("P:", p_opts, index=1, key="soil_p")
            with col_k:
                k_status = st.selectbox("K:", k_opts, index=2, key="soil_k")

            organic_c = st.number_input(t("organic_carbon", current_lang), min_value=0.0, max_value=5.0, value=0.55, step=0.05, key="soil_oc")
            notes = st.text_area("குறிப்புகள்:" if current_lang == "ta" else ("గమనికలు:" if current_lang == "te" else "Lab Notes:"), placeholder="", key="soil_notes")

            btn_soil_lbl = (
                "💾 மண் பரிசோதனையைச் சேமி" if current_lang == "ta"
                else ("💾 నేల పరీక్షను భద్రపరచు" if current_lang == "te"
                else "💾 Save Soil Test Record")
            )
            submit_soil = st.form_submit_button(btn_soil_lbl, use_container_width=True)

        if submit_soil:
            record = {
                "date": str(test_date),
                "location": sample_location,
                "ph": ph_value,
                "texture": texture,
                "drainage": drainage,
                "ec_dsm": ec_value,
                "organic_carbon_pct": organic_c,
                "available_n": n_status,
                "available_p": p_status,
                "available_k": k_status,
                "notes": notes or "",
            }
            add_soil_test(
                test_date=str(test_date),
                sampling_location=sample_location,
                ph=ph_value,
                texture=texture,
                drainage=drainage,
                ec_dsm=ec_value,
                organic_carbon_pct=organic_c,
                available_n=n_status,
                available_p=p_status,
                available_k=k_status,
                notes=notes or "",
            )
            add_soil_record(record)
            saved_msg = (
                "✅ மண் பரிசோதனை அறிக்கை சேமிக்கப்பட்டது!" if current_lang == "ta"
                else ("✅ నేల పరీక్ష నివేదిక భద్రపరచబడింది!" if current_lang == "te"
                else "✅ Soil test report logged successfully in database!")
            )
            st.success(saved_msg)

    with col_eval:
        eval_title = (
            "நிகழ்நேர மண் ஆய்வு முடிவுகள்" if current_lang == "ta"
            else ("నేల విశ్లేషణ ఫలితాలు" if current_lang == "te"
            else "Real-Time Soil Constraint Evaluation")
        )
        st.markdown(f"### 🔬 2. {eval_title}")

        is_valid_ph, alert_type, ph_msg = validate_soil_ph(ph_value)

        if alert_type == "success":
            st.success(f"**✓ pH ({ph_value:.1f}):** {ph_msg}")
        elif alert_type == "warning":
            st.warning(f"**⚠️ pH ({ph_value:.1f}):** {ph_msg}")
        else:
            st.error(f"**❌ pH:** {ph_msg}")

        if "Poor" in drainage or "மோசமான" in drainage or "పేలవమైన" in drainage:
            drainage_err = (
                "**🚨 வடிகால் குறைபாடு:** மல்லி வேர்களுக்கு நல்ல காற்று சுழற்சி தேவை. நீர் தேங்கினால் வேரழுகல் நோய் ஏற்படும்." if current_lang == "ta"
                else ("**🚨 నీటి పారుదల లోపం:** మల్లె వేర్లకు మంచి గాలి పారుదల అవసరం. నీరు నిలిస్తే వేరు కుళ్లు తెగులు వస్తుంది." if current_lang == "te"
                else "**🚨 Poor Drainage Alert:** Jasmine roots require high aeration. Prolonged waterlogging causes collar rot.")
            )
            st.error(drainage_err)
        else:
            drainage_ok = (
                f"**வடிகால் நிலை:** {drainage}. ஆரோக்கியமான மொட்டு உற்பத்திக்கு ஏற்றது." if current_lang == "ta"
                else (f"**నీటి పారుదల స్థితి:** {drainage}. ఆరోగ్యకరమైన పూల ఉత్పత్తికి అనుకూలం." if current_lang == "te"
                else f"**Drainage Status:** {drainage}. Good soil pore aeration supports healthy bud production.")
            )
            st.info(drainage_ok)

    # -----------------------------------------------------------------------
    # Soil History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    hist_title = (
        "மண் பரிசோதனை வரலாறு" if current_lang == "ta"
        else ("నేల పరీక్షల చరిత్ర" if current_lang == "te"
        else "Soil Test History")
    )
    st.markdown(f"### 📋 {hist_title}")
    db_soil_records = get_soil_tests()
    if db_soil_records:
        df = pd.DataFrame(db_soil_records)
        disp_cols = [c for c in ["test_date", "sampling_location", "ph", "texture", "drainage", "ec_dsm", "organic_carbon_pct", "available_n", "available_p", "available_k"] if c in df.columns]
        st.dataframe(df[disp_cols], use_container_width=True, hide_index=True)
    elif st.session_state.soil_test_records:
        df = pd.DataFrame(st.session_state.soil_test_records)
        disp_cols = [c for c in ["date", "location", "ph", "texture", "drainage", "ec_dsm", "organic_carbon_pct", "available_n", "available_p", "available_k"] if c in df.columns]
        st.dataframe(df[disp_cols], use_container_width=True, hide_index=True)
    else:
        empty_lbl = (
            "பதிவுகள் எதுவும் இல்லை." if current_lang == "ta"
            else ("ఇంకా వివరాలు నమోదు కాలేదు." if current_lang == "te"
            else "No soil test records logged yet.")
        )
        st.info(empty_lbl)
