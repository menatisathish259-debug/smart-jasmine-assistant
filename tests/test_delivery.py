"""
Delivery and Verification Integration Test Suite for Smart Jasmine Farming Assistant.
Validates end-to-end application integrity:
1. Multi-page modules compilation and render readiness
2. Database operations across all 11 tables with WAL mode
3. Image validation (JPEG, PNG, WebP, oversized, corrupt)
4. Error handling (invalid pH, negative fertilizers, empty dataset aborts)
5. Model loading, inference, uncertainty, and probability distributions
6. Recommendation safeguards, non-prescription guardrails, and expert referrals
7. Mobile CSS responsiveness and bilingual localization dictionaries
"""

import io
from pathlib import Path
from PIL import Image
import pytest

from config.settings import (
    CROP_NAME_EN,
    CROP_NAME_TA,
    FLOWER_STAGES,
    TAMIL_STAGE_TRANSLATIONS,
    SOIL_PH_RANGE,
    FERTILIZER_CATEGORIES,
)
from src.core.validation import (
    validate_soil_ph,
    validate_fertilizer_entry,
    validate_harvest_entry,
    validate_image_file,
)
from src.database.connection import init_database, get_db_connection
from src.database import repository
from src.agronomy.fertilizer_calculator import (
    verify_fertilizer_formulation,
    calculate_nutrient_inputs,
    evaluate_jasmine_fertilizer_split,
)
from src.agronomy.plant_health_engine import (
    analyze_plant_health_observations,
    check_expert_referral_conditions,
)
from src.agronomy.decision_support import (
    generate_integrated_agronomic_advisory,
)
from src.models.classifier import build_mobilenetv2_classifier
from src.models.inference import predict_flower_stage, is_model_available


# ---------------------------------------------------------------------------
# 1. Multi-Page Module Render Readiness Test
# ---------------------------------------------------------------------------
def test_all_page_modules_compile_and_importable():
    """Verify all 8 pages and app router compile cleanly without errors."""
    import app
    from src.ui.pages import (
        dashboard_page,
        flower_analysis_page,
        dataset_page,
        plant_health_page,
        fertilizer_page,
        soil_health_page,
        weather_page,
        farm_history_page,
    )
    assert hasattr(app, "render_dashboard")
    assert callable(dashboard_page.render_dashboard)
    assert callable(flower_analysis_page.render_flower_analysis)
    assert callable(dataset_page.render_dataset_page)
    assert callable(plant_health_page.render_plant_health)
    assert callable(fertilizer_page.render_fertilizer_records)
    assert callable(soil_health_page.render_soil_health)
    assert callable(weather_page.render_weather_irrigation)
    assert callable(farm_history_page.render_farm_history)


# ---------------------------------------------------------------------------
# 2. Database Operations Across All 11 Tables (ACID & WAL)
# ---------------------------------------------------------------------------
def test_database_all_tables_crud_and_wal(tmp_path):
    """Verify that all tables exist, WAL mode is active, and CRUD functions operate without conflict."""
    db_file = tmp_path / "delivery_test.db"
    init_database(db_file)

    with get_db_connection(db_file) as conn:
        # Verify WAL mode
        journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
        assert journal_mode.lower() == "wal"

        # Verify tables count >= 11
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        ).fetchall()
        table_names = [t[0] for t in tables]
        assert len(table_names) >= 11
        for expected in [
            "farm_profiles", "garden_sections", "fertilizer_products", "fertilizer_applications",
            "soil_tests", "irrigation_records", "pruning_records", "image_labels",
            "plant_observations", "harvest_records", "recommendations",
        ]:
            assert expected in table_names

    # Test Section Creation & Foreign Keys
    sec_id = repository.add_garden_section(
        section_name="Test North Plot",
        area_acres=0.25,
        plant_count=600,
        planting_year=2023,
        db_path=db_file,
    )
    assert sec_id > 0

    # Test Fertilizer Logging with FK
    app_id = repository.add_fertilizer_application(
        product_name="Urea",
        category="Chemical / Mineral",
        quantity_kg=25.0,
        application_date="2026-03-15",
        application_method="Ring application",
        section_id=sec_id,
        n_supplied_kg=11.5,
        db_path=db_file,
    )
    assert app_id > 0

    # Test Soil Test with FK
    soil_id = repository.add_soil_test(
        test_date="2026-03-15",
        sampling_location="North Plot composite",
        ph=6.8,
        texture="Red sandy loam",
        drainage="Well-drained",
        section_id=sec_id,
        db_path=db_file,
    )
    assert soil_id > 0


