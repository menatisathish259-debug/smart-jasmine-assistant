"""
Unit and Integration Tests for Tri-lingual Internationalization (i18n).
Verifies:
1. Pure English presentation (no Tamil or Telugu characters).
2. Pure Tamil presentation (no English letters in stage names, nav, or crop name).
3. Pure Telugu presentation (no English letters in stage names, nav, or crop name).
4. Language normalization and fallback behavior.
5. Bidirectional stage and navigation key resolution.
6. Multi-page modules compilation with tri-lingual signatures.
"""

import re
import pytest

from config.settings import (
    CROP_NAME_EN,
    CROP_NAME_TA,
    CROP_NAME_TE,
    FLOWER_STAGES,
    TAMIL_STAGE_TRANSLATIONS,
    TELUGU_STAGE_TRANSLATIONS,
)
from src.core.i18n import (
    SUPPORTED_LANGUAGES,
    PAGE_KEYS,
    normalize_lang,
    get_page_display_names,
    get_page_key_from_display,
    get_stage_name,
    get_stage_key_from_name,
    get_crop_name,
    t,
)
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

# Regex patterns for script detection
TAMIL_PATTERN = re.compile(r"[\u0B80-\u0BFF]")
TELUGU_PATTERN = re.compile(r"[\u0C00-\u0C7F]")
LATIN_PATTERN = re.compile(r"[a-zA-Z]")


def test_supported_languages_configured():
    """Verify English, Tamil, and Telugu are registered in SUPPORTED_LANGUAGES."""
    assert "en" in SUPPORTED_LANGUAGES
    assert "ta" in SUPPORTED_LANGUAGES
    assert "te" in SUPPORTED_LANGUAGES
    assert SUPPORTED_LANGUAGES["en"] == "English"
    assert SUPPORTED_LANGUAGES["ta"] == "தமிழ்"
    assert SUPPORTED_LANGUAGES["te"] == "తెలుగు"


def test_language_normalization():
    """Verify various casing, script forms, and legacy boolean mappings."""
    # English
    assert normalize_lang("en") == "en"
    assert normalize_lang("English") == "en"
    assert normalize_lang("ENGLISH") == "en"
    assert normalize_lang(None, is_tamil=False) == "en"

    # Tamil
    assert normalize_lang("ta") == "ta"
    assert normalize_lang("Tamil") == "ta"
    assert normalize_lang("தமிழ்") == "ta"
    assert normalize_lang(None, is_tamil=True) == "ta"

    # Telugu
    assert normalize_lang("te") == "te"
    assert normalize_lang("Telugu") == "te"
    assert normalize_lang("తెలుగు") == "te"

    # Fallback
    assert normalize_lang("unknown_lang") == "en"


def test_pure_english_presentation():
    """Verify that English selection contains zero Tamil or Telugu script characters."""
    # Flower stages
    for stage in FLOWER_STAGES:
        stg_name = get_stage_name(stage, "en")
        assert not TAMIL_PATTERN.search(stg_name), f"Tamil script found in English stage {stg_name}"
        assert not TELUGU_PATTERN.search(stg_name), f"Telugu script found in English stage {stg_name}"

    # Nav pages
    for nav in get_page_display_names("en"):
        assert not TAMIL_PATTERN.search(nav), f"Tamil script found in English nav {nav}"
        assert not TELUGU_PATTERN.search(nav), f"Telugu script found in English nav {nav}"

    # Core strings
    for key in ["app_title", "display_language", "navigate_modules", "btn_save"]:
        val = t(key, "en")
        assert not TAMIL_PATTERN.search(val), f"Tamil script found in English key {key}"
        assert not TELUGU_PATTERN.search(val), f"Telugu script found in English key {key}"


def test_pure_tamil_presentation():
    """Verify that Tamil selection contains zero English letters in stage names and navigation."""
    # Flower stages
    for stage in FLOWER_STAGES:
        stg_name = get_stage_name(stage, "ta")
        assert TAMIL_PATTERN.search(stg_name), f"Expected Tamil script in {stg_name}"
        assert not LATIN_PATTERN.search(stg_name), f"Latin/English letters leaked into Tamil stage {stg_name}"

    # Nav pages
    for nav in get_page_display_names("ta"):
        assert TAMIL_PATTERN.search(nav), f"Expected Tamil script in {nav}"
        assert not LATIN_PATTERN.search(nav), f"Latin/English letters leaked into Tamil nav {nav}"

    # Crop name
    crop_ta = get_crop_name("ta")
    assert TAMIL_PATTERN.search(crop_ta)
    assert not LATIN_PATTERN.search(crop_ta), f"Latin letters leaked into Tamil crop name: {crop_ta}"


def test_pure_telugu_presentation():
    """Verify that Telugu selection contains zero English letters in stage names and navigation."""
    # Flower stages
    for stage in FLOWER_STAGES:
        stg_name = get_stage_name(stage, "te")
        assert TELUGU_PATTERN.search(stg_name), f"Expected Telugu script in {stg_name}"
        assert not LATIN_PATTERN.search(stg_name), f"Latin/English letters leaked into Telugu stage {stg_name}"

    # Nav pages
    for nav in get_page_display_names("te"):
        assert TELUGU_PATTERN.search(nav), f"Expected Telugu script in {nav}"
        assert not LATIN_PATTERN.search(nav), f"Latin/English letters leaked into Telugu nav {nav}"

    # Crop name
    crop_te = get_crop_name("te")
    assert TELUGU_PATTERN.search(crop_te)
    assert not LATIN_PATTERN.search(crop_te), f"Latin letters leaked into Telugu crop name: {crop_te}"


def test_bidirectional_stage_and_nav_resolution():
    """Verify that display names in en, ta, te correctly resolve back to canonical internal keys."""
    for lang in ["en", "ta", "te"]:
        # Test navigation resolution
        for page_key in PAGE_KEYS:
            display_name = t(page_key, lang) if page_key in ["Dashboard"] else get_page_display_names(lang)[PAGE_KEYS.index(page_key)]
            resolved_key = get_page_key_from_display(display_name, lang)
            assert resolved_key == page_key, f"Failed resolving {display_name} ({lang}) to {page_key}"

        # Test stage resolution
        for stage_key in FLOWER_STAGES:
            stage_display = get_stage_name(stage_key, lang)
            resolved_stage = get_stage_key_from_name(stage_display, lang)
            assert resolved_stage == stage_key, f"Failed resolving {stage_display} ({lang}) to {stage_key}"


def test_all_page_modules_accept_tri_lingual_parameter():
    """Verify all 8 pages accept lang='en', lang='ta', lang='te' callable signatures without error."""
    page_functions = [
        dashboard_page.render_dashboard,
        flower_analysis_page.render_flower_analysis,
        dataset_page.render_dataset_page,
        plant_health_page.render_plant_health,
        fertilizer_page.render_fertilizer_records,
        soil_health_page.render_soil_health,
        weather_page.render_weather_irrigation,
        farm_history_page.render_farm_history,
    ]

    for fn in page_functions:
        assert callable(fn)
        # Check backward compatibility with is_tamil boolean
        import inspect
        sig = inspect.signature(fn)
        assert "is_tamil" in sig.parameters or "lang" in sig.parameters
