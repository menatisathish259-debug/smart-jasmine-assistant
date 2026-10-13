"""
Plant Health and Damage Analysis Page (Module C).
Structured symptom logging separating visible observations from suspected causes.
"""

from datetime import date
from PIL import Image
import streamlit as st

from src.core.constants import VISIBLE_SYMPTOMS
from src.core.validation import validate_image_file
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_health_record


def render_plant_health(is_tamil: bool) -> None:
    """Renders the plant health and symptom analysis page."""
    render_page_header(
        title_en="Plant Health & Damage Observations (Module C)",
        title_ta="பயிர் நலம் மற்றும் சேதக் கண்காணிப்பு (பகுதி C)",
        subtitle_en="Record visible crop abnormalities while separating observations from suspected causes",
        subtitle_ta="தென்படும் அறிகுறிகளைப் பதிவுசெய்து, சந்தேகிக்கப்படும் காரணங்களை முறைப்படி ஆராய்க",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Evidence-Based Logging Active. The system strictly separates visible observations from causes. No automated diagnosis without multi-source evidence.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Never apply chemical pesticides or fertilizers based solely on a leaf photograph. Check soil drainage, inspect root health, check underleaf pests with a hand lens, and seek local horticultural advice.",
        message_ta="புகைப்படத்தை மட்டுமே கொண்டு பூச்சிக்கொல்லிகளையோ உரங்களையோ பயன்படுத்த வேண்டாம். மண் ஈரப்பதம், வேர் நலம் மற்றும் இலைக்கு அடியில் உள்ள பூச்சிகளை ஆய்வு செய்து உறுதிப்படுத்தவும்.",
        is_tamil=is_tamil,
    )

    col_form, col_guide = st.columns([1, 1])

    with col_form:
        st.markdown("### 🔍 1. Log Visible Symptoms (அறிகுறிகளைப் பதிவுசெய்க)")

        with st.form("plant_health_form"):
            obs_date = st.date_input("Date / தேதி:", value=date.today(), max_value=date.today(), key="health_date")
            garden_section = st.selectbox(
                "Garden Section / பாத்தி:",
                options=[
                    "Section A (North Bed)",
                    "Section B (South Bed)",
                    "Section C (East Plot)",
                    "Section D (West Plot)",
                    "Whole Garden",
                ],
                key="health_section",
            )

            st.markdown("**Visible Observations (What you actually see):**")
            sym_yellow = st.checkbox("Yellowing leaves (இலைகள் மஞ்சள் நிறமாதல்)", key="sym_yellow")
            sym_curled = st.checkbox("Curled or distorted leaves (இலைகள் சுருங்குதல்)", key="sym_curled")
            sym_bud_drop = st.checkbox("Flower buds dropping prematurely (மொட்டுக்கள் உதிர்தல்)", key="sym_bud_drop")
            sym_brown_bud = st.checkbox("Brown, rotting, or pierced buds (துளையிடப்பட்ட / பழுப்பு மொட்டுகள்)", key="sym_brown_bud")
            sym_feeding = st.checkbox("Visible feeding holes / webbing (பூச்சி கடி தடம் / வலை)", key="sym_feeding")

            col_p, col_s = st.columns(2)
            with col_p:
                affected_part = st.selectbox(
                    "Affected Area / தாக்கப்பட்ட பகுதி:",
                    options=["Older lower leaves", "New tender flush", "Bud clusters & stalks", "Entire bush"],
                    key="health_part",
                )
            with col_s:
                severity = st.selectbox(
                    "Severity / தீவிரத்தன்மை:",
                    options=["Mild (<10% affected)", "Moderate (10-30% affected)", "Severe (>30% affected)"],
                    key="health_severity",
                )

            st.markdown("**Suspected Causes (To be investigated, not yet confirmed):**")
            suspected_list = st.multiselect(
                "Potential factors under investigation:",
                options=[
                    "Poor soil drainage / Root suffocation",
                    "Thrips or spider mites (underleaf)",
                    "Jasmine Bud Worm (Hendecasis duplifascialis)",
                    "Blossom Midge (Contarinia maculipennis)",
                    "Nitrogen or micronutrient deficiency (Iron/Zinc/Boron)",
                    "High daytime heat or dry wind stress",
                    "Over-fertilization / Fertilizer burn",
                ],
                key="health_suspected",
            )

            notes = st.text_area(
                "Field Inspection Notes / கள ஆய்வு குறிப்புகள்:",
                placeholder="e.g., Noticed yellowing on lower leaves after heavy watering. Soil surface stayed wet for 3 days.",
                key="health_notes",
            )

            submit_health = st.form_submit_button("💾 Save Health Observation", use_container_width=True)

        if submit_health:
            selected_symptoms = []
            if sym_yellow: selected_symptoms.append("Yellowing leaves")
            if sym_curled: selected_symptoms.append("Curled leaves")
            if sym_bud_drop: selected_symptoms.append("Bud dropping")
            if sym_brown_bud: selected_symptoms.append("Brown / damaged buds")
            if sym_feeding: selected_symptoms.append("Feeding holes / webbing")

            if not selected_symptoms:
                st.warning("Please check at least one visible symptom.")
            else:
                record = {
                    "date": str(obs_date),
                    "section": garden_section,
                    "visible_symptoms": selected_symptoms,
                    "affected_part": affected_part,
                    "severity": severity,
                    "suspected_causes": suspected_list if suspected_list else ["Investigation pending"],
                    "confirmed_diagnosis": "Unconfirmed — Field verification required",
                    "status": "Under Investigation",
                    "notes": notes or "No extra notes.",
                }
                add_health_record(record)
                st.success("✅ Plant health observation logged successfully!")

    with col_guide:
        st.markdown("### 🔬 2. Investigation Protocol (கள ஆய்வு வழிகாட்டி)")
        st.caption("How to investigate common jasmine abnormalities scientifically:")

        for sym_key, sym_info in VISIBLE_SYMPTOMS.items():
            with st.expander(f"📌 {sym_info['name_en']} ({sym_info['name_ta']})", expanded=False):
                st.markdown(f"**Visible Sign:** {sym_info['observations']}")
                st.markdown("**Potential Causes to Investigate:**")
                for cause in sym_info["potential_causes"]:
                    st.markdown(f"- {cause}")
                st.info(f"🔎 **Investigation Step:** {sym_info['investigation_step']}")

        st.markdown("### 📸 Optional Symptom Photograph")
        uploaded_sym = st.file_uploader(
            "Upload photo of symptomatic leaf or damaged bud:",
            type=["jpg", "jpeg", "png", "webp"],
            key="sym_photo_uploader",
        )
        if uploaded_sym:
            v_ok, v_msg, v_meta = validate_image_file(uploaded_sym)
            if v_ok:
                st.image(Image.open(uploaded_sym), caption=f"Symptom Record: {uploaded_sym.name}", use_container_width=True)
                st.success(f"✓ Image Verified ({v_meta['width']}x{v_meta['height']} px)")
            else:
                st.error(f"❌ {v_msg}")

    # -----------------------------------------------------------------------
    # History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📋 Logged Health Observations (பதிவு செய்யப்பட்ட ஆய்வுகள்)")
    if st.session_state.plant_health_records:
        import pandas as pd
        records_disp = []
        for r in st.session_state.plant_health_records:
            records_disp.append({
                "Date": r["date"],
                "Section": r["section"],
                "Symptoms": ", ".join(r["visible_symptoms"]) if isinstance(r["visible_symptoms"], list) else r["visible_symptoms"],
                "Part": r["affected_part"],
                "Severity": r["severity"],
                "Suspected Causes": ", ".join(r["suspected_causes"]) if isinstance(r["suspected_causes"], list) else r["suspected_causes"],
                "Diagnosis Status": r["confirmed_diagnosis"],
            })
        st.dataframe(pd.DataFrame(records_disp), use_container_width=True, hide_index=True)
    else:
        st.info("No plant health observations logged yet.")