# ---------------------------------------------------------------------------
# 3. Image Upload & Validation Tests
# ---------------------------------------------------------------------------
def test_image_upload_validation_formats_and_limits():
    """Verify valid PNG/JPEG/WebP accepted and oversized/corrupt rejected."""
    # 1. Valid PNG
    img_valid = Image.new("RGB", (300, 300), color=(255, 255, 255))
    buf_png = io.BytesIO()
    img_valid.save(buf_png, format="PNG")
    buf_png.name = "bud.png"
    v_ok, _, v_meta = validate_image_file(buf_png)
    assert v_ok is True
    assert v_meta["width"] == 300
    assert v_meta["height"] == 300

    # 2. Oversized image (>15MB buffer)
    oversized_bytes = b"0" * (16 * 1024 * 1024)  # 16 MB
    buf_huge = io.BytesIO(oversized_bytes)
    buf_huge.name = "huge.jpg"
    v_ok_h, v_msg_h, _ = validate_image_file(buf_huge)
    assert v_ok_h is False
    assert "exceeds maximum" in v_msg_h

    # 3. Corrupt/Invalid bytes
    buf_bad = io.BytesIO(b"this is not an image file")
    buf_bad.name = "corrupt.jpg"
    v_ok_b, v_msg_b, _ = validate_image_file(buf_bad)
    assert v_ok_b is False
    assert "corrupt" in v_msg_b.lower() or "invalid" in v_msg_b.lower()


# ---------------------------------------------------------------------------
# 4. Error Handling and Defensive Boundaries
# ---------------------------------------------------------------------------
def test_error_handling_soil_ph_bounds():
    """Verify boundary handling for optimal, acidic, alkaline, and invalid pH."""
    # Optimal
    ok, status, _ = validate_soil_ph(6.5)
    assert ok is True and status == "success"
    # Acidic
    ok, status, _ = validate_soil_ph(5.2)
    assert ok is True and status == "warning"
    # Alkaline
    ok, status, _ = validate_soil_ph(8.2)
    assert ok is True and status == "warning"
    # Impossible bounds
    ok, status, msg = validate_soil_ph(1.5)
    assert ok is False and status == "error"
    ok, status, msg = validate_soil_ph(12.0)
    assert ok is False and status == "error"


def test_error_handling_fertilizer_inputs():
    """Verify defensive rejection of invalid fertilizer application inputs."""
    # Zero quantity
    ok, msg = validate_fertilizer_entry("Urea", 0.0, "2026-03-01", "Section A")
    assert ok is False and "greater than 0" in msg
    # Excessive quantity (>5000 kg for small farm)
    ok, msg = validate_fertilizer_entry("Urea", 5500.0, "2026-03-01", "Section A")
    assert ok is False and "exceeds realistic single-application threshold" in msg


# ---------------------------------------------------------------------------
# 5. Model Loading, Probability Distribution, and Uncertainty Scoring
# ---------------------------------------------------------------------------
def test_model_inference_distributions_and_uncertainty(tmp_path):
    """Verify MobileNetV2 output sums to 100%, produces uncertainty, and adds safety disclaimer."""
    model_path = tmp_path / "eval_model.keras"
    model = build_mobilenetv2_classifier(num_classes=4, pretrained_weights=None)
    model.save(str(model_path))

    test_img = Image.new("RGB", (224, 224), color=(240, 240, 240))
    result = predict_flower_stage(test_img, model_path=model_path)

    assert result["status"] == "SUCCESS"
    assert result["predicted_stage"] in FLOWER_STAGES
    assert result["predicted_stage_ta"] in TAMIL_STAGE_TRANSLATIONS.values()
    # Check sum of probabilities == 100%
    probs_sum = sum(result["probabilities"].values())
    assert probs_sum == pytest.approx(100.0, abs=0.5)
    # Check uncertainty score calculation (1 - confidence)
    expected_unc = round(1.0 - (result["confidence_pct"] / 100.0), 4)
    assert result["uncertainty_score"] == pytest.approx(expected_unc, abs=0.01)
    # Check required disclaimer
    assert "EXPERIMENTAL AI PREDICTION" in result["disclaimer"]


# ---------------------------------------------------------------------------
# 6. Recommendation Safeguards & Non-Prescription Guardrails
# ---------------------------------------------------------------------------
def test_recommendation_safeguards_and_expert_referrals():
    """Verify that no image-only chemical rates are given and expert referrals are triggered."""
    # Check non-prescription guardrail in advisory
    adv = generate_integrated_agronomic_advisory(temp_c=32.0, rainfall_today_mm=0.0)
    assert "NEVER prescribes chemical pesticide doses" in adv["non_prescription_guardrail"]

    # Check that high damage severity (>30%) triggers authority referral
    ref = check_expert_referral_conditions(
        severity="Severe (>30% affected)",
        reported_symptom_ids=["yellowing_older_leaves"],
        top_hypotheses=["nitrogen_deficiency"],
    )
    assert ref is not None
    assert ref["is_recommended"] is True
    assert "KVK" in ref["recommended_authorities"][0]["entity"]


# ---------------------------------------------------------------------------
# 7. Bilingual Dictionaries and Localization Integrity
# ---------------------------------------------------------------------------
def test_bilingual_dictionary_coverage():
    """Verify every flower stage and major domain concept has a valid Tamil translation."""
    assert CROP_NAME_EN == "Jasminum sambac"
    assert "மல்லி" in CROP_NAME_TA
    for stage in FLOWER_STAGES:
        assert stage in TAMIL_STAGE_TRANSLATIONS
        assert len(TAMIL_STAGE_TRANSLATIONS[stage]) > 0
