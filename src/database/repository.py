"""
Data Repository and CRUD Operations for Smart Jasmine Farming Assistant.
Encapsulates all database interactions for farm profiles, sections, treatments, and logs.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from src.database.connection import get_db_connection


# ---------------------------------------------------------------------------
# 1. Farm Profile CRUD
# ---------------------------------------------------------------------------
def get_farm_profile(db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Fetches the active farm profile."""
    with get_db_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM farm_profiles ORDER BY id ASC LIMIT 1").fetchone()
        return dict(row) if row else None


def update_farm_profile(
    farm_id: int,
    farm_name: str,
    grower_name: str,
    total_area_acres: float,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> bool:
    """Updates the active farm profile."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            UPDATE farm_profiles
            SET farm_name = ?, grower_name = ?, total_area_acres = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (farm_name, grower_name, total_area_acres, notes, farm_id),
        )
        return cur.rowcount > 0


# ---------------------------------------------------------------------------
# 2. Garden Sections CRUD
# ---------------------------------------------------------------------------
def get_garden_sections(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all cultivated garden sections."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM garden_sections ORDER BY id ASC").fetchall()
        return [dict(r) for r in rows]


def add_garden_section(
    section_name: str,
    farm_id: int = 1,
    area_acres: float = 0.15,
    plant_count: int = 100,
    planting_year: int = 2022,
    drainage_status: str = "Well-drained",
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Adds a new garden section bed."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO garden_sections (
                farm_id, section_name, area_acres, plant_count, planting_year, drainage_status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (farm_id, section_name, area_acres, plant_count, planting_year, drainage_status, notes),
        )
        return cur.lastrowid


# ---------------------------------------------------------------------------
# 3. Fertilizer Products & Applications CRUD
# ---------------------------------------------------------------------------
def get_fertilizer_products(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all verified fertilizer formulations."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM fertilizer_products ORDER BY product_name ASC").fetchall()
        return [dict(r) for r in rows]


def add_fertilizer_application(
    product_name: str,
    category: str,
    quantity_kg: float,
    application_date: str,
    application_method: str,
    section_id: Optional[int] = None,
    product_id: Optional[int] = None,
    reason: Optional[str] = None,
    n_supplied_kg: float = 0.0,
    p_supplied_kg: float = 0.0,
    k_supplied_kg: float = 0.0,
    label_image_filename: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Records a fertilizer application event."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO fertilizer_applications (
                section_id, product_id, product_name, category, quantity_kg, application_date,
                application_method, reason, n_supplied_kg, p_supplied_kg, k_supplied_kg,
                label_image_filename, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                section_id, product_id, product_name, category, quantity_kg, application_date,
                application_method, reason, n_supplied_kg, p_supplied_kg, k_supplied_kg,
                label_image_filename, notes,
            ),
        )
        return cur.lastrowid


def get_fertilizer_applications(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all fertilizer applications in reverse chronological order."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT f.*, s.section_name
            FROM fertilizer_applications f
            LEFT JOIN garden_sections s ON f.section_id = s.id
            ORDER BY f.application_date DESC, f.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_total_nutrients_applied(db_path: Optional[Path] = None) -> Dict[str, float]:
    """Calculates total kilograms of N, P, K applied across the garden."""
    with get_db_connection(db_path) as conn:
        row = conn.execute(
            """
            SELECT 
                COALESCE(SUM(n_supplied_kg), 0.0) as total_n,
                COALESCE(SUM(p_supplied_kg), 0.0) as total_p,
                COALESCE(SUM(k_supplied_kg), 0.0) as total_k
            FROM fertilizer_applications
            """
        ).fetchone()
        return {
            "total_n": round(row["total_n"], 2),
            "total_p": round(row["total_p"], 2),
            "total_k": round(row["total_k"], 2),
        }


# ---------------------------------------------------------------------------
# 4. Soil Tests CRUD
# ---------------------------------------------------------------------------
def add_soil_test(
    test_date: str,
    sampling_location: str,
    ph: float,
    texture: str,
    drainage: str,
    section_id: Optional[int] = None,
    ec_dsm: float = 0.4,
    organic_carbon_pct: float = 0.5,
    available_n: Optional[str] = None,
    available_p: Optional[str] = None,
    available_k: Optional[str] = None,
    micronutrients_status: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Stores a soil test result."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO soil_tests (
                section_id, test_date, sampling_location, ph, ec_dsm, texture, drainage,
                organic_carbon_pct, available_n, available_p, available_k, micronutrients_status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                section_id, test_date, sampling_location, ph, ec_dsm, texture, drainage,
                organic_carbon_pct, available_n, available_p, available_k, micronutrients_status, notes,
            ),
        )
        return cur.lastrowid


def get_soil_tests(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all soil test records."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT t.*, s.section_name
            FROM soil_tests t
            LEFT JOIN garden_sections s ON t.section_id = s.id
            ORDER BY t.test_date DESC, t.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 5. Irrigation & Pruning CRUD
# ---------------------------------------------------------------------------
def add_irrigation_record(
    irrigation_date: str,
    was_irrigated: bool,
    method: str,
    moisture_depth_observation: str,
    section_id: Optional[int] = None,
    duration_minutes: int = 45,
    weather_temp_c: Optional[float] = None,
    humidity_pct: Optional[float] = None,
    rainfall_mm: float = 0.0,
    forecast_rain_mm: float = 0.0,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Logs an irrigation application or rain event."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO irrigation_records (
                section_id, irrigation_date, was_irrigated, method, moisture_depth_observation,
                duration_minutes, weather_temp_c, humidity_pct, rainfall_mm, forecast_rain_mm, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                section_id, irrigation_date, 1 if was_irrigated else 0, method, moisture_depth_observation,
                duration_minutes, weather_temp_c, humidity_pct, rainfall_mm, forecast_rain_mm, notes,
            ),
        )
        return cur.lastrowid


def get_irrigation_records(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns irrigation and weather history."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT i.*, s.section_name
            FROM irrigation_records i
            LEFT JOIN garden_sections s ON i.section_id = s.id
            ORDER BY i.irrigation_date DESC, i.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def add_pruning_record(
    pruning_date: str,
    pruning_type: str,
    height_cut_cm: float = 35.0,
    section_id: Optional[int] = None,
    defoliation_done: bool = False,
    foliage_cleared: bool = True,
    water_withheld_days: int = 10,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Logs a pruning intervention."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO pruning_records (
                section_id, pruning_date, pruning_type, height_cut_cm, defoliation_done,
                foliage_cleared, water_withheld_days, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                section_id, pruning_date, pruning_type, height_cut_cm,
                1 if defoliation_done else 0, 1 if foliage_cleared else 0, water_withheld_days, notes,
            ),
        )
        return cur.lastrowid


def get_pruning_records(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all pruning records."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT p.*, s.section_name
            FROM pruning_records p
            LEFT JOIN garden_sections s ON p.section_id = s.id
            ORDER BY p.pruning_date DESC, p.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 6. Image Labels CRUD
# ---------------------------------------------------------------------------
def add_image_label(
    filename: str,
    filepath: str,
    label_stage: str,
    image_type: str = "single_bud",
    section_id: Optional[int] = None,
    labeled_by: str = "grower",
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: Optional[str] = None,
    filesize_kb: Optional[float] = None,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Stores ground-truth photograph labels for dataset preparation."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO image_labels (
                filename, filepath, section_id, image_type, label_stage, labeled_by,
                width, height, format, filesize_kb, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (filename, filepath, section_id, image_type, label_stage, labeled_by, width, height, format, filesize_kb, notes),
        )
        return cur.lastrowid


def get_image_labels(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all staged photograph labels."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT l.*, s.section_name
            FROM image_labels l
            LEFT JOIN garden_sections s ON l.section_id = s.id
            ORDER BY l.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 7. Plant Observations CRUD
# ---------------------------------------------------------------------------
def add_plant_observation(
    observation_date: str,
    visible_symptoms: str,
    affected_part: str,
    severity: str,
    section_id: Optional[int] = None,
    suspected_causes: Optional[str] = None,
    confirmed_diagnosis: str = "Unconfirmed",
    status: str = "Under Investigation",
    image_filename: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Logs a field observation of crop symptoms or damage."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO plant_observations (
                section_id, observation_date, visible_symptoms, affected_part, severity,
                suspected_causes, confirmed_diagnosis, status, image_filename, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                section_id, observation_date, visible_symptoms, affected_part, severity,
                suspected_causes, confirmed_diagnosis, status, image_filename, notes,
            ),
        )
        return cur.lastrowid


def get_plant_observations(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all plant health observations."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT o.*, s.section_name
            FROM plant_observations o
            LEFT JOIN garden_sections s ON o.section_id = s.id
            ORDER BY o.observation_date DESC, o.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 8. Harvest Records CRUD
# ---------------------------------------------------------------------------
def add_harvest_record(
    harvest_date: str,
    stage: str,
    quantity: float,
    unit: str = "buds",
    section_id: Optional[int] = None,
    grade: Optional[str] = None,
    time_of_day: str = "Morning (6:00 - 8:30 AM)",
    image_filename: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> int:
    """Records a harvest or staged observation."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO harvest_records (
                section_id, harvest_date, stage, quantity, unit, grade,
                time_of_day, image_filename, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (section_id, harvest_date, stage, quantity, unit, grade, time_of_day, image_filename, notes),
        )
        return cur.lastrowid


def get_harvest_records(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all harvest records in reverse chronological order."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT h.*, s.section_name
            FROM harvest_records h
            LEFT JOIN garden_sections s ON h.section_id = s.id
            ORDER BY h.harvest_date DESC, h.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 9. Recommendations CRUD
# ---------------------------------------------------------------------------
def add_recommendation(
    recommendation_date: str,
    category: str,
    title: str,
    observation_basis: str,
    recommended_action: str,
    supporting_evidence: str,
    section_id: Optional[int] = None,
    status: str = "Active",
    db_path: Optional[Path] = None,
) -> int:
    """Stores an evidence-based recommendation."""
    with get_db_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO recommendations (
                section_id, recommendation_date, category, title, observation_basis,
                recommended_action, supporting_evidence, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (section_id, recommendation_date, category, title, observation_basis, recommended_action, supporting_evidence, status),
        )
        return cur.lastrowid


def get_recommendations(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns all stored recommendations."""
    with get_db_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT r.*, s.section_name
            FROM recommendations r
            LEFT JOIN garden_sections s ON r.section_id = s.id
            ORDER BY r.recommendation_date DESC, r.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]
