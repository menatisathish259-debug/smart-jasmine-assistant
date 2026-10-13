"""
Fertilizer Identification and Management Page (Module E).
Records fertilizer applications, verifies bag label formulations, calculates active nutrient inputs,
and provides horticultural decision support cross-referencing soil and weather conditions.
Displays purely in English, Tamil, or Telugu based on selected language.
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
)
from src.core.validation import validate_image_file
from src.core.i18n import (
    normalize_lang,
    get_section_options,
    t,
)
from src.database.repository import (
    get_garden_sections,
    get_fertilizer_products,
    add_fertilizer_product,
    add_fertilizer_application,
    get_fertilizer_applications,
    get_total_nutrients_applied,
    get_recent_irrigation_by_section,
)
from src.ui.components import render_page_header, render_ai_status, render_safety_warning
from src.ui.state import add_fertilizer_record


def render_fertilizer_records(is_tamil: bool = False, lang: str = "en") -> None:
    """Renders the fertilizer management and nutrient accounting page in pure single-language presentation."""
    current_lang = normalize_lang(lang, is_tamil)

    render_page_header(
        title_en="Fertilizer Identification & Management (Module E)",
        title_ta="உர மேலாண்மை மற்றும் ஊட்டச்சத்து கணக்கீடு (பகுதி E)",
        title_te="ఎరువుల నిర్వహణ మరియు పోషకాల గణన (విభాగం E)",
        subtitle_en="Verify fertilizer formulations, calculate active NPK inputs, and align with horticultural standards",
        subtitle_ta="உரங்களை முறைப்படி சரிபார்த்து, பயிருக்கு கிடைத்த தழை, மணி, சாம்பல் சத்துக்களை கணக்கிடுங்கள்",
        subtitle_te="ఎరువుల ఫార్ములాను సరిచూసి, మొక్కకు అందిన నత్రజని, భాస్వరం, పొటాష్ పోషకాలను లెక్కించండి",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_ai_status(
        phase_description_en="Nutrient Accounting & Formulation Verifier Active. Calculates elemental NPK delivered per bush.",
        desc_ta="ஊட்டச்சத்து கணக்கீடு செயலில் உள்ளது. ஒவ்வொரு செடிக்கும் கிடைத்த சத்துக்கள் கணக்கிடப்படுகின்றன.",
        desc_te="పోషకాల లెక్కింపు సిద్ధంగా ఉంది. ప్రతి మొక్కకు అందిన పోషకాలు ఖచ్చితంగా లెక్కించబడతాయి.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    render_safety_warning(
        message_en="NEVER identify fertilizer solely by package color or shape. Excessive nitrogen produces lush vegetative shoots with fewer flower buds, and causes chemical root burn in dry ground.",
        message_ta="பையின் நிறம் அல்லது வடிவத்தை மட்டும் வைத்து உரத்தை அடையாளம் காணாதீர்கள். அதிக தழைச்சத்து இலை வளர்ச்சியை மட்டுமே கூட்டி பூக்களை குறைத்துவிடும்.",
        message_te="సంచి రంగు లేదా ఆకారాన్ని బట్టి ఎరువులను గుర్తించవద్దు. అధిక నత్రజని ఆకుల ఎదుగుదలనే పెంచి మొగ్గల సంఖ్యను తగ్గిస్తుంది.",
        is_tamil=is_tamil,
        lang=current_lang,
    )

    db_sections = get_garden_sections()
    section_options = get_section_options(current_lang)

    # Fetch custom registered products
    registered_db_products = get_fertilizer_products()
    product_choices = list(STANDARD_FERTILIZER_DATABASE.keys())
    for p in registered_db_products:
        if p["product_name"] not in product_choices:
            product_choices.append(p["product_name"])

    # Tab titles in pure language
    if current_lang == "ta":
        tabs_labels = [
            "📝 1. உரமிடுதல் பதிவு மற்றும் கணக்கீடு",
            "🏷️ 2. உர ஆய்வு மற்றும் லேபிள் பதிவு",
            "📊 3. ஊட்டச்சத்து இருப்பு மற்றும் இலக்கு",
        ]
    elif current_lang == "te":
        tabs_labels = [
            "📝 1. ఎరువుల నమోదు మరియు లెక్కింపు",
            "🏷️ 2. ఎరువుల లేబుల్ తనిఖీ",
            "📊 3. పోషకాల సమతుల్యత మరియు లక్ష్యం",
        ]
    else:
        tabs_labels = [
            "📝 1. Log Application & Calculate NPK",
            "🏷️ 2. Formulation Verifier & Label Entry",
            "📊 3. Seasonal Nutrient Budget",
        ]

    tab_app, tab_verify, tab_budget = st.tabs(tabs_labels)

    # -----------------------------------------------------------------------
    # TAB 1: Log Application & Nutrient Accounting
    # -----------------------------------------------------------------------
    with tab_app:
        col_form, col_calc = st.columns([1, 1])

        with col_form:
            log_title = (
                "உரமிடுதல் பதிவு" if current_lang == "ta"
                else ("ఎరువుల నమోదు" if current_lang == "te"
                else "Log Fertilizer Application Event")
            )
            st.markdown(f"### 📝 {log_title}")

            app_date = st.date_input(t("app_date", current_lang), value=date.today(), max_value=date.today(), key="fa_date")
            chosen_sec_name = st.selectbox(t("garden_section", current_lang), options=section_options, key="fa_sec")
            plant_count = 500
            sec_id = None
            if db_sections and len(db_sections) > 0:
                sec_id = db_sections[0]["id"]
                plant_count = db_sections[0].get("plant_count", 500)

            # Weather Cross-Reference (Rain check)
            recent_irrig = get_recent_irrigation_by_section(sec_id, limit=1)
            forecast_rain = recent_irrig[0].get("forecast_rain_mm", 0.0) if recent_irrig else 0.0
            if forecast_rain >= 15.0:
                rain_warn = (
                    f"🌧️ மழை எச்சரிக்கை: {forecast_rain:.1f} மி.மீ மழை எதிர்பார்க்கப்படுகிறது! உரம் கரைந்து வீணாவதை தடுக்க உரமிடுதலை தள்ளிப்போடுங்கள்." if current_lang == "ta"
                    else (f"🌧️ వర్ష సూచన హెచ్చరిక: {forecast_rain:.1f} మి.మీ వర్షం పడే అవకాశం ఉంది! ఎరువులు కొట్టుకుపోకుండా ఉండటానికి ప్రస్తుతానికి ఆపండి." if current_lang == "te"
                    else f"🌧️ WEATHER HAZARD: {forecast_rain:.1f} mm rain forecasted! Delay granular topdressing to prevent leaching.")
                )
                st.error(rain_warn)

            chosen_product_name = st.selectbox(t("fert_product", current_lang), options=product_choices, key="fa_prod")

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

            analysis_lbl = (
                f"உறுதிப்படுத்தப்பட்ட சத்துக்கள்: **{default_n}% N - {default_p}% P₂O₅ - {default_k}% K₂O**" if current_lang == "ta"
                else (f"ధృవీకరించిన పోషకాలు: **{default_n}% N - {default_p}% P₂O₅ - {default_k}% K₂O**" if current_lang == "te"
                else f"Guaranteed Analysis: **{default_n}% N - {default_p}% P₂O₅ - {default_k}% K₂O**")
            )
            st.caption(analysis_lbl)

            col_q, col_stg = st.columns(2)
            with col_q:
                qty_label = (
                    "அளவு (கிலோகிராம்):" if current_lang == "ta"
                    else ("పరిమాణం (కిలోలు):" if current_lang == "te"
                    else "Quantity Applied (kg):")
                )
                qty_kg = st.number_input(qty_label, min_value=0.5, max_value=2000.0, value=25.0, step=5.0, key="fa_qty")
            with col_stg:
                split_stage = st.selectbox(
                    "பயிர் வளர்ச்சி நிலை:" if current_lang == "ta" else ("పంట దశ:" if current_lang == "te" else "Crop Split Stage:"),
                    options=["flowering_flush", "post_pruning"],
                    format_func=lambda x: (
                        ("பூக்கும் பருவம்" if x == "flowering_flush" else "கவாத்துக்கு பின் அடி உரம்") if current_lang == "ta"
                        else (("పూత సమయం" if x == "flowering_flush" else "కత్తిరింపు తర్వాత ప్రాథమిక ఎరువు") if current_lang == "te"
                        else ("Peak Flowering Flush" if x == "flowering_flush" else "Post-Pruning Basal"))
                    ),
                    key="fa_split",
                )

            method_options = (
                [
                    "செடியைச் சுற்றி வட்டப்பாத்தி அமைத்து மண்ணில் கலக்குதல்",
                    "மேல் உரமாக தூவுதல்",
                    "இலைவழி தெளிப்பு",
                    "சொட்டுநீர் பாசனம் வழி உரம் செலுத்துதல்",
                ] if current_lang == "ta"
                else (
                    [
                        "మొక్క చుట్టూ పాదు తీసి మట్టిలో కలపడం",
                        "పైపాటుగా చల్లడం",
                        "ఆకులపై పిచికారీ",
                        "డ్రిప్ ద్వారా ఎరువుల యాజమాన్యం",
                    ] if current_lang == "te"
                    else [
                        "Ring application around root basin + soil incorporation",
                        "Broadcasting before light hoeing",
                        "Foliar spray",
                        "Fertigation (drip injection)",
                    ]
                )
            )
            method = st.selectbox("இடும் முறை:" if current_lang == "ta" else ("వేసే పద్ధతి:" if current_lang == "te" else "Application Method:"), options=method_options, key="fa_method")

            reason_lbl = "காரணம் / நோக்கம்:" if current_lang == "ta" else ("ఉద్దేశం:" if current_lang == "te" else "Application Purpose:")
            reason = st.text_input(reason_lbl, placeholder="", key="fa_reason")

            rec_btn_lbl = (
                "💾 உரமிடுதலைப் பதிவுசெய்" if current_lang == "ta"
                else ("💾 ఎరువుల వివరాలను భద్రపరచు" if current_lang == "te"
                else "💾 Record Fertilizer Application")
            )
            log_app_btn = st.button(rec_btn_lbl, use_container_width=True, type="primary")

        # Real-time Nutrient Accounting Card
        with col_calc:
            calc_title = (
                "செயலில் உள்ள ஊட்டச்சத்துக்கள் கணக்கீடு" if current_lang == "ta"
                else ("లభించిన పోషకాల లెక్కింపు" if current_lang == "te"
                else "Active Nutrient Input Accounting")
            )
            st.markdown(f"### 📊 {calc_title}")

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
                n_lbl = "தழைச்சத்து (N)" if current_lang == "ta" else ("నత్రజని (N)" if current_lang == "te" else "Delivered N")
                st.metric(n_lbl, f"{deliv['N']:.2f} kg", f"{per_plant['N_g']:.1f} g / bush")
            with c2:
                p_lbl = "மணிச்சத்து (P₂O₅)" if current_lang == "ta" else ("భాస్వరం (P₂O₅)" if current_lang == "te" else "Delivered P₂O₅")
                st.metric(p_lbl, f"{deliv['P2O5']:.2f} kg", f"{per_plant['P2O5_g']:.1f} g / bush")
            with c3:
                k_lbl = "சாம்பல் சத்து (K₂O)" if current_lang == "ta" else ("పొటాష్ (K₂O)" if current_lang == "te" else "Delivered K₂O")
                st.metric(k_lbl, f"{deliv['K2O']:.2f} kg", f"{per_plant['K2O_g']:.1f} g / bush")

            # Evaluate against recommendations
            eval_split = evaluate_jasmine_fertilizer_split(
                n_applied_g_plant=per_plant["N_g"],
                p_applied_g_plant=per_plant["P2O5_g"],
                k_applied_g_plant=per_plant["K2O_g"],
                split_stage=split_stage,
            )

            if eval_split["safety_alerts"]:
                for alert in eval_split["safety_alerts"]:
                    st.error(alert)
            else:
                ok_msg = (
                    "✓ செடிக்கு இட்ட சத்துக்கள் பாதுகாப்பான வரம்பிற்குள் உள்ளன." if current_lang == "ta"
                    else ("✓ ప్రతి మొక్కకు వేసిన మోతాదు సురక్షిత పరిమితుల్లోనే ఉంది." if current_lang == "te"
                    else "✓ Application dose per bush is within safe agronomic thresholds.")
                )
                st.success(ok_msg)

        # Handle Save Event
        if log_app_btn:
            app_id = add_fertilizer_application(
                product_name=chosen_product_name,
                category=default_cat,
                quantity_kg=qty_kg,
                application_date=str(app_date),
                application_method=method,
                section_id=sec_id,
                reason=reason or "Routine application.",
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
            saved_ack = (
                f"✅ உரமிடுதல் பதிவு #{app_id} சேமிக்கப்பட்டது!" if current_lang == "ta"
                else (f"✅ ఎరువుల నమోదు #{app_id} భద్రపరచబడింది!" if current_lang == "te"
                else f"✅ Fertilizer application #{app_id} successfully saved!")
            )
            st.success(saved_ack)
            st.rerun()

    # -----------------------------------------------------------------------
    # TAB 2: Formulation Verifier & Label Entry
    # -----------------------------------------------------------------------
    with tab_verify:
        v_title = (
            "உர ஆய்வு மற்றும் லேபிள் பதிவு" if current_lang == "ta"
            else ("ఎరువుల లేబుల్ తనిఖీ మరియు నమోదు" if current_lang == "te"
            else "Fertilizer Bag Label Verifier & Registry")
        )
        st.markdown(f"### 🏷️ {v_title}")

        with st.form("label_verification_form"):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                p_name_lbl = "வணிகப் பெயர்:" if current_lang == "ta" else ("వాణిజ్య పేరు:" if current_lang == "te" else "Product Trade Name:")
                new_prod_name = st.text_input(p_name_lbl, key="lv_name")
                cat_lbl = "உர வகைப்பாடு:" if current_lang == "ta" else ("వర్గీకరణ:" if current_lang == "te" else "Product Classification:")
                new_category = st.selectbox(cat_lbl, options=FERTILIZER_CATEGORIES, key="lv_cat")
                mfg_lbl = "உற்பத்தியாளர் / நிறுவனம்:" if current_lang == "ta" else ("తయారీదారు:" if current_lang == "te" else "Manufacturer:")
                new_manufacturer = st.text_input(mfg_lbl, key="lv_mfg")
            with col_b2:
                col_n, col_p, col_k = st.columns(3)
                with col_n:
                    input_n = st.number_input("N (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_n")
                with col_p:
                    input_p = st.number_input("P₂O₅ (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_p")
                with col_k:
                    input_k = st.number_input("K₂O (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.5, key="lv_k")

                input_secondary = st.text_input("நுண்ணூட்டச்சத்துக்கள்:" if current_lang == "ta" else ("సూక్ష్మ పోషకాలు:" if current_lang == "te" else "Secondary Nutrients:"), key="lv_sec")

            v_btn_lbl = (
                "🔍 சரிபார்த்து பதிவுசெய்" if current_lang == "ta"
                else ("🔍 తనిఖీ చేసి నమోదు చేయి" if current_lang == "te"
                else "🔍 Verify & Register Formulation")
            )
            verify_submit = st.form_submit_button(v_btn_lbl, use_container_width=True)

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
                    add_fertilizer_product(
                        product_name=new_prod_name,
                        category=new_category,
                        formulation_n=input_n,
                        formulation_p=input_p,
                        formulation_k=input_k,
                        secondary_nutrients=input_secondary,
                        manufacturer=new_manufacturer,
                    )
                    st.success(f"✓ '{new_prod_name}' registered!")
                    st.rerun()

    # -----------------------------------------------------------------------
    # TAB 3: Seasonal Nutrient Budget
    # -----------------------------------------------------------------------
    with tab_budget:
        b_title = (
            "பருவகால மொத்த ஊட்டச்சத்து இருப்பு" if current_lang == "ta"
            else ("సీజన్ వారీగా మొత్తం పోషకాల రికార్డు" if current_lang == "te"
            else "Seasonal Garden Nutrient Budget")
        )
        st.markdown(f"### 📊 {b_title}")

        totals = get_total_nutrients_applied()
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("மொத்த தழைச்சத்து (N)" if current_lang == "ta" else ("మొత్తం నత్రజని (N)" if current_lang == "te" else "Cumulative N"), f"{totals['total_n']:.2f} kg")
        with m2:
            st.metric("மொத்த மணிச்சத்து (P₂O₅)" if current_lang == "ta" else ("మొత్తం భాస్వరం (P₂O₅)" if current_lang == "te" else "Cumulative P₂O₅"), f"{totals['total_p']:.2f} kg")
        with m3:
            st.metric("மொத்த சாம்பல் சத்து (K₂O)" if current_lang == "ta" else ("మొత్తం పొటాష్ (K₂O)" if current_lang == "te" else "Cumulative K₂O"), f"{totals['total_k']:.2f} kg")

        st.markdown("---")
        h_title = (
            "முந்தைய உரமிடுதல் பதிவுகள்" if current_lang == "ta"
            else ("గత ఎరువుల రికార్డులు" if current_lang == "te"
            else "Historic Fertilizer Applications Log")
        )
        st.markdown(f"### 📋 {h_title}")
        all_apps = get_fertilizer_applications()
        if all_apps:
            disp_apps = []
            for a in all_apps:
                disp_apps.append({
                    "Date": a["application_date"],
                    "Section": a.get("section_name") or "Garden",
                    "Product": a["product_name"],
                    "Qty (kg)": a["quantity_kg"],
                    "N (kg)": a["n_supplied_kg"],
                    "P₂O₅ (kg)": a["p_supplied_kg"],
                    "K₂O (kg)": a["k_supplied_kg"],
                    "Method": a["application_method"],
                })
            st.dataframe(pd.DataFrame(disp_apps), use_container_width=True, hide_index=True)
        else:
            st.info("பதிவுகள் எதுவும் இல்லை." if current_lang == "ta" else ("ఇంకా వివరాలు నమోదు కాలేదు." if current_lang == "te" else "No fertilizer applications logged in the database yet."))
