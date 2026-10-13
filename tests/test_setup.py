"""
Unit tests for Phase 1: Project structure, settings, and constants.
"""

import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    DB_DIR,
    MODELS_DIR,
    FLOWER_STAGES,
    SOIL_PH_RANGE,
    TAMIL_STAGE_TRANSLATIONS,
)
from src.core.constants import (
    FlowerMaturityStage,
    HARVEST_GUIDANCE,
    VISIBLE_SYMPTOMS,
    STANDARD_FERTILIZER_NPK,
)
from src.utils.logger import get_logger


def test_project_directories_exist():
    """Verify that all core directories are established."""
    assert BASE_DIR.is_dir(), "Base project directory must exist"
    assert DATA_DIR.is_dir(), "data/ directory must exist"
    assert RAW_DATA_DIR.is_dir(), "data/raw/ directory must exist"
    assert PROCESSED_DATA_DIR.is_dir(), "data/processed/ directory must exist"
    assert DB_DIR.is_dir(), "data/db/ directory must exist"
    assert MODELS_DIR.is_dir(), "models/ directory must exist"


def test_flower_stages_configured():
    """Verify flower stages conform to requirements."""
    expected_stages = {
        "READY_TO_PLUCK",
        "NOT_READY",
        "TOO_OPEN",
        "DAMAGED_OR_ABNORMAL",
    }
    assert set(FLOWER_STAGES) == expected_stages
    for stage in expected_stages:
        assert stage in TAMIL_STAGE_TRANSLATIONS
        assert stage in HARVEST_GUIDANCE


def test_harvest_guidance_completeness():
    """Check that each harvest stage includes actionable agricultural guidance."""
    for stage in FlowerMaturityStage:
        guidance = HARVEST_GUIDANCE[stage.value]
        assert "status_title" in guidance
        assert "description" in guidance
        assert "recommended_action" in guidance
        assert len(guidance["recommended_action"]) > 10


def test_soil_ph_parameters():
    """Verify baseline soil pH parameters match jasmine cultivation parameters (6.0 - 7.0)."""
    assert SOIL_PH_RANGE["min_optimal"] == 6.0
    assert SOIL_PH_RANGE["max_optimal"] == 7.0
    assert SOIL_PH_RANGE["min_optimal"] < SOIL_PH_RANGE["max_optimal"]


def test_fertilizer_npk_definitions():
    """Verify common fertilizers have realistic NPK values."""
    assert "Urea" in STANDARD_FERTILIZER_NPK
    assert STANDARD_FERTILIZER_NPK["Urea"]["N"] == 46.0
    assert "MOP (Muriate of Potash)" in STANDARD_FERTILIZER_NPK
    assert STANDARD_FERTILIZER_NPK["MOP (Muriate of Potash)"]["K"] == 60.0


def test_logger_initialization():
    """Verify logging setup initializes cleanly."""
    logger = get_logger()
    assert logger is not None
    assert logger.name == "JasmineAssistant"


def test_streamlit_app_exists_and_compiles():
    """Verify that the entry point app.py exists and compiles without syntax error."""
    app_file = BASE_DIR / "app.py"
    assert app_file.is_file(), "app.py must exist as the Streamlit entrypoint"
    import py_compile
    compiled = py_compile.compile(str(app_file), doraise=True)
    assert compiled is not None, "app.py must be valid Python code"

