"""
Unit tests for Agronomy, Nutrient Calculations, Plant Health Engine, and Decision Support.
Validates TNAU Jasminum sambac standards, non-prescription guardrails, and expert referral rules.
"""

import pytest
from pathlib import Path

from src.agronomy.fertilizer_calculator import (
    verify_fertilizer_formulation,
    calculate_nutrient_inputs,
    evaluate_jasmine_fertilizer_split,
    STANDARD_FERTILIZER_DATABASE,
)
from src.agronomy.plant_health_engine import (
    analyze_plant_health_observations,
    check_expert_referral_conditions,
    VISIBLE_SYMPTOMS_CATALOG,
    DIFFERENTIAL_DIAGNOSES,
)
from src.agronomy.decision_support import (
    generate_integrated_agronomic_advisory,
)
from src.database.connection import init_database
from src.database.repository import (
    add_fertilizer_product,
    get_fertilizer_products,
    add_fertilizer_application,
    get_cumulative_nutrients_by_section,
    add_soil_test,
    get_latest_soil_test_by_section,
    add_plant_observation,
    update_plant_observation_diagnosis,
    get_plant_observations,
)


# ---------------------------------------------------------------------------
# 1. Fertilizer Formulation Verification Tests
# ---------------------------------------------------------------------------
def test_verify_fertilizer_formulation_standard_urea():
    """Verify standard Urea formulation conforms to FCO standards."""
    res = verify_fertilizer_formulation(
        product_name="Urea",
        category="Chemical / Mineral",
        n_pct=46.0,
        p_pct=0.0,
        k_pct=0.0,
    )
    assert res["is_valid"] is True
    assert res["total_active_macro_pct"] == 46.0
    assert len(res["errors"]) == 0


def test_verify_fertilizer_formulation_invalid_bounds():
    """Verify negative and >100% percentages are rejected."""
    # Negative value
    res_neg = verify_fertilizer_formulation("Bad Fertilizer", "Chemical / Mineral", -5.0, 10.0, 10.0)
    assert res_neg["is_valid"] is False
    assert any("negative" in e for e in res_neg["errors"])

    # Exceeding 100% individual
    res_high = verify_fertilizer_formulation("Bad Fertilizer", "Chemical / Mineral", 105.0, 0.0, 0.0)
    assert res_high["is_valid"] is False

    # Total sum exceeding 100%
    res_sum = verify_fertilizer_formulation("Impossible Mix", "Chemical / Mineral", 50.0, 40.0, 30.0)
    assert res_sum["is_valid"] is False
    assert any("exceeds 100%" in e for e in res_sum["errors"])


def test_verify_fertilizer_formulation_known_product_deviation_warning():
    """Verify that entering a non-standard formulation for a known product produces an FCO warning."""
    res = verify_fertilizer_formulation(
        product_name="Urea",
        category="Chemical / Mineral",
        n_pct=25.0,  # Real Urea is 46%
        p_pct=0.0,
        k_pct=0.0,
    )
    assert res["is_valid"] is True
    assert any("differs from standard" in w for w in res["warnings"])


# ---------------------------------------------------------------------------
# 2. Nutrient Input Calculations Tests
# ---------------------------------------------------------------------------
def test_calculate_nutrient_inputs_urea_per_bush():
    """Verify elemental kg and per-bush calculations for 50 kg Urea applied on 500 bushes."""
    res = calculate_nutrient_inputs(
        quantity_kg=50.0,
        n_pct=46.0,
        p_pct=0.0,
        k_pct=0.0,
        plant_count=500,
        area_acres=0.25,
    )
    # 50 kg * 46% = 23.0 kg N
    assert res["nutrients_delivered_kg"]["N"] == 23.0
    assert res["nutrients_delivered_kg"]["P2O5"] == 0.0
    assert res["nutrients_delivered_kg"]["K2O"] == 0.0

    # 23 kg * 1000 / 500 bushes = 46.0 g N / bush
    assert res["per_plant_g"]["N_g"] == 46.0
    # 23 kg / 0.25 acre = 92.0 kg N / acre
    assert res["per_acre_kg"]["N_kg_acre"] == 92.0


def test_calculate_nutrient_inputs_zero_or_negative_raises():
    """Verify error on zero or negative application quantity."""
    with pytest.raises(ValueError):
        calculate_nutrient_inputs(0.0, 17.0, 17.0, 17.0)


