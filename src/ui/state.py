"""
Session State Management for Smart Jasmine Farming Assistant.
Maintains in-memory records and state across page navigations in Streamlit.
"""

from datetime import date, timedelta
from typing import List, Dict, Any
import streamlit as st


def init_session_state() -> None:
    """Initializes default session state variables if not already present."""
    if "harvest_records" not in st.session_state:
        # Initial ground-truth staging examples from family garden
        st.session_state.harvest_records = [
            {
                "id": 1,
                "date": str(date.today() - timedelta(days=2)),
                "section": "Section A (North Bed)",
                "stage": "READY_TO_PLUCK",
                "quantity": 120,
                "unit": "buds",
                "notes": "Picked between 6:30 AM and 7:45 AM. Firm white elongated buds.",
                "image_filename": "sample_ready_bud_1.jpg",
            },
            {
                "id": 2,
                "date": str(date.today() - timedelta(days=1)),
                "section": "Section B (South Bed)",
                "stage": "NOT_READY",
                "quantity": 85,
                "unit": "buds",
                "notes": "Tight greenish buds. Retained on bush for next harvest cycle.",
                "image_filename": "sample_not_ready_1.jpg",
            },
        ]

    if "plant_health_records" not in st.session_state:
        st.session_state.plant_health_records = [
            {
                "id": 1,
                "date": str(date.today() - timedelta(days=3)),
                "section": "Section A (North Bed)",
                "visible_symptoms": ["yellowing_leaves"],
                "affected_part": "Older lower leaves",
                "severity": "Mild (5-10% of bush)",
                "suspected_causes": ["Nitrogen deficiency or temporary waterlogging after rain"],
                "confirmed_diagnosis": "Unconfirmed - Monitoring drainage first",
                "status": "Under Investigation",
            }
        ]

    if "fertilizer_records" not in st.session_state:
        st.session_state.fertilizer_records = [
            {
                "id": 1,
                "date": str(date.today() - timedelta(days=14)),
                "section": "Section A & B (Entire Plot - 0.5 acre)",
                "product_name": "Farmyard Manure (FYM)",
                "category": "Organic Manure / FYM",
                "quantity_kg": 250.0,
                "method": "Basal soil incorporation around root zone (15 cm ring)",
                "reason": "Post-pruning basal nutrition enrichment",
                "nutrients_estimated": "Approx. 1.25 kg N, 0.5 kg P2O5, 1.25 kg K2O",
            }
        ]

    if "soil_test_records" not in st.session_state:
        st.session_state.soil_test_records = [
            {
                "id": 1,
                "date": str(date.today() - timedelta(days=30)),
                "location": "Composite sample (0-15 cm depth)",
                "ph": 6.8,
                "texture": "Red sandy loam (செம்மண் மணற்பாங்கான நிலம்)",
                "drainage": "Well-drained, gentle slope",
                "organic_carbon_pct": 0.55,
                "ec_dsm": 0.4,
                "available_n": "Medium (240 kg/ha)",
                "available_p": "Medium (18 kg/ha)",
                "available_k": "High (290 kg/ha)",
                "notes": "Optimal pH 6.8. Good drainage confirmed.",
            }
        ]

    if "weather_irrigation_records" not in st.session_state:
        st.session_state.weather_irrigation_records = [
            {
                "id": 1,
                "date": str(date.today() - timedelta(days=1)),
                "irrigation_done": True,
                "method": "Basin irrigation around pruned bush rings",
                "depth_moisture_cm": "15-20 cm depth moist, no standing water",
                "weather_temp_c": 32.5,
                "humidity_pct": 68.0,
                "rainfall_mm": 0.0,
                "notes": "Irrigated at 5:30 PM after sun cooled down.",
            }
        ]

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"

    if "language" not in st.session_state:
        st.session_state.language = "English"


def add_harvest_record(record: Dict[str, Any]) -> None:
    """Appends a new flower harvest record."""
    record["id"] = len(st.session_state.harvest_records) + 1
    st.session_state.harvest_records.insert(0, record)


def add_health_record(record: Dict[str, Any]) -> None:
    """Appends a new plant health observation record."""
    record["id"] = len(st.session_state.plant_health_records) + 1
    st.session_state.plant_health_records.insert(0, record)


def add_fertilizer_record(record: Dict[str, Any]) -> None:
    """Appends a new fertilizer application record."""
    record["id"] = len(st.session_state.fertilizer_records) + 1
    st.session_state.fertilizer_records.insert(0, record)


def add_soil_record(record: Dict[str, Any]) -> None:
    """Appends a new soil test record."""
    record["id"] = len(st.session_state.soil_test_records) + 1
    st.session_state.soil_test_records.insert(0, record)


def add_weather_irrigation_record(record: Dict[str, Any]) -> None:
    """Appends an irrigation or weather log."""
    record["id"] = len(st.session_state.weather_irrigation_records) + 1
    st.session_state.weather_irrigation_records.insert(0, record)
