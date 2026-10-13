"""
Weather and Irrigation Tracking Page (Module G).
Monitors climatic conditions, logs irrigation events, and guides moisture management.
"""

from datetime import date
import streamlit as st

from config.settings import WEATHER_CITY
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_weather_irrigation_record


def render_weather_irrigation(is_tamil: bool) -> None:
    """Renders the weather observations and irrigation management page."""
    render_page_header(
        title_en="Weather & Irrigation Tracking (Module G)",
        title_ta="வானிலை மற்றும் பாசன மேலாண்மை (பகுதி G)",
        subtitle_en="Track temperature, rainfall, and root-zone moisture to optimize irrigation timing",
        subtitle_ta="வெப்பநிலை, மழை மற்றும் வேர்ப்பகுதி ஈரப்பதத்தை கண்காணித்து சரியான பாசன முடிவுகளை எடுங்கள்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Field Observation Active. Automated Weather API integration will connect in Phase 10. Manual field logging enabled.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Do not determine irrigation requirements or diagnose disease from weather data alone. Always verify soil moisture at 15–30 cm root depth before running irrigation.",
        message_ta="வானிலை தகவலை மட்டும் வைத்து பாசன முடிவையோ அல்லது நோய் தாக்குதலையோ கணிக்க வேண்டாம். 15-30 செ.மீ வேர்ப்பகுதி ஈரப்பதத்தை நேரில் பார்த்து பாசனம் செய்யவும்.",
        is_tamil=is_tamil,
    )

    col_input, col_advisory = st.columns([1, 1])

    with col_input:
        st.markdown(f"### 🌦️ 1. Log Field Weather & Irrigation ({WEATHER_CITY} Region)")

        with st.form("weather_irrigation_form"):
            log_date = st.date_input("Date / தேதி:", value=date.today(), max_value=date.today(), key="weath_date")

            col_t, col_h = st.columns(2)
            with col_t:
                temp_c = st.number_input("Day Temperature (°C):", min_value=15.0, max_value=50.0, value=33.0, step=0.5, key="weath_temp")
            with col_h:
                humidity_pct = st.number_input("Relative Humidity (%):", min_value=10.0, max_value=100.0, value=65.0, step=1.0, key="weath_hum")

            col_r, col_f = st.columns(2)
            with col_r:
                rainfall_mm = st.number_input("Rainfall Today (mm):", min_value=0.0, max_value=500.0, value=0.0, step=1.0, key="weath_rain")
            with col_f:
                forecast_rain_mm = st.number_input("Forecast 24h Rain (mm):", min_value=0.0, max_value=500.0, value=0.0, step=1.0, key="weath_forecast")

            st.markdown("**Irrigation Execution:**")
            was_irrigated = st.checkbox("Irrigated Today? (இன்று பாசனம் செய்யப்பட்டதா?)", value=True, key="weath_irrig_done")

            irrig_method = st.selectbox(
                "Irrigation Method / பாசன முறை:",
                options=[
                    "Basin irrigation around root rings (15-20 cm depth)",
                    "Drip irrigation along row beds",
                    "Furrow irrigation between planted rows",
                    "No irrigation (Soil sufficiently moist)",
                ],
                key="weath_method",
            )

            moisture_depth = st.selectbox(
                "Soil Moisture at 15–20 cm Root Depth:",
                options=[
                    "Optimal crumbly moist (Ideal for flower bud growth)",
                    "Dry and powdery (Irrigation urgently needed)",
                    "Wet and sticky / Saturated (Risk of waterlogging - Stop irrigation)",
                ],
                key="weath_moisture",
            )

            notes = st.text_area("Field Climatic Notes / குறிப்புகள்:", placeholder="e.g., Heavy dry winds in afternoon, flower petals slightly dry at tips...", key="weath_notes")

            submit_weath = st.form_submit_button("💾 Save Weather & Irrigation Record", use_container_width=True)

        if submit_weath:
            record = {
                "date": str(log_date),
                "weather_temp_c": temp_c,
                "humidity_pct": humidity_pct,
                "rainfall_mm": rainfall_mm,
                "forecast_rain_mm": forecast_rain_mm,
                "irrigation_done": was_irrigated,
                "method": irrig_method,
                "depth_moisture_cm": moisture_depth,
                "notes": notes or "Daily observation logged.",
            }
            add_weather_irrigation_record(record)
            st.success("✅ Weather and irrigation record saved!")

    with col_advisory:
        st.markdown("### 💧 2. Jasminum sambac Irrigation Guidelines")
        st.caption("Evidence-based water management rules:")

        st.markdown(
            """
            <div class="farm-card">
                <b>1. Peak Flowering Season (March to August):</b><br>
                Jasmine requires consistent soil moisture. Water once every 4 to 6 days depending on temperature and soil drainage. Never flood the garden.<br><br>
                <b>2. Water Withholding for Pruning (Nov - Dec):</b><br>
                Stop watering 10–15 days before pruning. This induces foliage drop and concentrates bush carbohydrates for uniform bud emergence after post-pruning watering and manuring.<br><br>
                <b>3. Overhead Sprinklers Caution:</b><br>
                Avoid overhead wetting during flowering. Water droplets on mature white buds promote blossom blight (*Botrytis cinerea*) and stain petals brown.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if forecast_rain_mm > 15.0:
            st.warning(
                f"⚠️ **Rainfall Alert:** {forecast_rain_mm:.1f} mm forecast. "
                "Postpone planned irrigation and ensure drainage furrows are cleared to prevent root collar water stagnation."
            )

    # -----------------------------------------------------------------------
    # History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📋 Weather & Irrigation History (பதிவுகள்)")
    if st.session_state.weather_irrigation_records:
        import pandas as pd
        df = pd.DataFrame(st.session_state.weather_irrigation_records)
        disp_cols = [c for c in ["date", "weather_temp_c", "humidity_pct", "rainfall_mm", "irrigation_done", "method", "depth_moisture_cm", "notes"] if c in df.columns]
        st.dataframe(df[disp_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No weather or irrigation records logged yet.")