# ---------------------------------------------------------------------------
# 3. TNAU Jasmine Split Evaluation Tests
# ---------------------------------------------------------------------------
def test_evaluate_jasmine_fertilizer_split_excess_n_alert():
    """Verify alert when single nitrogen application exceeds 40g N/bush."""
    res = evaluate_jasmine_fertilizer_split(
        n_applied_g_plant=46.0,
        p_applied_g_plant=0.0,
        k_applied_g_plant=20.0,
        split_stage="flowering_flush",
    )
    assert res["is_safe"] is False
    assert any("EXCESS NITROGEN SURGE" in alert for alert in res["safety_alerts"])


def test_evaluate_jasmine_fertilizer_split_balanced_dose():
    """Verify balanced dose passes without safety alerts."""
    res = evaluate_jasmine_fertilizer_split(
        n_applied_g_plant=25.0,
        p_applied_g_plant=0.0,
        k_applied_g_plant=30.0,
        split_stage="flowering_flush",
    )
    assert res["is_safe"] is True
    assert len(res["safety_alerts"]) == 0


# ---------------------------------------------------------------------------
# 4. Plant Health Symptom Observation & Differential Hypotheses Tests
# ---------------------------------------------------------------------------
def test_analyze_plant_health_yellowing_with_high_ph_context():
    """Verify interveinal yellowing with soil pH >= 7.5 ranks Iron Chlorosis highest."""
    res = analyze_plant_health_observations(
        reported_symptom_ids=["yellowing_young_leaves"],
        affected_part="New tender flush",
        severity="Moderate (10-30% affected)",
        soil_ph=7.8,
    )
    assert res["status"] == "ANALYSIS_COMPLETE"
    top_hyp = res["hypotheses"][0]
    assert top_hyp["id"] == "iron_chlorosis"
    assert "Iron" in top_hyp["cause_name_en"]
    assert "சுண்ணாம்பு" in top_hyp["cause_name_ta"]
    # Check that missing information is surfaced
    assert any("pH" in m for m in res["missing_information"]) or any("Foliar" in m for m in res["missing_information"])
    assert "EVIDENCE-BASED AGRICULTURAL SAFETY NOTICE" in res["safety_disclaimer"]


def test_analyze_plant_health_bud_worm_matching():
    """Verify bud bore holes and webbing correctly hypothesize Jasmine Bud Worm."""
    res = analyze_plant_health_observations(
        reported_symptom_ids=["bud_bore_holes", "bud_webbing"],
        affected_part="Flower buds and cymes",
        severity="Moderate (10-30% affected)",
    )
    top_hyp = res["hypotheses"][0]
    assert top_hyp["id"] == "jasmine_bud_worm"
    assert "Hendecasis" in top_hyp["cause_name_en"]
    assert any("frass" in s.lower() for s in top_hyp["supporting_indicators"])
    assert any("razor" in s.lower() for s in top_hyp["verification_steps"])


def test_analyze_plant_health_no_symptoms_handled():
    """Verify engine handles empty symptom input gracefully."""
    res = analyze_plant_health_observations([], "Whole bush", "Mild")
    assert res["status"] == "NO_SYMPTOMS"
    assert len(res["hypotheses"]) == 0


# ---------------------------------------------------------------------------
# 5. Expert Referral Trigger Tests
# ---------------------------------------------------------------------------
def test_expert_referral_triggered_on_severe_damage():
    """Verify referral to KVK / ADH when damage exceeds 30%."""
    ref = check_expert_referral_conditions(
        severity="Severe (>30% affected)",
        reported_symptom_ids=["yellowing_older_leaves"],
        top_hypotheses=["nitrogen_deficiency"],
    )
    assert ref is not None
    assert ref["is_recommended"] is True
    assert "High disease/pest pressure" in ref["reasons"][0]
    assert "sample_collection_protocol" in ref


def test_expert_referral_triggered_on_suspected_collar_rot():
    """Verify referral when sudden branch wilt and collar rot are hypothesized."""
    ref = check_expert_referral_conditions(
        severity="Moderate (10-30% affected)",
        reported_symptom_ids=["stunted_shoots_wilt"],
        top_hypotheses=["root_rot_collar_rot"],
    )
    assert ref is not None
    assert any("collar rot" in r.lower() for r in ref["reasons"])


def test_expert_referral_not_triggered_on_mild_symptoms():
    """Verify mild localized symptoms do not trigger urgent expert referral."""
    ref = check_expert_referral_conditions(
        severity="Mild (<10% affected)",
        reported_symptom_ids=["curled_leaves_downward"],
        top_hypotheses=["thrips"],
    )
    assert ref is None


# ---------------------------------------------------------------------------
# 6. Integrated Agronomic Decision Support Tests
# ---------------------------------------------------------------------------
def test_integrated_advisory_heavy_rain_fertilizer_hazard():
    """Verify heavy rain forecast triggers warning against topdressing granular fertilizer."""
    advisory = generate_integrated_agronomic_advisory(
        forecast_rain_mm=25.0,
        temp_c=31.0,
    )
    assert advisory["status"] == "ADVISORY_GENERATED"
    assert any("HEAVY RAINFALL WARNING" in w for w in advisory["safety_warnings"])
    assert any("leaching" in w for w in advisory["safety_warnings"])


