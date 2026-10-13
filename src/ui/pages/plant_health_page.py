"""
Plant Health and Damage Analysis Page (Module C).
Structured symptom logging strictly separating visible observations from confirmed causes.
Provides differential diagnostic hypotheses, missing information audits, and expert referral conditions.
"""

from datetime import date
from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

from src.agronomy.plant_health_engine import (
    analyze_plant_health_observations,
    VISIBLE_SYMPTOMS_CATALOG,
    DIFFERENTIAL_DIAGNOSES,
)
from src.core.validation import validate_image_file
from src.database.repository import (
    add_plant_observation,
    get_plant_observations,
    update_plant_observation_diagnosis,
    get_latest_soil_test_by_section,
    get_garden_sections,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_health_record


def render_plant_health(is_tamil: bool) -> None:
    """Renders the upgraded plant health and symptom analysis page."""
    render_page_header(
        title_en="Plant Health & Damage Observations (Module C)",
        title_ta="பயிர் நலம் மற்றும் சேதக் கண்காணிப்பு (பகுதி C)",
        subtitle_en="Record visible crop abnormalities while strictly separating physical observations from confirmed diagnoses",
        subtitle_ta="தென்படும் அறிகுறிகளைப் பதிவுசெய்து, சந்தேகிக்கப்படும் காரணங்களை முறைப்படி ஆராய்க",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Evidence-Based Diagnostic Engine Active. Separates visible symptoms from inferred causes. Shows missing information and expert-referral conditions.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="NEVER prescribe chemical pesticides or fertilizer rates based solely on photographs. Always verify root depth moisture, check underleaf pests with a 10x lens, test soil pH, and seek local horticultural extension advice.",
        message_ta="புகைப்படத்தை மட்டுமே கொண்டு பூச்சிக்கொல்லிகளையோ உரங்களையோ பயன்படுத்த வேண்டாம். மண் ஈரப்பதம், வேர் நலம் மற்றும் இலைக்கு அடியில் உள்ள பூச்சிகளை ஆய்வு செய்து உறுதிப்படுத்தவும்.",
        is_tamil=is_tamil,
    )

    # Fetch available sections from SQLite
    db_sections = get_garden_sections()
    section_names = [s["section_name"] for s in db_sections] if db_sections else [
        "Section A (North Bed)", "Section B (South Bed)", "Section C (East Plot)", "Section D (West Plot)"
    ]

    tab_log, tab_history, tab_guide = st.tabs([
        "🔍 1. Log Symptoms & Analyze" if not is_tamil else "🔍 1. அறிகுறிகள் & பகுப்பாய்வு",
        "📋 2. Observation History & Confirmation" if not is_tamil else "📋 2. முந்தைய ஆய்வுகள் & உறுதிப்படுத்தல்",
        "🔬 3. Scientific Scouting Guide" if not is_tamil else "🔬 3. அறிவியல் கள ஆய்வு வழிகாட்டி",
    ])

    # -----------------------------------------------------------------------
    # TAB 1: Log Visible Symptoms & Run Diagnostic Hypotheses
    # -----------------------------------------------------------------------
    with tab_log:
        col_form, col_analysis = st.columns([1, 1])

        with col_form:
            st.markdown("### 📝 Record Visible Crop Signs (கள அறிகுறிகள்)")
            st.caption("Check only what you physically observe on the bushes today:")

            obs_date = st.date_input("Observation Date / தேதி:", value=date.today(), max_value=date.today(), key="ph_date")
            chosen_section_name = st.selectbox("Garden Section / பாத்தி:", options=section_names, key="ph_section")

            # Find section ID and latest soil pH if available
            chosen_section_id = None
            if db_sections:
                for s in db_sections:
                    if s["section_name"] == chosen_section_name:
                        chosen_section_id = s["id"]
                        break

            latest_soil = get_latest_soil_test_by_section(chosen_section_id)
            current_soil_ph = latest_soil["ph"] if latest_soil else None
            current_soil_drainage = latest_soil["drainage"] if latest_soil else None

            if current_soil_ph is not None:
                st.caption(f"ℹ️ Section Soil Context: pH = **{current_soil_ph:.1f}** | Drainage = **{current_soil_drainage}**")

            st.markdown("**1. Visible Physical Symptoms Checklist:**")
            selected_symptom_ids = []
            for sid, sdata in VISIBLE_SYMPTOMS_CATALOG.items():
                label = f"{sdata['name_ta']} ({sdata['name_en']})" if is_tamil else f"{sdata['name_en']} ({sdata['name_ta']})"
                if st.checkbox(label, key=f"chk_sym_{sid}"):
                    selected_symptom_ids.append(sid)

            col_p, col_s = st.columns(2)
            with col_p:
                affected_part = st.selectbox(
                    "Primary Affected Part:",
                    options=[
                        "New tender flush",
                        "Older lower leaves",
                        "Flower buds and cymes",
                        "Entire branch or whole bush",
                    ],
                    key="ph_part",
                )
            with col_s:
                severity = st.selectbox(
                    "Damage Severity:",
                    options=["Mild (<10% affected)", "Moderate (10-30% affected)", "Severe (>30% affected)"],
                    index=0,
                    key="ph_severity",
                )

            uploaded_photo = st.file_uploader(
                "Optional symptom photograph (Leaf, Bud, or Bush):",
                type=["jpg", "jpeg", "png", "webp"],
                key="ph_photo",
            )
            saved_photo_name = None
            if uploaded_photo:
                v_ok, v_msg, v_meta = validate_image_file(uploaded_photo)
                if v_ok:
                    st.image(Image.open(uploaded_photo), caption=f"Symptom photo: {uploaded_photo.name}", use_container_width=True)
                    saved_photo_name = uploaded_photo.name
                else:
                    st.error(f"❌ {v_msg}")

            notes = st.text_area(
                "Field Scout Notes / களக் குறிப்புகள்:",
                placeholder="e.g., Yellowing started 2 days after basin watering. 10x lens showed no red mites underleaf.",
                key="ph_notes",
            )

            save_btn = st.button("💾 Save Observation to Farm Records", use_container_width=True, type="primary")

        # Live Diagnostic Hypotheses Panel
        with col_analysis:
            st.markdown("### 🔬 Differential Diagnostic Hypotheses")
            st.caption("Hypotheses generated by multi-factor agronomic analysis:")

            if not selected_symptom_ids:
                st.info("👈 Check one or more visible symptoms on the left to see differential hypotheses and missing data audits.")
            else:
                analysis_result = analyze_plant_health_observations(
                    reported_symptom_ids=selected_symptom_ids,
                    affected_part=affected_part,
                    severity=severity,
                    has_image=bool(uploaded_photo),
                    soil_ph=current_soil_ph,
                    soil_drainage=current_soil_drainage,
                )

                st.warning(analysis_result["safety_disclaimer"])

                # Expert Referral Alert if triggered
                referral = analysis_result.get("expert_referral")
                if referral:
                    st.error(
                        f"""
                        🚨 **EXPERT REFERRAL CONDITION TRIGGERED ({referral['urgency']})**
                        **Reasons:** {', '.join(referral['reasons'])}
                        """
                    )
                    with st.expander("🏛️ View Authority Referral Contacts & Sample Protocol", expanded=True):
                        st.markdown("**Recommended Agricultural Authorities:**")
                        for auth in referral["recommended_authorities"]:
                            st.write(f"• **{auth['entity']}** — *{auth['role']}* ({auth['contact_info']})")
                        st.markdown("**Sample Collection Protocol:**")
                        st.text(referral["sample_collection_protocol"])

                # Ranked Hypotheses
                st.markdown(f"#### Top Differential Hypotheses ({len(analysis_result['hypotheses'])} identified):")
                for idx, hyp in enumerate(analysis_result["hypotheses"][:3], 1):
                    with st.expander(f"{idx}. {hyp['cause_name_en']} — {hyp['cause_name_ta']} ({hyp['category']})", expanded=(idx==1)):
                        st.caption(f"Confidence: {hyp['confidence_label']}")
                        st.markdown("**Supporting Indicators:**")
                        for ind in hyp["supporting_indicators"]:
                            st.write(f"✓ {ind}")
                        if hyp["contradicting_indicators"]:
                            st.markdown("**Contradicting Indicators:**")
                            for cind in hyp["contradicting_indicators"]:
                                st.write(f"⚠️ {cind}")
                        st.markdown("**Required Field Verification Steps:**")
                        for vstep in hyp["verification_steps"]:
                            st.info(f"🔎 {vstep}")
                        st.caption(f"Source: {hyp['evidence_source']}")

                # Missing Information Audit
                st.markdown("#### ❓ Missing Information Needed to Confirm:")
                for minfo in analysis_result["missing_information"]:
                    st.write(f"• {minfo}")

        # Handle Save
        if save_btn:
            if not selected_symptom_ids:
                st.error("Please select at least one visible symptom before saving.")
            else:
                sym_names = [VISIBLE_SYMPTOMS_CATALOG[sid]["name_en"] for sid in selected_symptom_ids if sid in VISIBLE_SYMPTOMS_CATALOG]
                top_hyp_names = [h["cause_name_en"] for h in analysis_result["hypotheses"][:2]]
                
                # Save to database
                obs_id = add_plant_observation(
                    observation_date=str(obs_date),
                    visible_symptoms=", ".join(sym_names),
                    affected_part=affected_part,
                    severity=severity,
                    section_id=chosen_section_id,
                    suspected_causes=", ".join(top_hyp_names),
                    confirmed_diagnosis="Unconfirmed (Hypotheses Under Field Verification)",
                    status="Under Investigation",
                    image_filename=saved_photo_name,
                    notes=notes or "Field symptom observation recorded.",
                )

                # Keep session state synchronized
                add_health_record({
                    "id": obs_id,
                    "date": str(obs_date),
                    "section": chosen_section_name,
                    "visible_symptoms": sym_names,
                    "affected_part": affected_part,
                    "severity": severity,
                    "suspected_causes": top_hyp_names,
                    "confirmed_diagnosis": "Unconfirmed (Field Verification Pending)",
                    "status": "Under Investigation",
                    "notes": notes,
                })
                st.success(f"✅ Observation saved with ID #{obs_id}! Status: Under Investigation.")
                st.rerun()

    # -----------------------------------------------------------------------
    # TAB 2: Observation History & Confirmation Tracker
    # -----------------------------------------------------------------------
    with tab_history:
        st.markdown("### 📋 Stored Plant Observations (பதிவு செய்யப்பட்ட ஆய்வுகள்)")
        st.caption("Track field investigations from initial symptom notice to confirmed diagnosis:")

        db_obs = get_plant_observations()
        if not db_obs:
            st.info("No plant health observations recorded in the database yet.")
        else:
            disp_list = []
            for o in db_obs:
                disp_list.append({
                    "ID": o["id"],
                    "Date": o["observation_date"],
                    "Section": o.get("section_name") or "Unassigned",
                    "Symptoms": o["visible_symptoms"],
                    "Part": o["affected_part"],
                    "Severity": o["severity"],
                    "Suspected Causes": o["suspected_causes"],
                    "Confirmed Diagnosis": o["confirmed_diagnosis"],
                    "Status": o["status"],
                })
            st.dataframe(pd.DataFrame(disp_list), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### 🔬 Update Confirmed Diagnosis (ஆய்வு முடிவை உறுதிப்படுத்துக)")
            st.caption("Once you have inspected with a hand lens, checked roots, or consulted an extension officer:")

            with st.form("update_diagnosis_form"):
                col_sel_id, col_conf_diag = st.columns([1, 2])
                with col_sel_id:
                    selected_obs_id = st.selectbox("Select Observation ID:", options=[o["id"] for o in db_obs])
                with col_conf_diag:
                    confirmed_diag = st.selectbox(
                        "Confirmed Diagnosis / உறுதிப்படுத்தப்பட்ட காரணம்:",
                        options=[
                            "Confirmed: Nitrogen Deficiency (older leaves chlorosis)",
                            "Confirmed: Iron Chlorosis (high soil pH / calcareous)",
                            "Confirmed: Poor Drainage / Root Suffocation",
                            "Confirmed: Jasmine Bud Worm (Hendecasis duplifascialis)",
                            "Confirmed: Blossom Midge (Contarinia maculipennis)",
                            "Confirmed: Red Spider Mites (Tetranychus urticae)",
                            "Confirmed: Thrips (Thrips orientalis)",
                            "Confirmed: Collar Rot / Root Rot (Sclerotium / Fusarium)",
                            "Inconclusive / Environmental Heat Stress",
                        ],
                    )

                col_st, col_nt = st.columns([1, 2])
                with col_st:
                    new_status = st.selectbox("Investigation Status:", ["Resolved", "Monitoring", "Referred to Expert"])
                with col_nt:
                    confirm_notes = st.text_input("Confirmation Notes:", placeholder="e.g. Sliced fallen buds; yellow midge larvae found.")

                submit_update = st.form_submit_button("✅ Update Confirmed Diagnosis", use_container_width=True)

            if submit_update:
                update_plant_observation_diagnosis(
                    observation_id=selected_obs_id,
                    confirmed_diagnosis=confirmed_diag,
                    status=new_status,
                    notes=confirm_notes,
                )
                st.success(f"✓ Observation #{selected_obs_id} updated to '{confirmed_diag}' ({new_status})!")
                st.rerun()

    # -----------------------------------------------------------------------
    # TAB 3: Scientific Scouting Guide
    # -----------------------------------------------------------------------
    with tab_guide:
        st.markdown("### 🔬 TNAU & ICAR Jasminum sambac Scouting Protocol")
        st.caption("Field inspection methodology to separate looks-alike symptoms:")

        for diag_key, diag_info in DIFFERENTIAL_DIAGNOSES.items():
            with st.expander(f"📌 {diag_info['cause_name_en']} — {diag_info['cause_name_ta']} ({diag_info['category']})", expanded=False):
                st.markdown("**Typical Visible Signs:**")
                for s in diag_info["supporting_indicators"]:
                    st.write(f"• {s}")
                st.markdown("**How to Differentiate from Look-Alikes:**")
                for cs in diag_info["contradicting_indicators"]:
                    st.write(f"• {cs}")
                st.markdown("**Physical Verification Procedure:**")
                for v in diag_info["verification_steps"]:
                    st.info(f"🔎 {v}")
                st.caption(f"Evidence Source: {diag_info['evidence_source']}")
