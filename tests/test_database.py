"""
Unit tests for Phase 3: SQLite Database Schema and CRUD Operations.
Runs against an isolated temporary SQLite database.
"""

import os
from pathlib import Path
from datetime import date
import sqlite3
import pytest

from src.database.connection import init_database, get_db_connection
from src.database import repository


@pytest.fixture
def temp_db(tmp_path) -> Path:
    """Fixture providing an isolated temporary database path."""
    db_file = tmp_path / "test_jasmine.db"
    init_database(db_file)
    return db_file


def test_init_database_creates_tables_and_seeds(temp_db):
    """Verify that all 11 tables and initial seed data are populated."""
    with get_db_connection(temp_db) as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        table_names = {row["name"] for row in tables}

    expected_tables = {
        "farm_profiles",
        "garden_sections",
        "fertilizer_products",
        "fertilizer_applications",
        "soil_tests",
        "irrigation_records",
        "pruning_records",
        "image_labels",
        "plant_observations",
        "harvest_records",
        "recommendations",
    }
    assert expected_tables.issubset(table_names), f"Missing tables: {expected_tables - table_names}"


def test_farm_profile_privacy_and_crud(temp_db):
    """Verify farm profile can be read and updated without storing sensitive GPS coordinates."""
    profile = repository.get_farm_profile(temp_db)
    assert profile is not None
    assert "Family Jasmine Garden" in profile["farm_name"]
    # Ensure no exact GPS coordinate fields exist for privacy
    assert "latitude" not in profile
    assert "longitude" not in profile
    assert "gps" not in profile

    # Update profile
    updated = repository.update_farm_profile(
        farm_id=profile["id"],
        farm_name="Updated Organic Jasmine Plot",
        grower_name="Sathish & Family",
        total_area_acres=0.75,
        notes="Transitioning to organic FYM and vermicompost.",
        db_path=temp_db,
    )
    assert updated is True

    fresh = repository.get_farm_profile(temp_db)
    assert fresh["farm_name"] == "Updated Organic Jasmine Plot"
    assert fresh["total_area_acres"] == 0.75


def test_garden_sections_crud(temp_db):
    """Verify adding and retrieving garden sections."""
    sections = repository.get_garden_sections(temp_db)
    initial_count = len(sections)
    assert initial_count >= 4

    new_id = repository.add_garden_section(
        section_name="Section E (New Cutting Bed)",
        farm_id=1,
        area_acres=0.10,
        plant_count=60,
        planting_year=2024,
        drainage_status="Well-drained",
        notes="Rooted stem cuttings.",
        db_path=temp_db,
    )
    assert new_id > 0

    all_sec = repository.get_garden_sections(temp_db)
    assert len(all_sec) == initial_count + 1


def test_fertilizer_applications_and_nutrient_sum(temp_db):
    """Verify recording fertilizer treatments and summing active nutrients."""
    app_id = repository.add_fertilizer_application(
        product_name="Urea (46% N)",
        category="Nitrogen Fertilizer",
        quantity_kg=50.0,
        application_date=str(date.today()),
        application_method="Ring soil incorporation",
        section_id=1,
        n_supplied_kg=23.0,
        p_supplied_kg=0.0,
        k_supplied_kg=0.0,
        db_path=temp_db,
    )
    assert app_id > 0

    app_id2 = repository.add_fertilizer_application(
        product_name="MOP (60% K2O)",
        category="Potash Fertilizer",
        quantity_kg=20.0,
        application_date=str(date.today()),
        application_method="Soil incorporation",
        section_id=1,
        n_supplied_kg=0.0,
        p_supplied_kg=0.0,
        k_supplied_kg=12.0,
        db_path=temp_db,
    )
    assert app_id2 > 0

    totals = repository.get_total_nutrients_applied(temp_db)
    assert totals["total_n"] == 23.0
    assert totals["total_k"] == 12.0


def test_soil_test_crud_and_constraint(temp_db):
    """Verify soil test recording and pH check constraint."""
    st_id = repository.add_soil_test(
        test_date=str(date.today()),
        sampling_location="North Bed (0-15 cm)",
        ph=6.7,
        texture="Red sandy loam",
        drainage="Well-drained",
        section_id=1,
        db_path=temp_db,
    )
    assert st_id > 0

    records = repository.get_soil_tests(temp_db)
    assert len(records) == 1
    assert records[0]["ph"] == 6.7

    # Test that out-of-range pH triggers SQLite CHECK constraint
    with pytest.raises(sqlite3.IntegrityError):
        repository.add_soil_test(
            test_date=str(date.today()),
            sampling_location="North Bed",
            ph=12.5,  # Violates CHECK(ph >= 3.0 AND ph <= 10.0)
            texture="Clay",
            drainage="Poor",
            section_id=1,
            db_path=temp_db,
        )


def test_harvest_records_crud_and_stage_constraint(temp_db):
    """Verify harvest records creation and valid stage constraint."""
    h_id = repository.add_harvest_record(
        harvest_date=str(date.today()),
        stage="READY_TO_PLUCK",
        quantity=150.0,
        unit="buds",
        section_id=1,
        grade="Premium Grade A",
        db_path=temp_db,
    )
    assert h_id > 0

    harvests = repository.get_harvest_records(temp_db)
    assert len(harvests) == 1
    assert harvests[0]["stage"] == "READY_TO_PLUCK"

    # Test invalid stage constraint
    with pytest.raises(sqlite3.IntegrityError):
        repository.add_harvest_record(
            harvest_date=str(date.today()),
            stage="INVALID_STAGE",
            quantity=50.0,
            section_id=1,
            db_path=temp_db,
        )


def test_irrigation_and_pruning_crud(temp_db):
    """Verify irrigation and pruning logs."""
    irrig_id = repository.add_irrigation_record(
        irrigation_date=str(date.today()),
        was_irrigated=True,
        method="Basin ring irrigation",
        moisture_depth_observation="15 cm moist",
        section_id=1,
        weather_temp_c=32.0,
        humidity_pct=70.0,
        db_path=temp_db,
    )
    assert irrig_id > 0

    prun_id = repository.add_pruning_record(
        pruning_date=str(date.today()),
        pruning_type="Annual Winter Pruning",
        height_cut_cm=35.0,
        section_id=1,
        water_withheld_days=12,
        notes="Pruned back to healthy brown wood; cleared foliage.",
        db_path=temp_db,
    )
    assert prun_id > 0

    assert len(repository.get_irrigation_records(temp_db)) == 1
    assert len(repository.get_pruning_records(temp_db)) == 1


def test_plant_observations_and_recommendations(temp_db):
    """Verify plant observation symptom logging and recommendations storage."""
    obs_id = repository.add_plant_observation(
        observation_date=str(date.today()),
        visible_symptoms="Yellowing leaves, Curled leaves",
        affected_part="Lower mature leaves",
        severity="Mild (<10%)",
        section_id=1,
        suspected_causes="Excessive rain water stagnation",
        status="Under Investigation",
        db_path=temp_db,
    )
    assert obs_id > 0

    rec_id = repository.add_recommendation(
        recommendation_date=str(date.today()),
        category="Soil & Drainage",
        title="Clear drainage furrows after rain",
        observation_basis="Mild yellowing on lower leaves following rain",
        recommended_action="Hoe shallow drainage trenches between rows to avoid root suffocation.",
        supporting_evidence="Jasmine requires aeration; root water stagnation for 24h causes yellowing.",
        section_id=1,
        db_path=temp_db,
    )
    assert rec_id > 0

    assert len(repository.get_plant_observations(temp_db)) == 1
    assert len(repository.get_recommendations(temp_db)) == 1
