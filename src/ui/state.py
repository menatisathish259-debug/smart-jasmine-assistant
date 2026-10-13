"""
Session State & Database Synchronization for Smart Jasmine Farming Assistant.
Bridges in-memory Streamlit state with the persistent SQLite database.
"""

from typing import Dict, Any
import streamlit as st

from src.database.connection import init_database
from src.database import repository


def init_session_state() -> None:
    """Initializes the database schema and loads records into Streamlit session state."""
    # Ensure database tables exist
    init_database()

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"

    if "language" not in st.session_state:
        st.session_state.language = "English"

    # Load persistent records from SQLite
    refresh_records_from_db()


def refresh_records_from_db() -> None:
    """Reloads all farm records from SQLite into Streamlit session state."""
    st.session_state.farm_profile = repository.get_farm_profile()
    st.session_state.garden_sections = repository.get_garden_sections()
    st.session_state.fertilizer_products = repository.get_fertilizer_products()

    # Normalize records for display
    st.session_state.harvest_records = repository.get_harvest_records()
    st.session_state.plant_health_records = repository.get_plant_observations()
    st.session_state.fertilizer_records = repository.get_fertilizer_applications()
    st.session_state.soil_test_records = repository.get_soil_tests()
    st.session_state.weather_irrigation_records = repository.get_irrigation_records()
    st.session_state.pruning_records = repository.get_pruning_records()
    st.session_state.recommendations = repository.get_recommendations()


def add_harvest_record(record: Dict[str, Any]) -> int:
    """Inserts a harvest record into SQLite and syncs state."""
    new_id = repository.add_harvest_record(
        harvest_date=record["date"],
        stage=record["stage"],
        quantity=float(record["quantity"]),
        unit=record.get("unit", "buds"),
        section_id=record.get("section_id"),
        grade=record.get("grade"),
        time_of_day=record.get("time_of_day", "Morning (6:00 - 8:30 AM)"),
        image_filename=record.get("image_filename"),
        notes=record.get("notes"),
    )
    refresh_records_from_db()
    return new_id


def add_health_record(record: Dict[str, Any]) -> int:
    """Inserts a plant health observation into SQLite and syncs state."""
    symptoms_str = (
        ", ".join(record["visible_symptoms"])
        if isinstance(record.get("visible_symptoms"), list)
        else str(record.get("visible_symptoms", ""))
    )
    causes_str = (
        ", ".join(record["suspected_causes"])
        if isinstance(record.get("suspected_causes"), list)
        else str(record.get("suspected_causes", ""))
    )

    new_id = repository.add_plant_observation(
        observation_date=record["date"],
        visible_symptoms=symptoms_str,
        affected_part=record.get("affected_part", "Whole bush"),
        severity=record.get("severity", "Mild"),
        section_id=record.get("section_id"),
        suspected_causes=causes_str,
        confirmed_diagnosis=record.get("confirmed_diagnosis", "Unconfirmed"),
        status=record.get("status", "Under Investigation"),
        image_filename=record.get("image_filename"),
        notes=record.get("notes"),
    )
    refresh_records_from_db()
    return new_id


def add_fertilizer_record(record: Dict[str, Any]) -> int:
    """Inserts a fertilizer application into SQLite and syncs state."""
    new_id = repository.add_fertilizer_application(
        product_name=record["product_name"],
        category=record["category"],
        quantity_kg=float(record["quantity_kg"]),
        application_date=record["date"],
        application_method=record["method"],
        section_id=record.get("section_id"),
        product_id=record.get("product_id"),
        reason=record.get("reason"),
        n_supplied_kg=float(record.get("n_kg", 0.0)),
        p_supplied_kg=float(record.get("p_kg", 0.0)),
        k_supplied_kg=float(record.get("k_kg", 0.0)),
        label_image_filename=record.get("label_image_filename"),
        notes=record.get("notes"),
    )
    refresh_records_from_db()
    return new_id


def add_soil_record(record: Dict[str, Any]) -> int:
    """Inserts a soil test into SQLite and syncs state."""
    new_id = repository.add_soil_test(
        test_date=record["date"],
        sampling_location=record["location"],
        ph=float(record["ph"]),
        texture=record["texture"],
        drainage=record["drainage"],
        section_id=record.get("section_id"),
        ec_dsm=float(record.get("ec_dsm", 0.4)),
        organic_carbon_pct=float(record.get("organic_carbon_pct", 0.5)),
        available_n=record.get("available_n"),
        available_p=record.get("available_p"),
        available_k=record.get("available_k"),
        micronutrients_status=record.get("micronutrients_status"),
        notes=record.get("notes"),
    )
    refresh_records_from_db()
    return new_id


def add_weather_irrigation_record(record: Dict[str, Any]) -> int:
    """Inserts an irrigation and weather log into SQLite and syncs state."""
    new_id = repository.add_irrigation_record(
        irrigation_date=record["date"],
        was_irrigated=bool(record["irrigation_done"]),
        method=record["method"],
        moisture_depth_observation=record["depth_moisture_cm"],
        section_id=record.get("section_id"),
        duration_minutes=int(record.get("duration_minutes", 45)),
        weather_temp_c=float(record.get("weather_temp_c", 30.0)),
        humidity_pct=float(record.get("humidity_pct", 65.0)),
        rainfall_mm=float(record.get("rainfall_mm", 0.0)),
        forecast_rain_mm=float(record.get("forecast_rain_mm", 0.0)),
        notes=record.get("notes"),
    )
    refresh_records_from_db()
    return new_id
