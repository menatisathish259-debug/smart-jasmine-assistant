"""
Soil Health and Nutrient Tracking Page (Module F).
Records soil test results, validates pH against the 6.0-7.0 baseline, and flags soil constraints.
"""

from datetime import date
import streamlit as st

from config.settings import SOIL_PH_RANGE
from src.core.validation import validate_soil_ph
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_soil_record


def render_soil_health(is_tamil: bool) -> None:
    """Renders the soil health records and agronomic analysis page."""
    render_page_header(
        title_en="Soil Health & Nutrient Analysis (Module F)",
        title_ta="மண் நலம் மற்றும் பரிசோதனை முடிவுகள் (பகுதி F)",
        subtitle_en="Track soil test reports, evaluate pH constraints (6.0-7.0), and assess drainage conditions",
        subtitle_ta="மண் பரிசோதனை முடிவுகளைப் பதிவுசெய்து, கார அமில நிலை (pH) மற்றும் வடிகால் வசதியை ஆராய்க",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Soil Rule Engine Active. Target pH range (6.0-7.0) based on horticultural standards. Missing soil test parameters are never fabricated.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Sandy loam is not the only suitable soil; well-drained red loams and clay loams with ample organic matter are also productive. Never guess missing nutrient figures; verify with an official soil test laboratory.",
        message_ta="செம்மண் மற்றும் களிமண் கலந்த நல்ல வடிகால் வசதி கொண்ட நிலங்களும் மல்லிக்கு ஏற்றவை. விடுபட்ட தகவல்களை சுயமாக யூகிக்காமல் முறையான மண் பரிசோதனை அறிக்கையை பயன்படுத்தவும்.",
        is_tamil=is_tamil,
    )

    col_form, col_eval = st.columns([1, 1])

    with col_form:
        st.markdown("### 🧪 1. Record Soil Test Report (மண் பரிசோதனைப் பதிவு)")

        with st.form("soil_test_form"):
            test_date = st.date_input("Test Date / பரிசோதனை தேதி:", value=date.today(), max_value=date.today(), key="soil_date")
            sample_location = st.text_input(
                "Sampling Depth & Location / இடம்:",
                value="Composite topsoil sample (0-15 cm depth), Center plot",
                key="soil_loc",
            )

            col_ph, col_ec = st.columns(2)
            with col_ph:
                ph_value = st.number_input(
                    "Soil pH / கார அமில நிலை:",
                    min_value=3.0,
                    max_value=10.0,
                    value=6.8,
                    step=0.1,
                    format="%.1f",
                    key="soil_ph",
                )
            with col_ec:
                ec_value = st.number_input(
                    "Electrical Conductivity (EC dS/m):",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.4,
                    step=0.05,
                    format="%.2f",
                    help="Normal for jasmine: < 1.0 dS/m",
                    key="soil_ec",
                )

            texture = st.selectbox(
                "Soil Texture / மண் வகை:",
                options=[
                    "Red sandy loam (செம்மண் மணற்பாங்கான நிலம்)",
                    "Red clay loam (செம்மண் களிப்பாங்கான நிலம்)",
                    "Sandy loam (மணற்பாங்கான வண்டல் மண்)",
                    "Clay loam (வண்டல் களிமண்)",
                    "Black soil with drainage (வடிகால் வசதியுடைய கரிசல் மண்)",
                    "Other soil texture",
                ],
                key="soil_texture",
            )

            drainage = st.selectbox(
                "Drainage Observation / வடிகால் நிலை:",
                options=[
                    "Well-drained (No water stays standing after 2 hours)",
                    "Moderate drainage (Slow percolation)",
                    "Poor drainage / Risk of standing water and waterlogging",
                ],
                key="soil_drainage",
            )

            col_n, col_p, col_k = st.columns(3)
            with col_n:
                n_status = st.selectbox("Available N:", ["Low (<280 kg/ha)", "Medium (280-560 kg/ha)", "High (>560 kg/ha)"], index=1, key="soil_n")
            with col_p:
                p_status = st.selectbox("Available P:", ["Low (<11 kg/ha)", "Medium (11-22 kg/ha)", "High (>22 kg/ha)"], index=1, key="soil_p")
            with col_k:
                k_status = st.selectbox("Available K:", ["Low (<118 kg/ha)", "Medium (118-280 kg/ha)", "High (>280 kg/ha)"], index=2, key="soil_k")

            organic_c = st.number_input("Organic Carbon (%) [Optional]:", min_value=0.0, max_value=5.0, value=0.55, step=0.05, key="soil_oc")
            notes = st.text_area("Lab Notes / ஆய்வகக் குறிப்புகள்:", placeholder="Official laboratory recommendations or micronutrient notes (Zinc, Iron, Boron)...", key="soil_notes")

            submit_soil = st.form_submit_button("💾 Save Soil Test Record", use_container_width=True)

        if submit_soil:
            is_valid_ph, alert_type, ph_msg = validate_soil_ph(ph_value)
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
                "notes": notes or "Standard soil test logged.",
            }
            add_soil_record(record)
            st.success("✅ Soil test report logged successfully!")

    with col_eval:
        st.markdown("### 🔬 2. Real-Time Soil Constraint Evaluation")
        st.caption("Agronomic interpretation of current pH and drainage:")

        is_valid_ph, alert_type, ph_msg = validate_soil_ph(ph_value)

        if alert_type == "success":
            st.success(f"**✓ pH Evaluation ({ph_value:.1f}):** {ph_msg}")
        elif alert_type == "warning":
            st.warning(f"**⚠️ pH Alert ({ph_value:.1f}):** {ph_msg}")
        else:
            st.error(f"**❌ pH Error:** {ph_msg}")

        # Drainage check
        if "Poor" in drainage:
            st.error(
                "**🚨 Severe Constraint - Poor Drainage:** Jasmine roots require high aeration. "
                "Waterlogging for more than 24 hours induces root asphyxiation, yellow leaves, bud drop, and collar rot."
            )
        else:
            st.info(f"**Drainage Status:** {drainage}. Good soil pore aeration supports healthy bud production.")

        # Soil Texture Insights
        st.markdown(
            f"""
            <div class="farm-card">
                <b>Cultivation Reference for {texture.split('(')[0].strip()}:</b><br>
                • <b>Organic Matter Requirement:</b> Maintain 10-15 tonnes/ha FYM or vermicompost to preserve moisture and nutrient retention.<br>
                • <b>Irrigation Interval:</b> Light, frequent watering rather than heavy flooding.<br>
                • <b>Root Penetration:</b> Jasminum sambac roots are fibrous and branch predominantly in the upper 30-45 cm of ground soil.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Soil History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📋 Soil Test History (மண் பரிசோதனை வரலாறு)")
    if st.session_state.soil_test_records:
        import pandas as pd
        df = pd.DataFrame(st.session_state.soil_test_records)
        disp_cols = [c for c in ["date", "location", "ph", "texture", "drainage", "ec_dsm", "organic_carbon_pct", "available_n", "available_p", "available_k"] if c in df.columns]
        st.dataframe(df[disp_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No soil test records logged yet.")
