"""
SQLite Connection Manager and Initializer for Smart Jasmine Farming Assistant.
Handles ACID transactions, WAL mode, and foreign keys.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from config.settings import DEFAULT_DB_PATH
from src.database.schema import SCHEMA_DDL, PRAGMA_FOREIGN_KEYS, PRAGMA_WAL_MODE
from src.utils.logger import get_logger

logger = get_logger()


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Creates and returns an optimized SQLite connection."""
    target_path = db_path or DEFAULT_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(target_path), timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute(PRAGMA_FOREIGN_KEYS)
    conn.execute(PRAGMA_WAL_MODE)
    return conn


@contextmanager
def get_db_connection(db_path: Optional[Path] = None) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite operations with auto-commit and rollback on error."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error during transaction: {e}")
        raise
    finally:
        conn.close()


def init_database(db_path: Optional[Path] = None) -> None:
    """Initializes tables, indices, and baseline data in the SQLite database."""
    target_path = db_path or DEFAULT_DB_PATH
    logger.info(f"Initializing SQLite database at: {target_path}")

    with get_db_connection(target_path) as conn:
        conn.executescript(SCHEMA_DDL)

    # Seed initial default farm profile & sections if none exist
    _seed_initial_data_if_empty(target_path)
    logger.info("Database initialization completed successfully.")


def _seed_initial_data_if_empty(db_path: Path) -> None:
    """Seeds initial farm profile, standard garden sections, and common fertilizers."""
    with get_db_connection(db_path) as conn:
        # Check farm profile
        cur = conn.execute("SELECT COUNT(*) as cnt FROM farm_profiles")
        if cur.fetchone()["cnt"] == 0:
            conn.execute(
                """
                INSERT INTO farm_profiles (
                    farm_name, grower_name, crop_variety, region_district,
                    total_area_acres, cultivation_method, baseline_soil_type, notes
                ) VALUES (
                    'Family Jasmine Garden', 'Family Grower', 'Jasminum sambac (குண்டு மல்லி)',
                    'Madurai / South Tamil Nadu', 0.5, 'Ground soil cultivation',
                    'Red sandy loam (செம்மண் மணற்பாங்கான நிலம்)',
                    'Family garden cultivated for fresh morning flower harvest and loose flower market.'
                )
                """
            )
            farm_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Seed standard garden sections
            sections = [
                ("Section A (North Bed)", 0.15, 120, 2021, "Well-drained"),
                ("Section B (South Bed)", 0.15, 120, 2021, "Well-drained"),
                ("Section C (East Plot)", 0.10, 80, 2022, "Moderate drainage"),
                ("Section D (West Plot)", 0.10, 80, 2023, "Well-drained"),
            ]
            for s_name, area, count, yr, drain in sections:
                conn.execute(
                    """
                    INSERT INTO garden_sections (
                        farm_id, section_name, area_acres, plant_count,
                        planting_year, drainage_status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (farm_id, s_name, area, count, yr, drain, "Standard cultivated ground bed."),
                )

        # Check fertilizer products
        cur_fert = conn.execute("SELECT COUNT(*) as cnt FROM fertilizer_products")
        if cur_fert.fetchone()["cnt"] == 0:
            standard_products = [
                ("Urea", "Nitrogen Fertilizer", "46-0-0", 46.0, 0.0, 0.0, 0.0, "Standard Brand", "Apply in moist soil ring."),
                ("MOP (Muriate of Potash)", "Potash Fertilizer", "0-0-60", 0.0, 0.0, 60.0, 0.0, "Standard Brand", "Supports flower size and aroma."),
                ("SSP (Single Super Phosphate)", "Phosphate Fertilizer", "0-16-0", 0.0, 16.0, 0.0, 0.0, "Standard Brand", "Apply at root depth for root vigor."),
                ("DAP (Di-Ammonium Phosphate)", "Complex Fertilizer", "18-46-0", 18.0, 46.0, 0.0, 0.0, "Standard Brand", "Pre-flush bud initiation."),
                ("Complex 17:17:17", "NPK Complex", "17-17-17", 17.0, 17.0, 17.0, 0.0, "Standard Brand", "Balanced seasonal nutrition."),
                ("Farmyard Manure (FYM)", "Organic Manure", "0.5-0.2-0.5", 0.5, 0.2, 0.5, 40.0, "On-farm livestock", "Essential post-pruning basal organic matter."),
                ("Vermicompost", "Organic Manure", "1.5-1.0-1.5", 1.5, 1.0, 1.5, 30.0, "Local Farm", "Improves microbial activity and moisture holding."),
                ("Neem Cake", "Organic Soil Amendment", "5-1-1", 5.0, 1.0, 1.0, 60.0, "Local Mill", "Nematode deterrent and slow-release nitrogen."),
            ]
            for name, cat, ratio, n, p, k, om, mfr, inst in standard_products:
                conn.execute(
                    """
                    INSERT INTO fertilizer_products (
                        product_name, category, npk_ratio, n_percent, p_percent,
                        k_percent, organic_matter_percent, manufacturer, label_instructions
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (name, cat, ratio, n, p, k, om, mfr, inst),
                )
