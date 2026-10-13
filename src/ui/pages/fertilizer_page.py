"""
Fertilizer Identification and Management Page (Module E).
Records fertilizer applications, calculates nutrient contributions, and validates product labels.
"""

from datetime import date
from PIL import Image
import streamlit as st

from config.settings import FERTILIZER_CATEGORIES
from src.core.constants import STANDARD_FERTILIZER_NPK
from src.core.validation import validate_fertilizer_entry, validate_image_file
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_fertilizer_record


def render_fertilizer_records(is_tamil: bool) -> None:
    """Renders the fertilizer tracking and nutrient calculation page."""
    render_page_header(
        title_en="Fertilizer Identification & Management (Module E)",
        title_ta="உர மேலாண்மை மற்றும் ஊட்டச்சத்து கணக்கீடு (பகுதி E)",
        subtitle_en="Track organic and mineral fertilizer applications and calculate active nutrient contributions",
        subtitle_ta="இயற்கை மற்றும் ரசாயன உரங்களை பதிவுசெய்து, பயிருக்கு கிடைத்த தழை, மணி, சாம்பல் சத்துக்களை கணக்கிடுங்கள்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Nutrient Accounting Active. OCR label reading will be integrated in Phase 9. Always verify product grades directly from label text.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="Never identify a fertilizer solely by package color or shape. Excessive nitrogen (Urea) produces lush green leaves with fewer flowers, and can cause root burn in dry soil.",
        message_ta="பையின் நிறம் அல்லது வடிவத்தை மட்டும் வைத்து உரத்தை அடையாளம் காணாதீர்கள். அதிக தழைச்சத்து (யுரியா) இலை வளர்ச்சியை மட்டுமே கூட்டி பூக்களை குறைத்துவிடும்.",
        is_tamil=is_tamil,
    )

    col_form, col_nutrients = st.columns([1, 1])

    with col_form:
        st.markdown("### 📝 1. Log Fertilizer Application (உரமிடுதல் பதிவு)")

        with st.form("fertilizer_log_form"):
            category = st.selectbox(
                "Fertilizer Category / உர வகை:",
                options=FERTILIZER_CATEGORIES,
                key="fert_category",
            )

            product_name = st.text_input(
                "Product Brand / Trade Name / பெயர்:",
                value="Urea (46% N)" if "Urea" in category else "Neem Coated Fertilizer",
                help="Exact name printed on the bag label",
                key="fert_name",
            )

            col_q, col_d = st.columns(2)
            with col_q:
                quantity_kg = st.number_input(
                    "Quantity Applied (kg) / அளவு (கிலோ):",
                    min_value=0.5,
                    max_value=5000.0,
                    value=25.0,
                    step=5.0,
                    key="fert_qty",
                )
            with col_d:
                app_date = st.date_input(
                    "Application Date / தேதி:",
                    value=date.today(),
                    max_value=date.today(),
                    key="fert_date",
                )

            area_treated = st.selectbox(
                "Garden Section / Treated Area / இடப்பரப்பு:",
                options=[
                    "Entire Farm (0.5 Acre)",
                    "Section A (North Bed)",
                    "Section B (South Bed)",
                    "Section C (East Plot)",
                    "Section D (West Plot)",
                    "Young Plants Only",
                ],
                key="fert_area",
            )

            method = st.selectbox(
                "Application Method / இடும் முறை:",
                options=[
                    "Ring application around root zone (15-20 cm away from trunk) + soil incorporation",
                    "Broadcasting before light hoeing",
                    "Foliar spray (water-soluble micronutrients/19-19-19)",
                    "Basal application at annual pruning",
                    "Fertigation (drip injection)",
                ],
                key="fert_method",
            )

            reason = st.text_input(
                "Reason for Application / நோக்கம்:",
                placeholder="e.g., Post-pruning vegetative growth, bud development, flower flush boost",
                key="fert_reason",
            )

            submit_fert = st.form_submit_button("💾 Save Fertilizer Application", use_container_width=True)

        if submit_fert:
            is_valid, msg = validate_fertilizer_entry(product_name, quantity_kg, app_date, area_treated)
            if not is_valid:
                st.error(f"❌ {msg}")
            else:
                # Estimate nutrients supplied
                n_contrib, p_contrib, k_contrib = 0.0, 0.0, 0.0
                for standard_name, npk_vals in STANDARD_FERTILIZER_NPK.items():
                    if standard_name.lower() in category.lower() or standard_name.lower() in product_name.lower():
                        n_contrib = round(quantity_kg * (npk_vals["N"] / 100.0), 2)
                        p_contrib = round(quantity_kg * (npk_vals["P"] / 100.0), 2)
                        k_contrib = round(quantity_kg * (npk_vals["K"] / 100.0), 2)
                        break

                record = {
                    "date": str(app_date),
                    "section": area_treated,
                    "product_name": product_name,
                    "category": category,
                    "quantity_kg": quantity_kg,
                    "method": method,
                    "reason": reason or "Seasonal maintenance.",
                    "nutrients_estimated": f"N: {n_contrib} kg | P2O5: {p_contrib} kg | K2O: {k_contrib} kg",
                    "n_kg": n_contrib,
                    "p_kg": p_contrib,
                    "k_kg": k_contrib,
                }
                add_fertilizer_record(record)
                st.success(f"✅ Fertilizer record saved! Estimated active nutrients: N={n_contrib} kg, P={p_contrib} kg, K={k_contrib} kg.")

    with col_nutrients:
        st.markdown("### 📊 2. Nutrient Contribution Summary")
        st.caption("Cumulative nutrients supplied from all recorded applications:")

        total_n = sum(r.get("n_kg", 0.0) for r in st.session_state.fertilizer_records)
        total_p = sum(r.get("p_kg", 0.0) for r in st.session_state.fertilizer_records)
        total_k = sum(r.get("k_kg", 0.0) for r in st.session_state.fertilizer_records)

        nk1, nk2, nk3 = st.columns(3)
        with nk1:
            st.markdown(
                f"""
                <div class="metric-tile" style="border-top:4px solid #1b4332;">
                    <div class="metric-label">Total Nitrogen (N)</div>
                    <div class="metric-value">{total_n:.2f} kg</div>
                    <div class="metric-sub">Foliage & growth</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with nk2:
            st.markdown(
                f"""
                <div class="metric-tile" style="border-top:4px solid #d4a373;">
                    <div class="metric-label">Total Phosphorus (P₂O₅)</div>
                    <div class="metric-value">{total_p:.2f} kg</div>
                    <div class="metric-sub">Rooting & bud initiation</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with nk3:
            st.markdown(
                f"""
                <div class="metric-tile" style="border-top:4px solid #52b788;">
                    <div class="metric-label">Total Potassium (K₂O)</div>
                    <div class="metric-value">{total_k:.2f} kg</div>
                    <div class="metric-sub">Flower weight & fragrance</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🏷️ Product Label Photograph Upload")
        uploaded_label = st.file_uploader(
            "Upload bag label photograph for record verification:",
            type=["jpg", "jpeg", "png", "webp"],
            key="fert_label_uploader",
        )
        if uploaded_label:
            v_ok, v_msg, v_meta = validate_image_file(uploaded_label)
            if v_ok:
                st.image(Image.open(uploaded_label), caption=f"Label photo: {uploaded_label.name}", use_container_width=True)
                st.success(f"✓ Label image verified ({v_meta['size_kb']} KB)")
            else:
                st.error(f"❌ {v_msg}")

    # -----------------------------------------------------------------------
    # Fertilizer History Table
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📋 Application Records (உரப் பதிவுகள்)")
    if st.session_state.fertilizer_records:
        import pandas as pd
        df = pd.DataFrame(st.session_state.fertilizer_records)
        display_cols = [c for c in ["date", "section", "product_name", "category", "quantity_kg", "method", "nutrients_estimated", "reason"] if c in df.columns]
        st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No fertilizer applications recorded yet.")
