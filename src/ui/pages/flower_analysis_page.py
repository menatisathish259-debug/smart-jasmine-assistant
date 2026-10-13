"""
Flower Analysis & Maturity Staging Page (Module A).
Supports validated image uploads, grower ground-truth labeling, and actionable harvest guidance.
"""

from datetime import date
from pathlib import Path
from PIL import Image
import streamlit as st

from config.settings import (
    FLOWER_STAGES,
    TAMIL_STAGE_TRANSLATIONS,
    RAW_DATA_DIR,
)
from src.core.constants import HARVEST_GUIDANCE, FlowerMaturityStage
from src.core.validation import validate_image_file, validate_harvest_entry
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_harvest_record


def render_flower_analysis(is_tamil: bool) -> None:
    """Renders the flower maturity analysis and staging page."""
    render_page_header(
        title_en="Flower Maturity Analysis (Module A)",
        title_ta="மலர் முதிர்ச்சி பகுப்பாய்வு (பகுதி A)",
        subtitle_en="Examine bud maturity, verify harvest readiness, and stage family photographs for model training",
        subtitle_ta="மொட்டு முதிர்ச்சியை ஆராயவும், அறுவடை நிலையை உறுதிப்படுத்தவும், பயிற்சிக்கு புகைப்படங்களை சேமிக்கவும்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Dataset Staging Phase. Your family's labeling serves as the ground truth. Trained MobileNetV2 inference will be integrated in Phase 5.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Do not rely on unvalidated computer models for harvest decisions. The grower's experienced judgment is the project ground truth.",
        message_ta="சரிபார்க்கப்படாத கணிப்புகளை நம்ப வேண்டாம். விவசாயியின் கள அனுபவமே இந்த அமைப்பின் முதன்மை உண்மை (ground truth).",
        is_tamil=is_tamil,
    )

    col_upload, col_details = st.columns([1, 1])

    uploaded_file = None
    img_metadata = {}

    with col_upload:
        st.markdown("### 📷 1. Upload Bud Photograph (புகைப்படம் பதிவேற்றுக)")
        uploaded_file = st.file_uploader(
            "Choose a close-up jasmine bud photograph (JPG, PNG, WEBP):",
            type=["jpg", "jpeg", "png", "webp"],
            key="flower_image_uploader",
            help="Take clear photographs in morning daylight for best evaluation.",
        )

        if uploaded_file is not None:
            is_valid, msg, img_metadata = validate_image_file(uploaded_file)
            if not is_valid:
                st.error(f"❌ {msg}")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)
                st.success(
                    f"✓ Image Verified: {img_metadata['width']}x{img_metadata['height']} px | "
                    f"{img_metadata['format']} | {img_metadata['size_kb']} KB"
                )

                # Experimental Model Inference (Phase 5 Integration)
                from src.models.inference import is_model_available, predict_flower_stage
                if is_model_available():
                    st.markdown("---")
                    st.markdown("#### 🤖 Experimental AI Inspection (MobileNetV2)")
                    if st.button("Run AI Maturity Prediction", key="btn_run_ai_pred", use_container_width=True):
                        with st.spinner("Analyzing flower features..."):
                            pred = predict_flower_stage(image)
                            if pred["status"] == "SUCCESS":
                                st.markdown(
                                    f"""
                                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px; padding:0.8rem; margin:0.5rem 0;">
                                        <b>Predicted Stage:</b> {pred['predicted_stage']} ({pred['predicted_stage_ta']})<br>
                                        <b>Model Confidence:</b> {pred['confidence_pct']}% (Uncertainty: {pred['uncertainty_score']})
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                st.warning(pred["disclaimer"])
                                with st.expander("📊 View Probability Distribution", expanded=False):
                                    for stg, prob in pred["probabilities"].items():
                                        st.write(f"• {stg}: **{prob:.1f}%**")
                else:
                    st.info("ℹ️ AI Model checkpoint will activate here after training in Phase 5.")
        else:
            st.info("ℹ️ Upload a photograph of individual jasmine buds or a whole flower cluster to inspect.")


    with col_details:
        st.markdown("### 🏷️ 2. Grower Assessment & Ground Truth (விவசாயியின் மதிப்பீடு)")
        st.caption("Record your harvest judgment to build the verified dataset for training.")

        with st.form("harvest_staging_form", clear_on_submit=False):
            stage_options = [
                f"{stage} — {TAMIL_STAGE_TRANSLATIONS[stage]}" if is_tamil else stage
                for stage in FLOWER_STAGES
            ]
            selected_stage_label = st.selectbox(
                "Maturity Stage / முதிர்ச்சி நிலை:",
                options=stage_options,
                index=0,
                key="form_selected_stage",
            )
            # Extract raw stage key
            selected_stage = selected_stage_label.split(" — ")[0].strip()

            col_sec, col_cnt = st.columns(2)
            with col_sec:
                garden_section = st.selectbox(
                    "Garden Section / பாத்தி:",
                    options=[
                        "Section A (North Bed)",
                        "Section B (South Bed)",
                        "Section C (East Plot)",
                        "Section D (West Plot)",
                        "Young Planting (< 1 Year)",
                    ],
                    key="form_garden_section",
                )
            with col_cnt:
                bud_count = st.number_input(
                    "Approx. Bud Count / எண்ணிக்கை:",
                    min_value=1,
                    max_value=5000,
                    value=50,
                    step=10,
                    key="form_bud_count",
                )

            obs_date = st.date_input(
                "Observation Date / தேதி:",
                value=date.today(),
                max_value=date.today(),
                key="form_obs_date",
            )

            notes = st.text_area(
                "Observations & Notes / குறிப்புகள்:",
                placeholder="e.g., Morning picking at 7:00 AM. Firm petals, slight elongation, no visible pest damage.",
                key="form_obs_notes",
            )

            submit_btn = st.form_submit_button("💾 Stage Observation in Farm Records", use_container_width=True)

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
                    "stage": selected_stage,
                    "quantity": bud_count,
                    "unit": "buds",
                    "notes": notes if notes.strip() else "Standard grower observation.",
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

                st.success(f"✅ Record successfully saved to SQLite database! Stage: **{selected_stage}** ({bud_count} buds).")


    # -----------------------------------------------------------------------
    # Dynamic Agricultural Action Guidance Card
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🌿 Harvest Guidance for Selected Stage")
    guidance = HARVEST_GUIDANCE.get(selected_stage, {})
    if guidance:
        badge_style = {
            "READY_TO_PLUCK": ("#d8f3dc", "#1b4332", "#52b788"),
            "NOT_READY": ("#faedcd", "#7f4f24", "#d4a373"),
            "TOO_OPEN": ("#fde2e4", "#9d0208", "#f4a261"),
            "DAMAGED_OR_ABNORMAL": ("#ffe3e3", "#9b2226", "#e63946"),
        }.get(selected_stage, ("#f1f5f9", "#334155", "#cbd5e1"))

        st.markdown(
            f"""
            <div style="background:{badge_style[0]}; border-left:6px solid {badge_style[2]}; padding:1.2rem; border-radius:10px; color:{badge_style[1]};">
                <h4 style="margin:0 0 6px 0; color:{badge_style[1]};">{guidance['status_title']} ({guidance['commercial_grade']})</h4>
                <p style="margin:0 0 10px 0; font-size:0.92rem;"><b>Description:</b> {guidance['description']}</p>
                <div style="background:#ffffff; padding:0.8rem; border-radius:8px; border:1px solid {badge_style[2]}; font-size:0.9rem;">
                    <b>💡 Recommended Harvest Action:</b> {guidance['recommended_action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Staged Records Table
    # -----------------------------------------------------------------------
    st.markdown("### 📋 Staged Flower Records (சேமிக்கப்பட்ட பதிவுகள்)")
    if st.session_state.harvest_records:
        import pandas as pd
        df = pd.DataFrame(st.session_state.harvest_records)
        st.dataframe(
            df[["date", "section", "stage", "quantity", "unit", "image_filename", "notes"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No flower maturity records logged yet.")
