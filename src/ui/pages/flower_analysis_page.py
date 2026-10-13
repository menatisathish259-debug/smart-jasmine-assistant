"""
Flower Analysis & Maturity Staging Page (Module A).
Supports validated image uploads, grower ground-truth labeling, and actionable harvest guidance.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

from datetime import date
from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

from config.settings import (
    FLOWER_STAGES,
    RAW_DATA_DIR,
)
from src.core.constants import HARVEST_GUIDANCE
from src.core.validation import validate_image_file, validate_harvest_entry
from src.core.i18n import (
    normalize_lang,
    get_stage_name,
    get_stage_key_from_name,
    get_section_options,
    t,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_harvest_record


def render_flower_analysis(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the flower maturity analysis and staging page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Flower Maturity Analysis (Module A)",
        title_ta="மலர் முதிர்ச்சி பகுப்பாய்வு (பகுதி A)",
        title_te="పూల పరిపక్వత విశ్లేషణ (విభాగం A)",
        subtitle_en="Examine bud maturity, verify harvest readiness, and stage family photographs for model training",
        subtitle_ta="மொட்டு முதிர்ச்சியை ஆராயவும், அறுவடை நிலையை உறுதிப்படுத்தவும், புகைப்படங்களை சேமிக்கவும்",
        subtitle_te="మొగ్గల పరిపక్వతను పరిశీలించి, కోత సంసిద్ధతను నిర్ధారించి, ఫోటోలను భద్రపరచండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Dataset Staging Phase. Your family's labeling serves as the ground truth. Trained MobileNetV2 inference will be integrated in Phase 5.",
        desc_ta="தரவு சேகரிப்பு நிலை. விவசாயியின் மதிப்பீடே முதன்மை உண்மை.",
        desc_te="డేటా సేకరణ దశ. రైతు క్షేత్ర అనుభవమే ప్రామాణికం.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="Do not rely on unvalidated computer models for harvest decisions. The grower's experienced judgment is the project ground truth.",
        message_ta="சரிபார்க்கப்படாத மாதிரிகளை நம்ப வேண்டாம். விவசாயியின் கள அனுபவமே இந்த அமைப்பின் முதன்மை உண்மை.",
        message_te="ధృవీకరించని కంప్యూటర్ అంచనాలపై ఆధారపడవద్దు. రైతు క్షేత్ర అనుభవమే తుది ప్రామాణికం.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    col_upload, col_details = st.columns([1, 1])

    uploaded_file = None
    img_metadata = {}

    with col_upload:
        st.markdown(f"### 📷 1. {t('upload_bud_photo', current_lang)}")
        uploaded_file = st.file_uploader(
            t("upload_bud_prompt", current_lang),
            type=["jpg", "jpeg", "png", "webp"],
            key="flower_image_uploader",
            help=t("upload_help", current_lang),
        )

        if uploaded_file is not None:
            is_valid, msg, img_metadata = validate_image_file(uploaded_file)
            if not is_valid:
                st.error(f"❌ {msg}")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"{uploaded_file.name}", use_container_width=True)
                st.success(
                    f"✓ {img_metadata['width']}x{img_metadata['height']} px | "
                    f"{img_metadata['format']} | {img_metadata['size_kb']} KB"
                )

                # Experimental Model Inference (Phase 5 Integration)
                from src.models.inference import is_model_available, predict_flower_stage
                if is_model_available():
                    st.markdown("---")
                    st.markdown(f"#### 🤖 {t('ai_prediction_box', current_lang)}")
                    if st.button(t("btn_run_ai", current_lang), key="btn_run_ai_pred", use_container_width=True):
                        with st.spinner("..."):
                            pred = predict_flower_stage(image)
                            if pred["status"] == "SUCCESS":
                                localized_pred_stage = get_stage_name(pred["predicted_stage"], current_lang)
                                st.markdown(
                                    f"""
                                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px; padding:0.8rem; margin:0.5rem 0;">
                                        <b>{t('predicted_stage', current_lang)}:</b> {localized_pred_stage}<br>
                                        <b>{t('confidence', current_lang)}:</b> {pred['confidence_pct']}% ({t('uncertainty', current_lang)}: {pred['uncertainty_score']})
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                st.warning(pred["disclaimer"])
                                with st.expander(f"📊 {t('prob_dist', current_lang)}", expanded=False):
                                    for stg, prob in pred["probabilities"].items():
                                        st.write(f"• {get_stage_name(stg, current_lang)}: **{prob:.1f}%**")
                else:
                    st.info("ℹ️ AI Model checkpoint will activate here after training in Phase 5.")
        else:
            if current_lang == "ta":
                st.info("ℹ️ மொட்டு புகைப்படத்தை பதிவேற்றவும்.")
            elif current_lang == "te":
                st.info("ℹ️ మొగ్గ ఫోటోను అప్‌లోడ్ చేయండి.")
            else:
                st.info("ℹ️ Upload a photograph of individual jasmine buds or a whole flower cluster to inspect.")

    with col_details:
        st.markdown(f"### 🏷️ 2. {t('grower_assessment', current_lang)}")
        st.caption(t("grower_caption", current_lang))

        with st.form("harvest_staging_form", clear_on_submit=False):
            stage_display_options = [get_stage_name(s, current_lang) for s in FLOWER_STAGES]
            selected_display_label = st.selectbox(
                t("maturity_stage", current_lang),
                options=stage_display_options,
                index=0,
                key="form_selected_stage",
            )
            selected_stage = get_stage_key_from_name(selected_display_label, current_lang)

            section_options = get_section_options(current_lang)
            col_sec, col_cnt = st.columns(2)
            with col_sec:
                garden_section = st.selectbox(
                    t("garden_section", current_lang),
                    options=section_options,
                    key="form_garden_section",
                )
            with col_cnt:
                bud_count_label = (
                    "எண்ணிக்கை:" if current_lang == "ta"
                    else ("మొగ్గల సంఖ్య:" if current_lang == "te"
                    else "Approx. Bud Count:")
                )
                bud_count = st.number_input(
                    bud_count_label,
                    min_value=1,
                    max_value=5000,
                    value=50,
                    step=10,
                    key="form_bud_count",
                )

            obs_date = st.date_input(
                t("obs_date", current_lang),
                value=date.today(),
                max_value=date.today(),
                key="form_obs_date",
            )

            notes_label = (
                "குறிப்புகள்:" if current_lang == "ta"
                else ("గమనికలు:" if current_lang == "te"
                else "Observations & Notes:")
            )
            notes = st.text_area(
                notes_label,
                placeholder=t("notes_placeholder", current_lang),
                key="form_obs_notes",
            )

            submit_label = (
                "💾 பதிவைச் சேமிக்கவும்" if current_lang == "ta"
                else ("💾 వివరాలను భద్రపరచు" if current_lang == "te"
                else "💾 Save Harvest Observation")
            )
            submit_btn = st.form_submit_button(submit_label, use_container_width=True)

        if submit_btn:
            is_valid_entry, entry_msg = validate_harvest_entry(selected_stage, bud_count, obs_date)
            if not is_valid_entry:
                st.error(f"❌ {entry_msg}")
            else:
                saved_filename = ""
                if uploaded_file is not None and "filename" in img_metadata:
                    # Save image to data/raw for Phase 4 dataset preparation
                    saved_path = RAW_DATA_DIR / f"{obs_date}_{selected_stage}_{uploaded_file.name}"
                    try:
                        with open(saved_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        saved_filename = saved_path.name
                    except Exception as e:
                        st.warning(f"Note: Could not write image to raw folder: {e}")

                record = {
                    "date": str(obs_date),
                    "section": garden_section,
                    "stage": get_stage_name(selected_stage, current_lang),
                    "quantity": bud_count,
                    "unit": "buds",
                    "notes": notes if notes.strip() else "",
                    "image_filename": saved_filename or "No image attached",
                }
                add_harvest_record(record)

                if saved_filename:
                    from src.database import repository
                    try:
                        repository.add_image_label(
                            filename=saved_filename,
                            filepath=str(saved_path),
                            label_stage=selected_stage,
                            image_type="single_bud",
                            width=img_metadata.get("width"),
                            height=img_metadata.get("height"),
                            format=img_metadata.get("format"),
                            filesize_kb=img_metadata.get("size_kb"),
                            notes=notes,
                        )
                    except Exception as ex:
                        st.caption(f"Image cataloged: {saved_filename}")

                success_msg = (
                    f"✅ பதிவு வெற்றிகரமாக சேமிக்கப்பட்டது! நிலை: **{get_stage_name(selected_stage, current_lang)}** ({bud_count})."
                    if current_lang == "ta"
                    else (
                        f"✅ వివరాలు విజయవంతంగా భద్రపరచబడ్డాయి! దశ: **{get_stage_name(selected_stage, current_lang)}** ({bud_count})."
                        if current_lang == "te"
                        else f"✅ Record successfully saved! Stage: **{get_stage_name(selected_stage, current_lang)}** ({bud_count} buds)."
                    )
                )
                st.success(success_msg)

    # -----------------------------------------------------------------------
    # Dynamic Agricultural Action Guidance Card
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"### 🌿 {t('harvest_guidance_title', current_lang)}")
    guidance = HARVEST_GUIDANCE.get(selected_stage, {})
    if guidance:
        badge_style = {
            "READY_TO_PLUCK": ("#d8f3dc", "#1b4332", "#52b788"),
            "NOT_READY": ("#faedcd", "#7f4f24", "#d4a373"),
            "TOO_OPEN": ("#fde2e4", "#9d0208", "#f4a261"),
            "DAMAGED_OR_ABNORMAL": ("#ffe3e3", "#9b2226", "#e63946"),
        }.get(selected_stage, ("#f1f5f9", "#334155", "#cbd5e1"))

        if current_lang == "ta":
            rec_title = f"{get_stage_name(selected_stage, 'ta')} (அறுவடை தரம்)"
            rec_action_lbl = "பரிந்துரைக்கப்பட்ட அறுவடை நடவடிக்கை:"
        elif current_lang == "te":
            rec_title = f"{get_stage_name(selected_stage, 'te')} (కోత నాణ్యత)"
            rec_action_lbl = "సిఫార్సు చేయబడిన కోత చర్య:"
        else:
            rec_title = f"{guidance['status_title']} ({guidance['commercial_grade']})"
            rec_action_lbl = "Recommended Harvest Action:"

        st.markdown(
            f"""
            <div style="background:{badge_style[0]}; border-left:6px solid {badge_style[2]}; padding:1.2rem; border-radius:10px; color:{badge_style[1]};">
                <h4 style="margin:0 0 6px 0; color:{badge_style[1]};">{rec_title}</h4>
                <p style="margin:0 0 10px 0; font-size:0.92rem;">{guidance['description']}</p>
                <div style="background:#ffffff; padding:0.8rem; border-radius:8px; border:1px solid {badge_style[2]}; font-size:0.9rem;">
                    <b>💡 {rec_action_lbl}</b> {guidance['recommended_action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Staged Records Table
    # -----------------------------------------------------------------------
    table_header = (
        "சேமிக்கப்பட்ட பதிவுகள்" if current_lang == "ta"
        else ("నమోదైన వివరాలు" if current_lang == "te"
        else "Staged Flower Records")
    )
    st.markdown(f"### 📋 {table_header}")
    if st.session_state.harvest_records:
        df = pd.DataFrame(st.session_state.harvest_records)
        st.dataframe(
            df[["date", "section", "stage", "quantity", "unit", "image_filename", "notes"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        empty_lbl = (
            "பதிவுகள் எதுவும் இல்லை." if current_lang == "ta"
            else ("ఇంకా వివరాలు నమోదు కాలేదు." if current_lang == "te"
            else "No flower maturity records logged yet.")
        )
        st.info(empty_lbl)
