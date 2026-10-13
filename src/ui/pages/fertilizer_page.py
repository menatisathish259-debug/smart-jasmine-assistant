"""
Fertilizer Identification and Management Page (Module E).
Records fertilizer applications, verifies bag label formulations, calculates active nutrient inputs,
and provides TNAU-aligned decision support cross-referencing soil and weather conditions.
"""

from datetime import date
from PIL import Image
import pandas as pd
import streamlit as st

from config.settings import FERTILIZER_CATEGORIES
from src.agronomy.fertilizer_calculator import (
    STANDARD_FERTILIZER_DATABASE,
    verify_fertilizer_formulation,
    calculate_nutrient_inputs,
    evaluate_jasmine_fertilizer_split,
    TNAU_ANNUAL_DOSE_G_PER_PLANT,
)
from src.core.validation import validate_image_file
from src.database.repository import (
    get_garden_sections,
    get_fertilizer_products,
    add_fertilizer_product,
    add_fertilizer_application,
    get_fertilizer_applications,
    get_total_nutrients_applied,
    get_cumulative_nutrients_by_section,
    get_recent_irrigation_by_section,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_fertilizer_record


def render_fertilizer_records(is_tamil: bool) -> None:
    """Renders the upgraded fertilizer management and nutrient accounting page."""
    render_page_header(
        title_en="Fertilizer Identification & Management (Module E)",
        title_ta="உர மேலாண்மை மற்றும் ஊட்டச்சத்து கணக்கீடு (பகுதி E)",
        subtitle_en="Verify fertilizer formulations, calculate active NPK inputs, and align with TNAU Jasminum sambac standards",
        subtitle_ta="உரங்களை முறைப்படி சரிபார்த்து, பயிருக்கு கிடைத்த தழை, மணி, சாம்பல் சத்துக்களை கணக்கிடுங்கள்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Nutrient Accounting & Formulation Verifier Active. Calculates elemental NPK delivered per bush. Cross-references rain forecast.",
        is_tamil=is_tamil,
    )

    render_safety_warning(
        message_en="NEVER identify fertilizer solely by package color or shape. Excessive nitrogen (Urea) produces lush vegetative shoots with fewer flower buds, and causes chemical root burn in dry ground.",
        message_ta="பையின் நிறம் அல்லது வடிவத்தை மட்டும் வைத்து உரத்தை அடையாளம் காணாதீர்கள். அதிக தழைச்சத்து (யுரியா) இலை வளர்ச்சியை மட்டுமே கூட்டி பூக்களை குறைத்துவிடும்.",
        is_tamil=is_tamil,
    )

    # Fetch database garden sections
    db_sections = get_garden_sections()
    section_map = {s["section_name"]: s for s in db_sections} if db_sections else {}
    section_options = list(section_map.keys()) if section_map else [
        "Section A (North Bed)", "Section B (South Bed)", "Section C (East Plot)", "Section D (West Plot)"
    ]

    # Fetch custom registered products
    registered_db_products = get_fertilizer_products()
    product_choices = list(STANDARD_FERTILIZER_DATABASE.keys())
    for p in registered_db_products:
        if p["product_name"] not in product_choices:
            product_choices.append(p["product_name"])

    tab_app, tab_verify, tab_budget = st.tabs([
        "📝 1. Log Application & Calculate NPK" if not is_tamil else "📝 1. உரமிடுதல் பதிவு & கணக்கீடு",
        "🏷️ 2. Formulation Verifier & Label Entry" if not is_tamil else "🏷️ 2. உர ஆய்வு & லேபிள் பதிவு",
        "📊 3. Seasonal Nutrient Budget" if not is_tamil else "📊 3. ஊட்டச்சத்து இருப்பு & TNAU இலக்கு",
    ])

    # -----------------------------------------------------------------------
    # TAB 1: Log Application & Nutrient Accounting
    # -----------------------------------------------------------------------
    with tab_app:
        col_form, col_calc = st.columns([1, 1])

        with col_form:
            st.markdown("### 📝 Log Fertilizer Application Event")

            app_date = st.date_input("Application Date / தேதி:", value=date.today(), max_value=date.today(), key="fa_date")
            chosen_sec_name = st.selectbox("Garden Section / பாத்தி:", options=section_options, key="fa_sec")
            chosen_sec_obj = section_map.get(chosen_sec_name)
            plant_count = chosen_sec_obj.get("plant_count", 500) if chosen_sec_obj else 500
            sec_id = chosen_sec_obj.get("id") if chosen_sec_obj else None

            # Weather Cross-Reference (Rain check)
            recent_irrig = get_recent_irrigation_by_section(sec_id, limit=1)
            forecast_rain = recent_irrig[0].get("forecast_rain_mm", 0.0) if recent_irrig else 0.0
            if forecast_rain >= 15.0:
                st.error(f"🌧️ WEATHER HAZARD: {forecast_rain:.1f} mm rain forecasted! Delay granular topdressing to prevent leaching.")

            chosen_product_name = st.selectbox("Fertilizer Product / உரம்:", options=product_choices, key="fa_prod")

            # Determine formulation defaults
            default_n, default_p, default_k = 0.0, 0.0, 0.0
            default_cat = "Chemical / Mineral"
            if chosen_product_name in STANDARD_FERTILIZER_DATABASE:
                std_info = STANDARD_FERTILIZER_DATABASE[chosen_product_name]
                default_n = std_info["n_pct"]
                default_p = std_info["p_pct"]
                default_k = std_info["k_pct"]
                default_cat = std_info["category"]
            else:
                for rp in registered_db_products:
                    if rp["product_name"] == chosen_product_name:
                        default_n = rp.get("formulation_n", 0.0)
                        default_p = rp.get("formulation_p", 0.0)
                        default_k = rp.get("formulation_k", 0.0)
                        default_cat = rp.get("category", "Chemical / Mineral")
                        break

            st.caption(f"Guaranteed Analysis: **{default_n}% N - {default_p}% P₂O₅ - {default_k}% K₂O** ({default_cat})")

            col_q, col_stg = st.columns(2)
            with col_q:
                qty_kg = st.number_input("Quantity Applied (kg):", min_value=0.5, max_value=2000.0, value=25.0, step=5.0, key="fa_qty")
            with col_stg:
                split_stage = st.selectbox(
                    "Crop Split Stage:",
                    options=["flowering_flush", "post_pruning"],
                    format_func=lambda x: "Peak Flowering Flush (Mar-Apr)" if x=="flowering_flush" else "Post-Pruning Basal (Dec-Jan)",
                    key="fa_split",
                )

            method = st.selectbox(
                "Application Method / இடும் முறை:",
                options=[
                    "Ring application around root basin (15-20 cm away from trunk) + soil incorporation",
                    "Broadcasting before light hoeing",
                    "Foliar spray (water-soluble micronutrients/19-19-19)",
                    "Basal incorporation at annual winter pruning",
                    "Fertigation (drip injection)",
                ],
                key="fa_method",
            )

            reason = st.text_input("Application Purpose:", placeholder="e.g. Flush boost before commercial festival harvest", key="fa_reason")

            log_app_btn = st.button("💾 Record Fertilizer Application", use_container_width=True, type="primary")

        # Real-time Nutrient Accounting Card
        with col_calc:
            st.markdown("### 📊 Active Nutrient Input Accounting")
            st.caption(f"Calculated for **{qty_kg:.1f} kg** applied across **{plant_count} bushes** in {chosen_sec_name}:")

            nutrients_res = calculate_nutrient_inputs(
                quantity_kg=qty_kg,
                n_pct=default_n,
                p_pct=default_p,
                k_pct=default_k,
                plant_count=plant_count,
            )

            deliv = nutrients_res["nutrients_delivered_kg"]
            per_plant = nutrients_res["per_plant_g"]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Delivered N", f"{deliv['N']:.2f} kg", f"{per_plant['N_g']:.1f} g / bush")
            with c2:
                st.metric("Delivered P₂O₅", f"{deliv['P2O5']:.2f} kg", f"{per_plant['P2O5_g']:.1f} g / bush")
            with c3:
                st.metric("Delivered K₂O", f"{deliv['K2O']:.2f} kg", f"{per_plant['K2O_g']:.1f} g / bush")

            # Evaluate against TNAU recommendations
            eval_split = evaluate_jasmine_fertilizer_split(
                n_applied_g_plant=per_plant["N_g"],
                p_applied_g_plant=per_plant["P2O5_g"],
                k_applied_g_plant=per_plant["K2O_g"],
                split_stage=split_stage,
            )

            st.markdown(f"#### TNAU Alignment: {eval_split['stage_title']}")
            if eval_split["safety_alerts"]:
                for alert in eval_split["safety_alerts"]:
                    st.error(alert)
            else:
                st.success("✓ Application dose per bush is within safe agronomic thresholds.")

            for note in eval_split["evaluation_notes"]:
                st.info(f"💡 {note}")

            st.caption(f"Source: {eval_split['evidence_source']}")

        # Handle Save Event
        if log_app_btn:
            app_id = add_fertilizer_application(
                product_name=chosen_product_name,
                category=default_cat,
                quantity_kg=qty_kg,
                application_date=str(app_date),
                application_method=method,
                section_id=sec_id,
                reason=reason or "Seasonal application.",
                n_supplied_kg=deliv["N"],
                p_supplied_kg=deliv["P2O5"],
                k_supplied_kg=deliv["K2O"],
                notes=f"Calculated: {per_plant['N_g']}g N, {per_plant['P2O5_g']}g P, {per_plant['K2O_g']}g K per bush.",
            )

            add_fertilizer_record({
                "date": str(app_date),
                "section": chosen_sec_name,
                "product_name": chosen_product_name,
                "category": default_cat,
                "quantity_kg": qty_kg,
                "method": method,
                "reason": reason,
                "n_kg": deliv["N"],
                "p_kg": deliv["P2O5"],
                "k_kg": deliv["K2O"],
            })
            st.success(f"✅ Fertilizer application #{app_id} successfully saved to SQLite!")
            st.rerun()

    # -----------------------------------------------------------------------
    # TAB 2: Formulation Verifier & Label Entry
    # -----------------------------------------------------------------------
    with tab_verify:
        st.markdown("### 🏷️ Fertilizer Bag Label Verifier & Registry")
        st.caption("Verify printed Guaranteed Analysis percentages before applying to farm beds:")

        with st.form("label_verification_form"):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                new_prod_name = st.text_input("Product Trade Name / Brand:", placeholder="e.g. Coromandel Gromor 17-17-17", key="lv_name")
                new_category = st.selectbox("Product Classification:", options=FERTILIZER_CATEGORIES, key="lv_cat")
                new_manufacturer = st.text_input("Manufacturer / Marketing Company:", placeholder="e.g. Coromandel International Ltd", key="lv_mfg")
            with col_b2:
                col_n, col_p, col_k = st.columns(3)
                with col_n:
                    input_n = st.number_input("Guaranteed N (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_n")
                with col_p:
                    input_p = st.number_input("Guaranteed P₂O₅ (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_p")
                with col_k:
                    input_k = st.number_input("Guaranteed K₂O (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_k")

                input_secondary = st.text_input("Secondary / Micronutrients on Label:", placeholder="e.g. Sulphur 4%, Zinc 0.5%", key="lv_sec")

            verify_submit = st.form_submit_button("🔍 Verify & Register Formulation", use_container_width=True)

        if verify_submit:
            if not new_prod_name:
                st.error("Please provide a product trade name.")
            else:
                ver_res = verify_fertilizer_formulation(
                    product_name=new_prod_name,
                    category=new_category,
                    n_pct=input_n,
                    p_pct=input_p,
                    k_pct=input_k,
                    secondary_nutrients=input_secondary,
                )

                if not ver_res["is_valid"]:
                    st.error(f"❌ Formulation Invalid: {'; '.join(ver_res['errors'])}")
                else:
                    st.success(f"✓ Valid Formulation! Total active macronutrients: **{ver_res['total_active_macro_pct']}%**.")
                    for warn in ver_res["warnings"]:
                        st.warning(warn)

                    # Save to database
                    add_fertilizer_product(
                        product_name=new_prod_name,
                        category=new_category,
                        formulation_n=input_n,
                        formulation_p=input_p,
                        formulation_k=input_k,
                        secondary_nutrients=input_secondary,
                        manufacturer=new_manufacturer,
                    )
                    st.success(f"✓ '{new_prod_name}' registered in farm database!")
                    st.rerun()

        st.markdown("---")
        st.markdown("#### 📸 Bag Label Photographic Upload")
        st.caption("Store high-resolution photograph of product label for batch traceability:")
        uploaded_bag_label = st.file_uploader("Upload label photo:", type=["jpg", "jpeg", "png", "webp"], key="bag_label_up")
        if uploaded_bag_label:
            v_ok, v_msg, v_meta = validate_image_file(uploaded_bag_label)
            if v_ok:
                st.image(Image.open(uploaded_bag_label), caption=f"Label: {uploaded_bag_label.name}", use_container_width=True)
                st.success(f"✓ Label image verified ({v_meta['size_kb']} KB)")
            else:
                st.error(f"❌ {v_msg}")

    # -----------------------------------------------------------------------
    # TAB 3: Seasonal Nutrient Budget & TNAU Progress
    # -----------------------------------------------------------------------
    with tab_budget:
        st.markdown("### 📊 Seasonal Garden Nutrient Budget vs TNAU Target")
        st.caption("Cumulative kilograms of active nutrients delivered to the farm:")

        totals = get_total_nutrients_applied()
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Cumulative Nitrogen (N)", f"{totals['total_n']:.2f} kg", "TNAU: ~60g/plant/yr")
        with m2:
            st.metric("Cumulative Phosphorus (P₂O₅)", f"{totals['total_p']:.2f} kg", "TNAU: ~120g/plant/yr")
        with m3:
            st.metric("Cumulative Potassium (K₂O)", f"{totals['total_k']:.2f} kg", "TNAU: ~120g/plant/yr")

        # Over-fertilization Risk Guardrail
        total_plants = sum(s.get("plant_count", 0) for s in db_sections) if db_sections else 2000
        if total_plants > 0:
            avg_n_g = (totals["total_n"] * 1000.0) / total_plants
            if avg_n_g > 65.0:
                st.error(
                    f"⚠️ HIGH NITROGEN ALERT ({avg_n_g:.1f} g N/bush across garden). "
                    "Cumulative nitrogen has exceeded the annual recommended target. "
                    "Withhold further urea applications to avoid flower bud shedding and bud worm outbreaks."
                )

        st.markdown("---")
        st.markdown("### 📋 Historic Fertilizer Applications Log")
        all_apps = get_fertilizer_applications()
        if all_apps:
            disp_apps = []
            for a in all_apps:
                disp_apps.append({
                    "Date": a["application_date"],
                    "Section": a.get("section_name") or "Whole Garden",
                    "Product": a["product_name"],
                    "Qty (kg)": a["quantity_kg"],
                    "N (kg)": a["n_supplied_kg"],
                    "P₂O₅ (kg)": a["p_supplied_kg"],
                    "K₂O (kg)": a["k_supplied_kg"],
                    "Method": a["application_method"],
                    "Reason": a.get("reason") or "Routine application",
                })
            st.dataframe(pd.DataFrame(disp_apps), use_container_width=True, hide_index=True)
        else:
            st.info("No fertilizer applications logged in the database yet.")
