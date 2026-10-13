"""
Dataset Organization & Image-Labeling Workflow Page (Phase 4).
Supports ground-truth labeling, duplicate auditing, split generation, and photography protocol.
Displays purely in English, Tamil, or Telugu based on selected language.
"""

from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

from config.settings import FLOWER_STAGES
from src.core.i18n import (
    normalize_lang,
    get_stage_name,
    get_stage_key_from_name,
    t,
)
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


def render_dataset_page(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the dataset organization and labeling workspace in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Dataset Organization & Labeling Workflow (Phase 4)",
        title_ta="தரவுத்தொகுப்பு மேலாண்மை மற்றும் லேபிளிங் (கட்டம் 4)",
        title_te="డేటాసెట్ నిర్వహణ మరియు లేబులింగ్ (దశ 4)",
        subtitle_en="Curate the family jasmine dataset, detect duplicates, and generate leak-free training splits",
        subtitle_ta="குடும்ப மல்லி புகைப்படங்களை நிர்வகிக்கவும், நகல்களை தவிர்க்கவும், பயிற்சிப் பிரிவுகளை உருவாக்கவும்",
        subtitle_te="తోట ఫోటోలను నిర్వహించండి, నకిలీలను గుర్తించండి, శిక్షణ విభజనలను రూపొందించండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Dataset Curation Phase. Whole-plant photos are strictly segregated. Small dataset warnings are strictly enforced.",
        desc_ta="தரவு தொகுப்பு நிலை. முழு செடி புகைப்படங்கள் தனித்தனியாக பிரிக்கப்பட்டுள்ளன.",
        desc_te="డేటా నిర్వహణ దశ. మొత్తం మొక్క ఫోటోలు ప్రత్యేకంగా భద్రపరచబడ్డాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="Do not claim that a small starter dataset is sufficient for training a reliable production model. Gather diverse photos across morning lighting, varying bush ages, and damage types.",
        message_ta="குறைந்த புகைப்படங்களை வைத்து நம்பகமான மாதிரி உருவாகிவிடும் என்று கருதக்கூடாது. பல்வேறு காலை வெளிச்சம், செடி வயது மற்றும் சேத வகைகளை தொடர்ந்து சேகரிக்கவும்.",
        message_te="తక్కువ ఫోటోలతో నమ్మకమైన నమూనా రాదు. వివిధ సమయాలు, ఎండ వెలుతురు మరియు తెగుళ్ల ఫోటోలను క్రమం తప్పకుండా సేకరించండి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    # -----------------------------------------------------------------------
    # Top KPI Metrics & Readiness Assessment
    # -----------------------------------------------------------------------
    summary = get_dataset_summary()
    scan = summary["scan"]
    stage_counts = scan["stage_counts"]

    lbl_ready = get_stage_name("READY_TO_PLUCK", current_lang)
    lbl_not_ready = get_stage_name("NOT_READY", current_lang)
    lbl_too_open = get_stage_name("TOO_OPEN", current_lang)
    lbl_damaged = get_stage_name("DAMAGED_OR_ABNORMAL", current_lang)
    lbl_whole = (
        "முழு செடி" if current_lang == "ta"
        else ("మొత్తం మొక్క" if current_lang == "te"
        else "Whole-Plant")
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #1b4332;">
                <div class="metric-label">{lbl_ready}</div>
                <div class="metric-value">{stage_counts.get('READY_TO_PLUCK', 0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #d4a373;">
                <div class="metric-label">{lbl_not_ready}</div>
                <div class="metric-value">{stage_counts.get('NOT_READY', 0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #f4a261;">
                <div class="metric-label">{lbl_too_open}</div>
                <div class="metric-value">{stage_counts.get('TOO_OPEN', 0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #e63946;">
                <div class="metric-label">{lbl_damaged}</div>
                <div class="metric-value">{stage_counts.get('DAMAGED_OR_ABNORMAL', 0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c5:
        st.markdown(
            f"""
            <div class="metric-tile" style="border-top:4px solid #64748b;">
                <div class="metric-label">{lbl_whole}</div>
                <div class="metric-value">{scan['whole_plant_count']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if summary["readiness_status"] == "INSUFFICIENT_FOR_TRAINING":
        st.error(f"🛑 {summary['readiness_message']}")
    elif summary["readiness_status"] == "MINIMAL_EXPERIMENTAL_ONLY":
        st.warning(f"⚠️ {summary['readiness_message']}")
    else:
        st.success(f"✓ {summary['readiness_message']}")

    # -----------------------------------------------------------------------
    # Multi-Tab Workflow
    # -----------------------------------------------------------------------
    if current_lang == "ta":
        tabs_labels = [
            "🏷️ லேபிளிங் பணி",
            "🔍 நகல்கள் கண்டறிதல்",
            "✂️ தரவு பிரிப்பு",
            "🧠 மாதிரி பயிற்சி மற்றும் மதிப்பீடு",
            "📸 புகைப்பட நெறிமுறை",
            "🌿 முழு செடி சேமிப்பு",
        ]
    elif current_lang == "te":
        tabs_labels = [
            "🏷️ ఫోటోల లేబులింగ్",
            "🔍 నకిలీల తనిఖీ",
            "✂️ డేటా విభజనలు",
            "🧠 నమూనా శిక్షణ మరియు మూల్యాంకనం",
            "📸 ఫోటోగ్రఫీ మార్గదర్శకాలు",
            "🌿 మొత్తం మొక్కల నిల్వ",
        ]
    else:
        tabs_labels = [
            "🏷️ Image Labeling",
            "🔍 Duplicate Audit",
            "✂️ Train/Val/Test Splits",
            "🧠 Model Training & Eval",
            "📸 Field Photography Guide",
            "🌿 Whole-Plant Holding",
        ]

    tab_label, tab_dups, tab_split, tab_train, tab_guide, tab_whole = st.tabs(tabs_labels)

    # -----------------------------------------------------------------------
    # Tab 1: Labeling Workflow
    # -----------------------------------------------------------------------
    with tab_label:
        l_title = (
            "புதிய புகைப்படங்களை லேபிளிங் செய்தல்" if current_lang == "ta"
            else ("కొత్త ఫోటోల లేబులింగ్" if current_lang == "te"
            else "Label New or Incoming Photographs")
        )
        st.markdown(f"### 🏷️ {l_title}")
        col_up, col_assign = st.columns([1, 1])

        with col_up:
            p_type_opts = (
                ["தனி மொட்டு", "முழு செடி"] if current_lang == "ta"
                else (["ఒంటరి పూల మొగ్గ", "మొత్తం మొక్క"] if current_lang == "te"
                else ["Single Flower Bud", "Whole Plant Bush"])
            )
            p_type_lbl = "புகைப்பட வகை:" if current_lang == "ta" else ("ఫోటో రకం:" if current_lang == "te" else "Photo Subject Type:")
            photo_type = st.radio(p_type_lbl, options=p_type_opts, index=0, key="ds_photo_type")
            is_single = photo_type in ["தனி மொட்டு", "ఒంటరి పూల మొగ్గ", "Single Flower Bud"]

            up_lbl = "புகைப்படத்தை பதிவேற்றவும்:" if current_lang == "ta" else ("ఫోటోను అప్‌లోడ్ చేయండి:" if current_lang == "te" else "Upload jasmine photograph:")
            uploaded = st.file_uploader(up_lbl, type=["jpg", "jpeg", "png", "webp"], key="ds_uploader")

            if uploaded:
                v_ok, v_msg, v_meta = validate_image_file(uploaded)
                if v_ok:
                    img = Image.open(uploaded)
                    st.image(img, caption=uploaded.name, use_container_width=True)
                    st.caption(f"{v_meta['width']}x{v_meta['height']} px | {v_meta['size_kb']} KB")
                else:
                    st.error(f"❌ {v_msg}")

        with col_assign:
            if uploaded and v_ok:
                if is_single:
                    stage_opts = [get_stage_name(s, current_lang) for s in FLOWER_STAGES]
                    stage_choice = st.selectbox(t("maturity_stage", current_lang), options=stage_opts, key="ds_stage_choice")
                    chosen_stage = get_stage_key_from_name(stage_choice, current_lang)

                    nt_lbl = "குறிப்புகள்:" if current_lang == "ta" else ("గమనికలు:" if current_lang == "te" else "Observation Notes:")
                    label_notes = st.text_input(nt_lbl, placeholder="", key="ds_notes")

                    btn_lbl = (
                        "💾 மொட்டை லேபிள் செய்து சேமிக்கவும்" if current_lang == "ta"
                        else ("💾 మొగ్గను లేబుల్ చేసి భద్రపరచు" if current_lang == "te"
                        else "💾 Save & Label Single Bud")
                    )
                    if st.button(btn_lbl, use_container_width=True, type="primary"):
                        target_dir = SINGLE_BUDS_RAW / chosen_stage
                        target_dir.mkdir(parents=True, exist_ok=True)
                        dest_file = target_dir / uploaded.name
                        with open(dest_file, "wb") as f:
                            f.write(uploaded.getvalue())

                        label_single_bud_image(dest_file, chosen_stage, notes=label_notes)
                        st.success(f"✓ {chosen_stage}")
                        st.rerun()

                else:
                    info_msg = (
                        "ℹ️ முழு செடி புகைப்படம் YOLO மாதிரிக்கு பிரத்யேகமாக வைக்கப்படும்." if current_lang == "ta"
                        else ("ℹ️ మొత్తం మొక్క ఫోటో YOLO నమూనా కోసం ప్రత్యేకంగా ఉంచబడుతుంది." if current_lang == "te"
                        else "ℹ️ Whole-Plant photo routed to incoming queue for Phase 7 YOLO.")
                    )
                    st.info(info_msg)
                    wp_notes = st.text_input("Bush Notes:", placeholder="", key="ds_wp_notes")
                    btn_wp_lbl = (
                        "📥 முழு செடி வரிசையில் சேமி" if current_lang == "ta"
                        else ("📥 మొత్తం మొక్కల వరుసలో భద్రపరచు" if current_lang == "te"
                        else "📥 Stage in Whole-Plant Queue")
                    )
                    if st.button(btn_wp_lbl, use_container_width=True, type="primary"):
                        dest_file = WHOLE_PLANT_RAW / "incoming" / uploaded.name
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(dest_file, "wb") as f:
                            f.write(uploaded.getvalue())

                        stage_whole_plant_image(dest_file, notes=wp_notes)
                        st.success("✓ Saved!")
                        st.rerun()

    # -----------------------------------------------------------------------
    # Tab 2: Duplicate Detection Audit
    # -----------------------------------------------------------------------
    with tab_dups:
        d_head = "நகல்கள் கண்டறிதல்" if current_lang == "ta" else ("నకిలీల తనిఖీ" if current_lang == "te" else "Duplicate Image Audit")
        st.markdown(f"### 🔍 {d_head}")
        btn_d_lbl = "🚀 நகல்கள் தணிக்கையை இயக்கு" if current_lang == "ta" else ("🚀 నకిలీల తనిఖీని ప్రారంభించు" if current_lang == "te" else "🚀 Run Duplicate Audit")
        if st.button(btn_d_lbl, key="btn_run_dups"):
            all_raw_images = []
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                all_raw_images.extend(list(SINGLE_BUDS_RAW.glob(f"**/*{ext}")))

            if not all_raw_images:
                st.info("No raw images found.")
            else:
                dup_results = find_duplicates(all_raw_images)
                st.write(f"Scanned: {dup_results['total_scanned']}")
                if dup_results["exact_duplicates"]:
                    st.error(f"Exact duplicates found: {len(dup_results['exact_duplicates'])}")
                else:
                    st.success("✓ No exact duplicates.")
                if dup_results["near_duplicates"]:
                    st.warning(f"Near duplicates found: {len(dup_results['near_duplicates'])}")
                else:
                    st.success("✓ No near duplicates.")

    # -----------------------------------------------------------------------
    # Tab 3: Split Generator
    # -----------------------------------------------------------------------
    with tab_split:
        s_head = "தரவு பிரிப்பு" if current_lang == "ta" else ("డేటా విభజన" if current_lang == "te" else "Generate Clean Partitions")
        st.markdown(f"### ✂️ {s_head}")
        col_ratio1, col_ratio2, col_ratio3 = st.columns(3)
        with col_ratio1:
            r_train = st.slider("Train:", 0.50, 0.85, 0.70, 0.05)
        with col_ratio2:
            r_val = st.slider("Validation:", 0.05, 0.25, 0.15, 0.05)
        with col_ratio3:
            r_test = round(1.0 - r_train - r_val, 2)
            st.metric("Test:", f"{r_test:.2f}")

        btn_s_lbl = "⚡ தரவைப் பிரி" if current_lang == "ta" else ("⚡ డేటాను విభజించు" if current_lang == "te" else "⚡ Partition Dataset")
        if st.button(btn_s_lbl, type="primary", key="btn_gen_split"):
            if summary["total_labeled"] == 0:
                st.error("0 labeled images.")
            else:
                split_res = prepare_dataset_splits(train_ratio=r_train, val_ratio=r_val, test_ratio=r_test)
                st.success(f"✓ Processed {split_res['total_split_samples']} images.")
                st.json(split_res["split_summary"])

    # -----------------------------------------------------------------------
    # Tab 4: Model Training & Evaluation
    # -----------------------------------------------------------------------
    with tab_train:
        m_head = "மாதிரி பயிற்சி மற்றும் மதிப்பீடு" if current_lang == "ta" else ("నమూనా శిక్షణ మరియు మూల్యాంకనం" if current_lang == "te" else "MobileNetV2 Model Training")
        st.markdown(f"### 🧠 {m_head}")

        from src.models.training import train_flower_classifier, DEFAULT_MODEL_PATH
        from src.models.evaluator import evaluate_model
        from src.models.inference import is_model_available

        col_cfg, col_act = st.columns([1, 1])
        with col_cfg:
            epochs = st.slider("Epochs:", 3, 30, 8, 1, key="tr_epochs")
            batch_sz = st.selectbox("Batch Size:", [4, 8, 16], index=1, key="tr_batch")
            st.write(f"Checkpoint: `{DEFAULT_MODEL_PATH.name}`")

        with col_act:
            btn_tr_lbl = "🚀 பயிற்சியைத் தொடங்கு" if current_lang == "ta" else ("🚀 శిక్షణను ప్రారంభించు" if current_lang == "te" else "🚀 Train MobileNetV2 Classifier")
            if st.button(btn_tr_lbl, type="primary", key="btn_start_train"):
                with st.spinner("..."):
                    res = train_flower_classifier(epochs=epochs, batch_size=batch_sz)
                    if res["status"] == "COMPLETED":
                        st.success(f"✓ Completed in {res['elapsed_seconds']}s!")
                    else:
                        st.error(f"❌ {res.get('message')}")

            if is_model_available():
                btn_ev_lbl = "📊 மாதிரியை மதிப்பிடு" if current_lang == "ta" else ("📊 నమూనాను మూల్యాంకనం చేయి" if current_lang == "te" else "📊 Evaluate Model")
                if st.button(btn_ev_lbl, key="btn_eval_test"):
                    with st.spinner("..."):
                        eval_res = evaluate_model()
                        if eval_res["status"] == "COMPLETED":
                            st.success(f"✓ Accuracy: {eval_res['overall_test_accuracy'] * 100:.1f}%")
                        else:
                            st.error(f"❌ {eval_res.get('message')}")

    # -----------------------------------------------------------------------
    # Tab 5: Field Photography Protocol
    # -----------------------------------------------------------------------
    with tab_guide:
        g_head = "புகைப்பட நெறிமுறை" if current_lang == "ta" else ("ఫోటోగ్రఫీ మార్గదర్శకాలు" if current_lang == "te" else "Field Photography Protocol")
        st.markdown(f"### 📸 {g_head}")
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
    # Tab 6: Whole-Plant Holding Area
    # -----------------------------------------------------------------------
    with tab_whole:
        w_head = "முழு செடி சேமிப்பு" if current_lang == "ta" else ("మొత్తం మొక్కల నిల్వ" if current_lang == "te" else "Whole-Plant Holding Area")
        st.markdown(f"### 🌿 {w_head}")
        if scan["whole_plant_files"]:
            st.write(f"Staged ({len(scan['whole_plant_files'])}):")
            for wp in scan["whole_plant_files"]:
                st.write(f" • `{Path(wp).name}`")
        else:
            empty_wp = "புகைப்படங்கள் எதுவும் இல்லை." if current_lang == "ta" else ("ఇంకా ఫోటోలు లేవు." if current_lang == "te" else "No photos in queue.")
            st.caption(empty_wp)
