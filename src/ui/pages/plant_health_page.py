"""
Plant Health and Damage Analysis Page (Module C).
Structured symptom logging strictly separating visible observations from confirmed causes.
Provides differential diagnostic hypotheses, missing information audits, and expert referral conditions.
Displays purely in English, Tamil, or Telugu based on selected language.
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
from src.core.i18n import (
    normalize_lang,
    get_section_options,
    t,
)
from src.database.repository import (
    add_plant_observation,
    get_plant_observations,
    update_plant_observation_diagnosis,
    get_latest_soil_test_by_section,
    get_garden_sections,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_health_record


def render_plant_health(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the plant health and symptom analysis page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Plant Health & Damage Observations (Module C)",
        title_ta="பயிர் நலம் மற்றும் சேதக் கண்காணிப்பு (பகுதி C)",
        title_te="మొక్కల ఆరోగ్యం మరియు నష్టాల పరిశీలన (విభాగం C)",
        subtitle_en="Record visible crop abnormalities while strictly separating physical observations from confirmed diagnoses",
        subtitle_ta="தென்படும் அறிகுறிகளைப் பதிவுசெய்து, சந்தேகிக்கப்படும் காரணங்களை முறைப்படி ஆராய்க",
        subtitle_te="కనిపించే లక్షణాలను నమోదు చేసి, అనుమానిత కారణాలను పద్ధతి ప్రకారం విశ్లేషించండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Evidence-Based Diagnostic Engine Active. Separates visible symptoms from inferred causes.",
        desc_ta="ஆதார அடிப்படையிலான பகுப்பாய்வு இயங்குகிறது. வெளிப்படையான அறிகுறிகள் மற்றும் உத்தேச காரணங்கள் தனித்தனியாக கையாளப்படுகின்றன.",
        desc_te="ఆధారాల ఆధారిత విశ్లేషణ సిద్ధంగా ఉంది. కనిపించే లక్షణాలు మరియు అనుమానిత కారణాలు వేరుగా విశ్లేషించబడతాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="NEVER prescribe chemical pesticides or fertilizer rates based solely on photographs. Always verify root depth moisture, check underleaf pests with a 10x lens, test soil pH, and seek local horticultural extension advice.",
        message_ta="புகைப்படத்தை மட்டுமே கொண்டு பூச்சிக்கொல்லிகளையோ உரங்களையோ பயன்படுத்த வேண்டாம். மண் ஈரப்பதம், வேர் நலம் மற்றும் இலைக்கு அடியில் உள்ள பூச்சிகளை ஆய்வு செய்து உறுதிப்படுத்தவும்.",
        message_te="ఫోటోలను మాత్రమే చూసి పురుగుమందులు లేదా ఎరువుల మోతాదులను నిర్ణయించవద్దు. నేల తేమ, వేర్లు మరియు ఆకుల క్రింది పురుగులను పరిశీలించి నిర్ధారించండి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    # Fetch available sections from SQLite
    db_sections = get_garden_sections()
    section_options = get_section_options(current_lang)

    # Tab titles in pure language
    if current_lang == "ta":
        tabs_labels = [
            "🔍 1. அறிகுறிகள் பதிவு மற்றும் பகுப்பாய்வு",
            "📋 2. முந்தைய ஆய்வுகள் மற்றும் உறுதிப்படுத்தல்",
            "🔬 3. அறிவியல் கள ஆய்வு வழிகாட்டி",
        ]
    elif current_lang == "te":
        tabs_labels = [
            "🔍 1. లక్షణాల నమోదు మరియు విశ్లేషణ",
            "📋 2. గత పరిశీలనలు మరియు నిర్ధారణ",
            "🔬 3. శాస్త్రీయ క్షేత్ర తనిఖీ సూచిక",
        ]
    else:
        tabs_labels = [
            "🔍 1. Log Symptoms & Analyze",
            "📋 2. Observation History & Confirmation",
            "🔬 3. Scientific Scouting Guide",
        ]

    tab_log, tab_history, tab_guide = st.tabs(tabs_labels)

    # -----------------------------------------------------------------------
    # TAB 1: Log Visible Symptoms & Run Diagnostic Hypotheses
    # -----------------------------------------------------------------------
    with tab_log:
        col_form, col_analysis = st.columns([1, 1])

        with col_form:
            card_head = (
                "கள அறிகுறிகள் பதிவு" if current_lang == "ta"
                else ("కనిపించే లక్షణాల నమోదు" if current_lang == "te"
                else "Record Visible Crop Signs")
            )
            st.markdown(f"### 📝 {card_head}")

            obs_date = st.date_input(t("obs_date", current_lang), value=date.today(), max_value=date.today(), key="ph_date")
            chosen_section_name = st.selectbox(t("garden_section", current_lang), options=section_options, key="ph_section")

            # Section ID
            chosen_section_id = None
            if db_sections and len(db_sections) > 0:
                chosen_section_id = db_sections[0]["id"]

            latest_soil = get_latest_soil_test_by_section(chosen_section_id)
            current_soil_ph = latest_soil["ph"] if latest_soil else None
            current_soil_drainage = latest_soil["drainage"] if latest_soil else None

            st.markdown(f"**{t('visible_symptoms_header', current_lang)}:**")
            selected_symptom_ids = []
            for sid, sdata in VISIBLE_SYMPTOMS_CATALOG.items():
                if current_lang == "ta":
                    sym_label = sdata["name_ta"]
                elif current_lang == "te":
                    sym_label = sdata.get("name_te", sdata["name_en"])
                else:
                    sym_label = sdata["name_en"]

                if st.checkbox(sym_label, key=f"chk_sym_{sid}"):
                    selected_symptom_ids.append(sid)

            col_p, col_s = st.columns(2)
            with col_p:
                if current_lang == "ta":
                    part_options = ["புதிய இளந்தளிர்கள்", "முதிர்ந்த கீழ் இலைகள்", "மலர் மொட்டுகள்", "முழு கிளை அல்லது முழு செடி"]
                elif current_lang == "te":
                    part_options = ["కొత్త లేత చిగుళ్లు", "క్రింది ముదిరిన ఆకులు", "పూల మొగ్గలు", "మొత్తం కొమ్మ లేదా మొక్క"]
                else:
                    part_options = ["New tender flush", "Older lower leaves", "Flower buds and cymes", "Entire branch or whole bush"]

                affected_part = st.selectbox(
                    t("affected_part", current_lang),
                    options=part_options,
                    key="ph_part",
                )
            with col_s:
                if current_lang == "ta":
                    sev_options = ["குறைவான சேதம் (10% கீழ்)", "மிதமான சேதம் (10-30%)", "தீவிர சேதம் (30% மேல்)"]
                elif current_lang == "te":
                    sev_options = ["స్వల్ప నష్టం (10% లోపు)", "మధ్యస్థ నష్టం (10-30%)", "తీవ్ర నష్టం (30% పైగా)"]
                else:
                    sev_options = ["Mild (<10% affected)", "Moderate (10-30% affected)", "Severe (>30% affected)"]

                severity = st.selectbox(
                    t("damage_severity", current_lang),
                    options=sev_options,
                    index=0,
                    key="ph_severity",
                )

            photo_label = (
                "அறிகுறி புகைப்படம் (விரும்பினால்):" if current_lang == "ta"
                else ("లక్షణం ఫోటో (ఐచ్ఛికం):" if current_lang == "te"
                else "Optional symptom photograph:")
            )
            uploaded_photo = st.file_uploader(photo_label, type=["jpg", "jpeg", "png", "webp"], key="ph_photo")
            saved_photo_name = None
            if uploaded_photo:
                v_ok, v_msg, v_meta = validate_image_file(uploaded_photo)
                if v_ok:
                    st.image(Image.open(uploaded_photo), caption=uploaded_photo.name, use_container_width=True)
                    saved_photo_name = uploaded_photo.name
                else:
                    st.error(f"❌ {v_msg}")

            notes_label = (
                "களக் குறிப்புகள்:" if current_lang == "ta"
                else ("క్షేత్ర గమనికలు:" if current_lang == "te"
                else "Field Scout Notes:")
            )
            notes = st.text_area(notes_label, placeholder=t("notes_placeholder", current_lang), key="ph_notes")

            save_label = (
                "💾 ஆய்வைச் சேமிக்கவும்" if current_lang == "ta"
                else ("💾 పరిశీలనను భద్రపరచు" if current_lang == "te"
                else "💾 Save Observation to Farm Records")
            )
            save_btn = st.button(save_label, use_container_width=True, type="primary")

        # Live Diagnostic Hypotheses Panel
        with col_analysis:
            st.markdown(f"### 🔬 {t('diagnostic_hypotheses', current_lang)}")

            if not selected_symptom_ids:
                empty_analysis = (
                    "👈 காரணங்களை ஆராய இடதுபுறத்தில் உள்ள அறிகுறிகளைத் தேர்ந்தெடுக்கவும்." if current_lang == "ta"
                    else ("👈 కారణాలను విశ్లేషించడానికి ఎడమవైపు లక్షణాలను ఎంచుకోండి." if current_lang == "te"
                    else "👈 Check one or more visible symptoms on the left to see differential hypotheses and missing data audits.")
                )
                st.info(empty_analysis)
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
                    ref_title = (
                        "விவசாய வல்லுநர் பரிந்துரை தேவை" if current_lang == "ta"
                        else ("వ్యవసాయ నిపుణుల సంప్రదింపు అవసరం" if current_lang == "te"
                        else "EXPERT REFERRAL CONDITION TRIGGERED")
                    )
                    st.error(f"🚨 **{ref_title}** ({referral['urgency']})")
                    with st.expander("🏛️ View Authority Referral Contacts", expanded=True):
                        for auth in referral["recommended_authorities"]:
                            st.write(f"• **{auth['entity']}** — *{auth['role']}* ({auth['contact_info']})")

                # Ranked Hypotheses
                hypo_head = (
                    f"கண்டறியப்பட்ட காரணங்கள் ({len(analysis_result['hypotheses'])}):" if current_lang == "ta"
                    else (f"గుర్తించిన కారణాలు ({len(analysis_result['hypotheses'])}):" if current_lang == "te"
                    else f"Top Differential Hypotheses ({len(analysis_result['hypotheses'])} identified):")
                )
                st.markdown(f"#### {hypo_head}")
                for idx, hyp in enumerate(analysis_result["hypotheses"][:3], 1):
                    if current_lang == "ta":
                        cause_name = hyp["cause_name_ta"]
                    elif current_lang == "te":
                        cause_name = hyp.get("cause_name_te", hyp["cause_name_en"])
                    else:
                        cause_name = hyp["cause_name_en"]

                    with st.expander(f"{idx}. {cause_name}", expanded=(idx == 1)):
                        for ind in hyp["supporting_indicators"]:
                            st.write(f"✓ {ind}")
                        if hyp["contradicting_indicators"]:
                            for cind in hyp["contradicting_indicators"]:
                                st.write(f"⚠️ {cind}")
                        for vstep in hyp["verification_steps"]:
                            st.info(f"🔎 {vstep}")

                # Missing Information Audit
                st.markdown(f"#### ❓ {t('missing_info', current_lang)}:")
                for minfo in analysis_result["missing_information"]:
                    st.write(f"• {minfo}")

        # Handle Save
        if save_btn:
            if not selected_symptom_ids:
                st.error("Please select at least one visible symptom.")
            else:
                sym_names = [VISIBLE_SYMPTOMS_CATALOG[sid]["name_en"] for sid in selected_symptom_ids if sid in VISIBLE_SYMPTOMS_CATALOG]
                top_hyp_names = [h["cause_name_en"] for h in analysis_result["hypotheses"][:2]]
                
                obs_id = add_plant_observation(
                    observation_date=str(obs_date),
                    visible_symptoms=", ".join(sym_names),
                    affected_part=affected_part,
                    severity=severity,
                    section_id=chosen_section_id,
                    suspected_causes=", ".join(top_hyp_names),
                    confirmed_diagnosis="Unconfirmed",
                    status="Under Investigation",
                    image_filename=saved_photo_name,
                    notes=notes or "",
                )

                add_health_record({
                    "id": obs_id,
                    "date": str(obs_date),
                    "section": chosen_section_name,
                    "visible_symptoms": sym_names,
                    "affected_part": affected_part,
                    "severity": severity,
                    "suspected_causes": top_hyp_names,
                    "confirmed_diagnosis": "Unconfirmed",
                    "status": "Under Investigation",
                    "notes": notes,
                })
                st.success(f"✅ Observation saved with ID #{obs_id}!")
                st.rerun()

    # -----------------------------------------------------------------------
    # TAB 2: Observation History & Confirmation Tracker
    # -----------------------------------------------------------------------
    with tab_history:
        history_head = (
            "பதிவு செய்யப்பட்ட ஆய்வுகள்" if current_lang == "ta"
            else ("నమోదైన పరిశీలనలు" if current_lang == "te"
            else "Stored Plant Observations")
        )
        st.markdown(f"### 📋 {history_head}")

        db_obs = get_plant_observations()
        if not db_obs:
            empty_hist = (
                "பதிவுகள் எதுவும் இல்லை." if current_lang == "ta"
                else ("ఇంకా వివరాలు నమోదు కాలేదు." if current_lang == "te"
                else "No plant health observations recorded in the database yet.")
            )
            st.info(empty_hist)
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
            st.markdown(f"### 🔬 {t('confirm_diagnosis', current_lang)}")

            with st.form("update_diagnosis_form"):
                col_sel_id, col_conf_diag = st.columns([1, 2])
                with col_sel_id:
                    selected_obs_id = st.selectbox("ID:", options=[o["id"] for o in db_obs])
                with col_conf_diag:
                    if current_lang == "ta":
                        diag_options = [
                            "தழைச்சத்து குறைபாடு",
                            "இரும்பு / துத்தநாக சத்து குறைபாடு",
                            "வடிகால் அடைப்பு / வேர் மூச்சுத்திணறல்",
                            "மல்லி மொட்டுப்புழு தாக்குதல்",
                            "மல்லி மொட்டு ஈ தாக்குதல்",
                            "செம்பேன் தாக்குதல்",
                            "மல்லி இலைப்பேன்",
                            "வேரழுகல் / தண்டு அழுகல் நோய்",
                        ]
                    elif current_lang == "te":
                        diag_options = [
                            "నత్రజని లోపం",
                            "ఇనుము / జింక్ లోపం",
                            "నీరు నిల్వ ఉండటం / వేర్లకు ప్రాణవాయువు లోపం",
                            "మల్లె మొగ్గ తొలుచు పురుగు",
                            "మల్లె మొగ్గ ఈగ",
                            "ఎర్ర నల్లి",
                            "తామర పురుగులు",
                            "మొదలు కుళ్లు / వేరు కుళ్లు తెగులు",
                        ]
                    else:
                        diag_options = [
                            "Nitrogen Deficiency",
                            "Iron / Zinc Chlorosis",
                            "Poor Drainage / Root Suffocation",
                            "Jasmine Bud Worm",
                            "Blossom Midge",
                            "Red Spider Mites",
                            "Thrips",
                            "Collar Rot / Root Rot",
                        ]
                    confirmed_diag = st.selectbox("Diagnosis:", options=diag_options)

                col_st, col_nt = st.columns([1, 2])
                with col_st:
                    status_opts = (
                        ["முடிவடைந்தது", "கண்காணிப்பில்", "வல்லுநருக்கு பரிந்துரைக்கப்பட்டது"] if current_lang == "ta"
                        else (["పరిష్కరించబడింది", "పరిశీలనలో", "నిపుణులకు పంపబడింది"] if current_lang == "te"
                        else ["Resolved", "Monitoring", "Referred to Expert"])
                    )
                    new_status = st.selectbox("Status:", status_opts)
                with col_nt:
                    confirm_notes = st.text_input("Notes:", placeholder="")

                btn_up_lbl = (
                    "✅ முடிவை உறுதிப்படுத்து" if current_lang == "ta"
                    else ("✅ కారణాన్ని నిర్ధారించు" if current_lang == "te"
                    else "✅ Update Confirmed Diagnosis")
                )
                submit_update = st.form_submit_button(btn_up_lbl, use_container_width=True)

            if submit_update:
                update_plant_observation_diagnosis(
                    observation_id=selected_obs_id,
                    confirmed_diagnosis=confirmed_diag,
                    status=new_status,
                    notes=confirm_notes,
                )
                st.success(f"✓ Observation #{selected_obs_id} updated!")
                st.rerun()

    # -----------------------------------------------------------------------
    # TAB 3: Scientific Scouting Guide
    # -----------------------------------------------------------------------
    with tab_guide:
        guide_head = (
            "அறிவியல் கள ஆய்வு வழிகாட்டி" if current_lang == "ta"
            else ("శాస్త్రీయ క్షేత్ర తనిఖీ మార్గదర్శకాలు" if current_lang == "te"
            else "Scientific Scouting Protocol")
        )
        st.markdown(f"### 🔬 {guide_head}")

        for diag_key, diag_info in DIFFERENTIAL_DIAGNOSES.items():
            if current_lang == "ta":
                d_name = diag_info["cause_name_ta"]
            elif current_lang == "te":
                d_name = diag_info.get("cause_name_te", diag_info["cause_name_en"])
            else:
                d_name = diag_info["cause_name_en"]

            with st.expander(f"📌 {d_name}", expanded=False):
                for s in diag_info["supporting_indicators"]:
                    st.write(f"• {s}")
                for cs in diag_info["contradicting_indicators"]:
                    st.write(f"• {cs}")
                for v in diag_info["verification_steps"]:
                    st.info(f"🔎 {v}")
