"""
Dataset Organization & Image-Labeling Workflow Page (Phase 4).
Supports ground-truth labeling, duplicate auditing, split generation, and photography protocol.
"""

from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

from config.settings import FLOWER_STAGES, TAMIL_STAGE_TRANSLATIONS
from src.dataset.organizer import (
    get_dataset_summary,
    prepare_dataset_splits,
    PHOTOGRAPHY_GUIDELINES,
    SINGLE_BUDS_RAW,
    WHOLE_PLANT_RAW,
)
from src.dataset.duplicate_detector import find_duplicates
from src.dataset.labeling import label_single_bud_image, stage_whole_plant_image
from src.core.validation import validate_image_file
from src.ui.components import render_page_header, render_ai_status, render_safety_warning


def render_dataset_page(is_tamil: bool) -> None:
    """Renders the dataset organization and labeling workspace."""
    render_page_header(
        title_en="Dataset Organization & Labeling Workflow (Phase 4)",
        title_ta="தரவுத்தொகுப்பு மேலாண்மை மற்றும் லேபிளிங் (கட்டம் 4)",
        subtitle_en="Curate the family jasmine dataset, detect duplicates, and generate leak-free training splits",
        subtitle_ta="குடும்ப மல்லி புகைப்படங்களை நிர்வகிக்கவும், நகல்களை தவிர்க்கவும், பயிற்சிப் பிரிவுகளை உருவாக்கவும்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Dataset Curation Phase. Whole-plant photos are strictly segregated. Small dataset warnings are strictly enforced.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Do not claim that a small starter dataset is sufficient for training a reliable production model. Gather diverse photos across morning lighting, varying bush ages, and damage types.",
        message_ta="சிறிய அளவிலான புகைப்படங்களை வைத்து நம்பகமான மாதிரி (model) உருவாகிவிடும் என்று கருதக்கூடாது. காலை வெளிச்சம், பல கோணங்கள் மற்றும் சேதமடைந்த மொட்டுகளை தொடர்ந்து சேகரிக்கவும்.",
        is_tamil=is_tamil,
    )

    # -----------------------------------------------------------------------
    # Top KPI Metrics & Readiness Assessment
    # -----------------------------------------------------------------------
    summary = get_dataset_summary()
    scan = summary["scan"]
    stage_counts = scan["stage_counts"]

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #1b4332;">
                <div class="metric-label">Ready to Pluck</div>
                <div class="metric-value">{stage_counts.get('READY_TO_PLUCK', 0)}</div>
                <div class="metric-sub">பறிக்கத் தயார்</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #d4a373;">
                <div class="metric-label">Not Ready</div>
                <div class="metric-value">{stage_counts.get('NOT_READY', 0)}</div>
                <div class="metric-sub">முதிரவில்லை</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #f4a261;">
                <div class="metric-label">Too Open</div>
                <div class="metric-value">{stage_counts.get('TOO_OPEN', 0)}</div>
                <div class="metric-sub">அதிகம் விரிந்தது</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #e63946;">
                <div class="metric-label">Damaged / Pest</div>
                <div class="metric-value">{stage_counts.get('DAMAGED_OR_ABNORMAL', 0)}</div>
                <div class="metric-sub">சேதமடைந்தது</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c5:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #64748b;">
                <div class="metric-label">Segregated Whole-Plant</div>
                <div class="metric-value">{scan['whole_plant_count']}</div>
                <div class="metric-sub">Phase 7 YOLO queue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Readiness Banner
    if summary["readiness_status"] == "INSUFFICIENT_FOR_TRAINING":
        st.error(f"🛑 **Dataset Readiness Status:** {summary['readiness_message']}")
    elif summary["readiness_status"] == "MINIMAL_EXPERIMENTAL_ONLY":
        st.warning(f"⚠️ **Dataset Readiness Status:** {summary['readiness_message']}")
    else:
        st.success(f"✓ **Dataset Readiness Status:** {summary['readiness_message']}")

    # -----------------------------------------------------------------------
    # Multi-Tab Workflow
    # -----------------------------------------------------------------------
    tab_label, tab_dups, tab_split, tab_guide, tab_whole = st.tabs([
        "🏷️ Image Labeling" if not is_tamil else "🏷️ லேபிளிங் பணி",
        "🔍 Duplicate Audit" if not is_tamil else "🔍 நகல்கள் கண்டறிதல்",
        "✂️ Train/Val/Test Splits" if not is_tamil else "✂️ தரவு பிரிப்பு",
        "📸 Field Photography Guide" if not is_tamil else "📸 புகைப்பட நெறிமுறை",
        "🌿 Whole-Plant Holding" if not is_tamil else "🌿 முழு செடி சேமிப்பு",
    ])

    # -----------------------------------------------------------------------
    # Tab 1: Labeling Workflow
    # -----------------------------------------------------------------------
    with tab_label:
        st.markdown("### 🏷️ Label New or Incoming Photographs")
        col_up, col_assign = st.columns([1, 1])

        with col_up:
            photo_type = st.radio(
                "Photo Subject Type / புகைப்பட வகை:",
                options=["Single Flower Bud (தனி மொட்டு)", "Whole Plant Bush (முழு செடி)"],
                index=0,
                key="ds_photo_type",
            )
            is_single = "Single" in photo_type

            uploaded = st.file_uploader(
                "Upload jasmine photograph for dataset:",
                type=["jpg", "jpeg", "png", "webp"],
                key="ds_uploader",
            )

            if uploaded:
                v_ok, v_msg, v_meta = validate_image_file(uploaded)
                if v_ok:
                    img = Image.open(uploaded)
                    st.image(img, caption=f"Uploaded: {uploaded.name}", use_container_width=True)
                    st.caption(f"Dimensions: {v_meta['width']}x{v_meta['height']} px | Format: {v_meta['format']} | Size: {v_meta['size_kb']} KB")
                else:
                    st.error(f"❌ {v_msg}")

        with col_assign:
            if uploaded and v_ok:
                if is_single:
                    st.markdown("#### Assign Ground-Truth Flower Maturity:")
                    st.caption("Select the grower's confirmed harvesting stage:")

                    stage_choice = st.selectbox(
                        "Flower Stage / முதிர்ச்சி நிலை:",
                        options=[f"{s} — {TAMIL_STAGE_TRANSLATIONS[s]}" if is_tamil else s for s in FLOWER_STAGES],
                        key="ds_stage_choice",
                    )
                    chosen_stage = stage_choice.split(" — ")[0].strip()

                    label_notes = st.text_input("Observation Notes (Optional):", placeholder="e.g. Clean white petals, morning harvest", key="ds_notes")

                    if st.button("💾 Save & Label Single Bud", use_container_width=True, type="primary"):
                        target_dir = SINGLE_BUDS_RAW / chosen_stage
                        target_dir.mkdir(parents=True, exist_ok=True)
                        dest_file = target_dir / uploaded.name
                        with open(dest_file, "wb") as f:
                            f.write(uploaded.getvalue())

                        res = label_single_bud_image(dest_file, chosen_stage, notes=label_notes)
                        st.success(f"✓ Saved and labeled as **{chosen_stage}** in `data/raw/single_buds/{chosen_stage}/`!")
                        st.rerun()

                else:
                    st.info(
                        "ℹ️ **Whole-Plant Photo:** This image will be routed to `data/raw/whole_plant/incoming/`. "
                        "It will **not** be included in single-bud classification training and is reserved for YOLO multi-bud detection in Phase 7."
                    )
                    wp_notes = st.text_input("Bush Notes:", placeholder="e.g., Row 2 North Bush, high bud density", key="ds_wp_notes")
                    if st.button("📥 Stage in Whole-Plant Queue", use_container_width=True, type="primary"):
                        dest_file = WHOLE_PLANT_RAW / "incoming" / uploaded.name
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(dest_file, "wb") as f:
                            f.write(uploaded.getvalue())

                        stage_whole_plant_image(dest_file, notes=wp_notes)
                        st.success("✓ Saved to whole-plant incoming queue!")
                        st.rerun()
            else:
                st.info("Upload a photograph on the left to begin labeling.")

    # -----------------------------------------------------------------------
    # Tab 2: Duplicate Detection Audit
    # -----------------------------------------------------------------------
    with tab_dups:
        st.markdown("### 🔍 Duplicate & Near-Duplicate Image Audit")
        st.caption(
            "Detects byte-for-byte identical photos and perceptual burst-shot near-duplicates. "
            "Prevents data leakage across training, validation, and test splits."
        )

        if st.button("🚀 Run Duplicate Audit on Raw Dataset", key="btn_run_dups"):
            all_raw_images = []
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                all_raw_images.extend(list(SINGLE_BUDS_RAW.glob(f"**/*{ext}")))

            if not all_raw_images:
                st.info("No raw images found in `data/raw/single_buds/` yet.")
            else:
                dup_results = find_duplicates(all_raw_images)
                st.markdown(f"**Total Images Scanned:** {dup_results['total_scanned']}")

                if dup_results["exact_duplicates"]:
                    st.error(f"Found {len(dup_results['exact_duplicates'])} exact duplicate cluster(s):")
                    for cl in dup_results["exact_duplicates"]:
                        st.write(" • " + ", ".join([Path(p).name for p in cl]))
                else:
                    st.success("✓ No exact byte-for-byte duplicates detected.")

                if dup_results["near_duplicates"]:
                    st.warning(f"Found {len(dup_results['near_duplicates'])} perceptual near-duplicate pair(s) (Burst shots):")
                    for p1, p2, dist in dup_results["near_duplicates"]:
                        st.write(f" • {Path(p1).name} ↔ {Path(p2).name} (Hamming Distance: {dist}/64)")
                else:
                    st.success("✓ No near-duplicate burst photographs detected.")

    # -----------------------------------------------------------------------
    # Tab 3: Split Generator
    # -----------------------------------------------------------------------
    with tab_split:
        st.markdown("### ✂️ Generate Clean Dataset Partitions")
        st.caption("Splits labeled buds into `train` (70%), `val` (15%), and `test` (15%) splits while preserving near-duplicate groupings.")

        col_ratio1, col_ratio2, col_ratio3 = st.columns(3)
        with col_ratio1:
            r_train = st.slider("Train Ratio:", min_value=0.50, max_value=0.85, value=0.70, step=0.05)
        with col_ratio2:
            r_val = st.slider("Validation Ratio:", min_value=0.05, max_value=0.25, value=0.15, step=0.05)
        with col_ratio3:
            r_test = round(1.0 - r_train - r_val, 2)
            st.metric("Test Ratio:", f"{r_test:.2f}")

        if st.button("⚡ Partition Dataset & Generate Manifest", type="primary", key="btn_gen_split"):
            if summary["total_labeled"] == 0:
                st.error("Cannot generate splits: 0 labeled single-bud images in `data/raw/single_buds/`.")
            else:
                split_res = prepare_dataset_splits(train_ratio=r_train, val_ratio=r_val, test_ratio=r_test)
                st.success(f"✓ Partitions created successfully! Processed {split_res['total_split_samples']} images.")
                st.json(split_res["split_summary"])

    # -----------------------------------------------------------------------
    # Tab 4: Field Photography Protocol
    # -----------------------------------------------------------------------
    with tab_guide:
        st.markdown("### 📸 Field Photography Guidelines for the Family Garden")
        st.caption("Follow these rules to gather high-utility, diverse jasmine photographs:")

        for g in PHOTOGRAPHY_GUIDELINES:
            st.markdown(
                f"""
                <div class="farm-card" style="border-left: 4px solid #2d6a4f;">
                    <h4 style="margin:0 0 6px 0; color:#1b4332;">{g['title']}</h4>
                    <p style="margin:0; font-size:0.9rem; color:#334155;">{g['guideline']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------------------------
    # Tab 5: Whole-Plant Holding Area
    # -----------------------------------------------------------------------
    with tab_whole:
        st.markdown("### 🌿 Segregated Whole-Plant Holding Area")
        st.info(
            "Whole-plant bush photographs contain multiple overlapping buds under varying shadows. "
            "They are strictly excluded from single-bud classification to prevent noise, and will be annotated "
            "with bounding boxes for YOLO in Phase 7."
        )
        if scan["whole_plant_files"]:
            st.markdown(f"**Staged Whole-Plant Images ({len(scan['whole_plant_files'])}):**")
            for wp in scan["whole_plant_files"]:
                st.write(f" • `{Path(wp).name}`")
        else:
            st.caption("No whole-plant photographs currently in holding queue.")