def test_integrated_advisory_heat_stress_irrigation_timing():
    """Verify high daytime heat (>=36°C) advises early morning irrigation only."""
    advisory = generate_integrated_agronomic_advisory(
        temp_c=38.0,
        forecast_rain_mm=0.0,
        root_moisture_depth_cm="Dry and powdery",
    )
    assert any("HIGH TEMPERATURE ALERT" in a for a in advisory["advisories"])
    assert any("early morning" in a.lower() for a in advisory["advisories"])


def test_integrated_advisory_high_nitrogen_threshold():
    """Verify alert when cumulative seasonal nitrogen exceeds 70g N/bush."""
    # 200 kg N across 2000 bushes = 100 g N/bush
    advisory = generate_integrated_agronomic_advisory(
        cumulative_n_kg=200.0,
        plant_count=2000,
    )
    assert any("HIGH CUMULATIVE NITROGEN" in w for w in advisory["safety_warnings"])


# ---------------------------------------------------------------------------
# 7. SQLite Repository Integration Tests
# ---------------------------------------------------------------------------
def test_repository_fertilizer_products_crud(tmp_path):
    """Verify adding custom verified fertilizer formulation and querying it."""
    db_file = tmp_path / "test_agronomy.db"
    init_database(db_file)

    prod_id = add_fertilizer_product(
        product_name="Coromandel Gromor 14-35-14",
        category="Chemical / Mineral",
        formulation_n=14.0,
        formulation_p=35.0,
        formulation_k=14.0,
        secondary_nutrients="None",
        manufacturer="Coromandel International",
        db_path=db_file,
    )
    assert prod_id > 0

    prods = get_fertilizer_products(db_path=db_file)
    names = [p["product_name"] for p in prods]
    assert "Coromandel Gromor 14-35-14" in names


def test_repository_cumulative_nutrients_by_section(tmp_path):
    """Verify cumulative nutrient sum by section."""
    db_file = tmp_path / "test_agronomy.db"
    init_database(db_file)

    # Add 2 applications to section 1
    add_fertilizer_application(
        product_name="Urea",
        category="Chemical / Mineral",
        quantity_kg=50.0,
        application_date="2026-03-01",
        application_method="Ring application",
        section_id=1,
        n_supplied_kg=23.0,
        p_supplied_kg=0.0,
        k_supplied_kg=0.0,
        db_path=db_file,
    )
    add_fertilizer_application(
        product_name="MOP",
        category="Chemical / Mineral",
        quantity_kg=25.0,
        application_date="2026-03-02",
        application_method="Ring application",
        section_id=1,
        n_supplied_kg=0.0,
        p_supplied_kg=0.0,
        k_supplied_kg=15.0,
        db_path=db_file,
    )

    sec1_nutrients = get_cumulative_nutrients_by_section(section_id=1, db_path=db_file)
    assert sec1_nutrients["total_n"] == 23.0
    assert sec1_nutrients["total_p"] == 0.0
    assert sec1_nutrients["total_k"] == 15.0


def test_repository_plant_observation_and_diagnosis_update(tmp_path):
    """Verify adding an observation as unconfirmed and subsequently updating with confirmed diagnosis."""
    db_file = tmp_path / "test_agronomy.db"
    init_database(db_file)

    obs_id = add_plant_observation(
        observation_date="2026-03-10",
        visible_symptoms="Yellowing of older lower leaves",
        affected_part="Older lower leaves",
        severity="Moderate (10-30% affected)",
        section_id=1,
        suspected_causes="Nitrogen Deficiency",
        confirmed_diagnosis="Unconfirmed",
        status="Under Investigation",
        notes="Awaiting soil test report",
        db_path=db_file,
    )
    assert obs_id > 0

    # Lab report arrives: update diagnosis
    ok = update_plant_observation_diagnosis(
        observation_id=obs_id,
        confirmed_diagnosis="Confirmed: Nitrogen Deficiency (Low available N: 180 kg/ha)",
        status="Resolved",
        notes="Applied light vermicompost ring dressing after confirming.",
        db_path=db_file,
    )
    assert ok is True

    obs_list = get_plant_observations(db_path=db_file)
    target = [o for o in obs_list if o["id"] == obs_id][0]
    assert "Confirmed: Nitrogen Deficiency" in target["confirmed_diagnosis"]
    assert target["status"] == "Resolved"
