"""
Weather and Irrigation Tracking Page (Module G).
Monitors climatic conditions, logs irrigation events, guides moisture management,
and generates multi-factor agronomic advisories cross-referencing soil and fertilization.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

from datetime import date
import pandas as pd
import streamlit as st

from config.settings import WEATHER_CITY
from src.agronomy.decision_support import generate_integrated_agronomic_advisory
from src.core.i18n import (
    normalize_lang,
    t,
)
from src.database.repository import (
    add_irrigation_record,
    get_irrigation_records,
    get_latest_soil_test_by_section,
    get_total_nutrients_applied,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_weather_irrigation_record


def render_weather_irrigation(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the weather observations and irrigation management page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Weather & Irrigation Tracking (Module G)",
        title_ta="வானிலை மற்றும் பாசன மேலாண்மை (பகுதி G)",
        title_te="వాతావరణం మరియు నీటిపారుదల నిర్వహణ (విభాగం G)",
        subtitle_en="Track temperature, rainfall, and root-zone moisture to optimize irrigation and fertilization timing",
        subtitle_ta="வெப்பநிலை, மழை மற்றும் வேர்ப்பகுதி ஈரப்பதத்தை கண்காணித்து சரியான பாசன முடிவுகளை எடுங்கள்",
        subtitle_te="ఉష్ణోగ్రత, వర్షపాతం మరియు వేర్ల తేమను పరిశీలించి సకాలంలో నీటి యాజమాన్య నిర్ణయాలు తీసుకోండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Field Observation & Advisory Active. Cross-references climatic data with soil moisture and fertilizer safety rules.",
        desc_ta="களக் கண்காணிப்பு செயலில் உள்ளது. காலநிலை மற்றும் மண் விதிகள் ஒருங்கிணைக்கப்படுகின்றன.",
        desc_te="క్షేత్ర పరిశీలన సిద్ధంగా ఉంది. వాతావరణం మరియు నేల నియమాలు సమన్వయం చేయబడ్డాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="Do not determine irrigation requirements or diagnose disease from weather data alone. Always verify soil moisture at 15–30 cm root depth before running irrigation.",
        message_ta="வானிலை தகவலை மட்டும் வைத்து பாசன முடிவையோ அல்லது நோய் தாக்குதலையோ கணிக்க வேண்டாம். வேர்ப்பகுதி ஈரப்பதத்தை நேரில் பார்த்து பாசனம் செய்யவும்.",
        message_te="వాతావరణ సమాచారం ఆధారంగా మాత్రమే నీరు పెట్టవద్దు. వేర్ల భాగంలో తేమను స్వయంగా చూసి నీటిని అందించండి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    latest_soil = get_latest_soil_test_by_section(None)
    soil_ph = latest_soil["ph"] if latest_soil else 6.8
    soil_drainage = latest_soil["drainage"] if latest_soil else "Well-drained"
    totals = get_total_nutrients_applied()

    col_input, col_advisory = st.columns([1, 1])

    with col_input:
        f_title = (
            f"வானிலை மற்றும் பாசனம் ({WEATHER_CITY} பகுதி)" if current_lang == "ta"
            else (f"వాతావరణం మరియు నీటిపారుదల ({WEATHER_CITY} ప్రాంతం)" if current_lang == "te"
            else f"Log Field Weather & Irrigation ({WEATHER_CITY} Region)")
        )
        st.markdown(f"### 🌦️ 1. {f_title}")

        with st.form("weather_irrigation_form"):
            date_lbl = "தேதி:" if current_lang == "ta" else ("తేదీ:" if current_lang == "te" else "Date:")
            log_date = st.date_input(date_lbl, value=date.today(), max_value=date.today(), key="weath_date")

            col_t, col_h = st.columns(2)
            with col_t:
                temp_c = st.number_input(t("day_temp", current_lang), min_value=15.0, max_value=50.0, value=33.5, step=0.5, key="weath_temp")
            with col_h:
                humidity_pct = st.number_input(t("rel_humidity", current_lang), min_value=10.0, max_value=100.0, value=65.0, step=1.0, key="weath_hum")

            col_r, col_f = st.columns(2)
            with col_r:
                rainfall_mm = st.number_input(t("rainfall_today", current_lang), min_value=0.0, max_value=500.0, value=0.0, step=1.0, key="weath_rain")
            with col_f:
                forecast_rain_mm = st.number_input(t("rainfall_forecast", current_lang), min_value=0.0, max_value=500.0, value=0.0, step=1.0, key="weath_forecast")

            irrig_done_lbl = (
                "இன்று நீர் பாய்ச்சப்பட்டதா?" if current_lang == "ta"
                else ("నేడు నీరు పెట్టారా?" if current_lang == "te"
                else "Irrigated Today?")
            )
            was_irrigated = st.checkbox(irrig_done_lbl, value=True, key="weath_irrig_done")

            if current_lang == "ta":
                method_options = [
                    "செடியைச் சுற்றி பாத்தி கட்டி நீர் பாய்ச்சுதல்",
                    "வரிசை சொட்டுநீர் பாசனம்",
                    "வாய்க்கால் பாசனம்",
                    "நீர் பாய்ச்சப்படவில்லை",
                ]
                moisture_options = [
                    "உகந்த ஈரப்பதம் (பூக்களுக்கு ஏற்றது)",
                    "வறண்ட மண் (உடனடி பாசனம் தேவை)",
                    "அதிக நீர் தேக்கம் (பாசனத்தை நிறுத்தவும்)",
                ]
            elif current_lang == "te":
                method_options = [
                    "మొక్క చుట్టూ పాదు కట్టి నీరు పెట్టడం",
                    "డ్రిప్ నీటిపారుదల",
                    "సాల్వల ద్వారా పారుదల",
                    "నీరు పెట్టలేదు",
                ]
                moisture_options = [
                    "తగినంత తేమ (పూతకు అనుకూలం)",
                    "ఎండిన నేల (వెంటనే నీరు పెట్టాలి)",
                    "నీరు నిలిచి ఉంది (నీరు పెట్టడం ఆపండి)",
                ]
            else:
                method_options = [
                    "Basin irrigation around root rings",
                    "Drip irrigation along row beds",
                    "Furrow irrigation between planted rows",
                    "No irrigation (Soil sufficiently moist)",
                ]
                moisture_options = [
                    "Optimal crumbly moist (Ideal for buds)",
                    "Dry and powdery (Irrigation urgently needed)",
                    "Wet and sticky / Saturated (Stop irrigation)",
                ]

            irrig_method = st.selectbox(t("irrig_method", current_lang), options=method_options, key="weath_method")
            moisture_depth = st.selectbox(t("soil_moisture_level", current_lang), options=moisture_options, key="weath_moisture")

            notes_lbl = "குறிப்புகள்:" if current_lang == "ta" else ("గమనికలు:" if current_lang == "te" else "Field Climatic Notes:")
            notes = st.text_area(notes_lbl, placeholder="", key="weath_notes")

            submit_lbl = (
                "💾 வானிலை மற்றும் பாசனப் பதிவைச் சேமி" if current_lang == "ta"
                else ("💾 వాతావరణ మరియు పారుదల వివరాలను భద్రపరచు" if current_lang == "te"
                else "💾 Save Weather & Irrigation Record")
            )
            submit_weath = st.form_submit_button(submit_lbl, use_container_width=True)

        if submit_weath:
            add_irrigation_record(
                irrigation_date=str(log_date),
                was_irrigated=was_irrigated,
                method=irrig_method,
                moisture_depth_observation=moisture_depth,
                weather_temp_c=temp_c,
                humidity_pct=humidity_pct,
                rainfall_mm=rainfall_mm,
                forecast_rain_mm=forecast_rain_mm,
                notes=notes or "",
            )

            record = {
                "date": str(log_date),
                "weather_temp_c": temp_c,
                "humidity_pct": humidity_pct,
                "rainfall_mm": rainfall_mm,
                "forecast_rain_mm": forecast_rain_mm,
                "irrigation_done": was_irrigated,
                "method": irrig_method,
                "depth_moisture_cm": moisture_depth,
                "notes": notes or "",
            }
            add_weather_irrigation_record(record)
            saved_msg = (
                "✅ வானிலை மற்றும் பாசனப் பதிவு சேமிக்கப்பட்டது!" if current_lang == "ta"
                else ("✅ వివరాలు విజయవంతంగా భద్రపరచబడ్డాయి!" if current_lang == "te"
                else "✅ Weather and irrigation record saved to SQLite database!")
            )
            st.success(saved_msg)
            st.rerun()

    with col_advisory:
        adv_title = (
            "ஒருங்கிணைந்த வேளாண் ஆலோசனை" if current_lang == "ta"
            else ("సమన్వయ వ్యవసాయ సలహా" if current_lang == "te"
            else "Integrated Agronomic Weather Advisory")
        )
        st.markdown(f"### 🌾 2. {adv_title}")

        advisory_res = generate_integrated_agronomic_advisory(
            soil_ph=soil_ph,
            soil_drainage=soil_drainage,
            root_moisture_depth_cm=moisture_depth,
            temp_c=temp_c,
            humidity_pct=humidity_pct,
            rainfall_today_mm=rainfall_mm,
            forecast_rain_mm=forecast_rain_mm,
            cumulative_n_kg=totals["total_n"],
            cumulative_p_kg=totals["total_p"],
            cumulative_k_kg=totals["total_k"],
            plant_count=2000,
        )

        for warn in advisory_res["safety_warnings"]:
            st.error(warn)

        for adv in advisory_res["advisories"]:
            st.info(f"💡 {adv}")

        st.warning(advisory_res["non_prescription_guardrail"])

        st.markdown("---")
        rules_head = (
            "மல்லி பாசன மேலாண்மை நெறிமுறைகள்" if current_lang == "ta"
            else ("మల్లె తోట నీటి యాజమాన్య సూత్రాలు" if current_lang == "te"
            else "Jasminum sambac Water Management Standards")
        )
        st.markdown(f"### 💧 {rules_head}")

        if current_lang == "ta":
            rules_content = """
            <div class="farm-card">
                <b>1. உச்ச பூக்கும் பருவம் (மார்ச் - ஆகஸ்ட்):</b><br>
                மல்லிக்கு சீரான மண் ஈரப்பதம் அவசியம். வெப்பம் மற்றும் வடிகாலுக்கு ஏற்ப 4 முதல் 6 நாட்களுக்கு ஒருமுறை நீர் பாய்ச்சவும்.<br><br>
                <b>2. கவாத்துக்கான நீர் நிறுத்தம் (நவம்பர் - டிசம்பர்):</b><br>
                கவாத்துக்கு 10-15 நாட்களுக்கு முன் நீர் பாய்ச்சுவதை நிறுத்தவும். இதனால் இலைகள் உதிர்ந்து புது தளிர்கள் ஒரே சீராக வரும்.<br><br>
                <b>3. மேல் தெளிப்பான் எச்சரிக்கை:</b><br>
                பூக்கும் போது மேலே இருந்து நீர் தெளிப்பதை தவிர்க்கவும். மொட்டுகளின் மேல் நீர் பட்டால் பழுப்பு நிற புள்ளிகள் ஏற்படும்.
            </div>
            """
        elif current_lang == "te":
            rules_content = """
            <div class="farm-card">
                <b>1. అధిక పూత సమయం (మార్చి నుండి ఆగస్టు):</b><br>
                మల్లెకు స్థిరమైన తేమ అవసరం. ఉష్ణోగ్రత మరియు నేలను బట్టి ప్రతి 4 నుండి 6 రోజులకు ఒకసారి నీరు పెట్టాలి.<br><br>
                <b>2. కత్తిరింపు కోసం నీరు ఆపడం (నవంబర్ - డిసెంబర్):</b><br>
                కత్తిరింపుకు 10-15 రోజుల ముందు నీరు పెట్టడం ఆపాలి. దీనివల్ల ఆకులు రాలి, కత్తిరింపు తర్వాత కొత్త చిగుళ్లు ఏకరీతిగా వస్తాయి.<br><br>
                <b>3. స్ప్రింక్లర్ల వాడకంలో జాగ్రత్త:</b><br>
                పూత సమయంలో ఆకులపై పైనుండి నీరు చిమ్మవద్దు. మొగ్గలపై నీటి బిందువులు పడితే మచ్చలు ఏర్పడతాయి.
            </div>
            """
        else:
            rules_content = """
            <div class="farm-card">
                <b>1. Peak Flowering Season (March to August):</b><br>
                Jasmine requires consistent soil moisture. Water once every 4 to 6 days depending on temperature and drainage.<br><br>
                <b>2. Water Withholding for Pruning (Nov - Dec):</b><br>
                Stop watering 10–15 days before pruning to induce leaf drop for uniform bud emergence.<br><br>
                <b>3. Overhead Sprinklers Caution:</b><br>
                Avoid overhead wetting during flowering to prevent petal staining and blossom blight.
            </div>
            """
        st.markdown(rules_content, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    hist_title = (
        "வானிலை மற்றும் பாசன பதிவுகள்" if current_lang == "ta"
        else ("వాతావరణ మరియు పారుదల చరిత్ర" if current_lang == "te"
        else "Weather & Irrigation History")
    )
    st.markdown(f"### 📋 {hist_title}")
    db_irrig = get_irrigation_records()
    if db_irrig:
        disp_cols = ["irrigation_date", "weather_temp_c", "humidity_pct", "rainfall_mm", "forecast_rain_mm", "was_irrigated", "method", "moisture_depth_observation"]
        df_irrig = pd.DataFrame(db_irrig)
        valid_cols = [c for c in disp_cols if c in df_irrig.columns]
        st.dataframe(df_irrig[valid_cols], use_container_width=True, hide_index=True)
    elif st.session_state.weather_irrigation_records:
        df = pd.DataFrame(st.session_state.weather_irrigation_records)
        disp_cols = [c for c in ["date", "weather_temp_c", "humidity_pct", "rainfall_mm", "irrigation_done", "method", "depth_moisture_cm", "notes"] if c in df.columns]
        st.dataframe(df[disp_cols], use_container_width=True, hide_index=True)
    else:
        st.info("பதிவுகள் எதுவும் இல்லை." if current_lang == "ta" else ("ఇంకా వివరాలు నమోదు కాలేదు." if current_lang == "te" else "No weather or irrigation records logged yet."))
