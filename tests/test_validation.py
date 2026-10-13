"""
Unit tests for input validation, image verification, and session state.
"""

from io import BytesIO
from datetime import date, timedelta
from PIL import Image
import pytest

from src.core.validation import (
    validate_soil_ph,
    validate_fertilizer_entry,
    validate_harvest_entry,
    validate_image_file,
)


class MockUploadedFile:
    """Mock Streamlit UploadedFile object."""
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


def test_validate_soil_ph_optimal():
    """Test optimal pH range 6.0 - 7.0."""
    valid, alert, msg = validate_soil_ph(6.5)
    assert valid is True
    assert alert == "success"
    assert "Optimal" in msg


def test_validate_soil_ph_acidic_and_alkaline():
    """Test warning alerts when outside 6.0 - 7.0."""
    valid_acid, alert_acid, _ = validate_soil_ph(5.5)
    assert valid_acid is True
    assert alert_acid == "warning"

    valid_alk, alert_alk, _ = validate_soil_ph(7.8)
    assert valid_alk is True
    assert alert_alk == "warning"


def test_validate_soil_ph_unrealistic():
    """Test rejection of out-of-bounds pH values."""
    valid_low, alert_low, _ = validate_soil_ph(2.0)
    assert valid_low is False
    assert alert_low == "error"

    valid_high, alert_high, _ = validate_soil_ph(12.5)
    assert valid_high is False
    assert alert_high == "error"


def test_validate_fertilizer_valid():
    """Test valid fertilizer application inputs."""
    valid, msg = validate_fertilizer_entry(
        product_name="Urea (46% N)",
        quantity_kg=25.0,
        application_date=date.today(),
        area_treated="Section A",
    )
    assert valid is True


def test_validate_fertilizer_invalid_inputs():
    """Test invalid fertilizer quantities, names, and future dates."""
    # Blank name
    v1, _ = validate_fertilizer_entry("", 25.0, date.today(), "Section A")
    assert v1 is False

    # Negative quantity
    v2, _ = validate_fertilizer_entry("Urea", -5.0, date.today(), "Section A")
    assert v2 is False

    # Zero quantity
    v3, _ = validate_fertilizer_entry("Urea", 0.0, date.today(), "Section A")
    assert v3 is False

    # Future date
    v4, _ = validate_fertilizer_entry("Urea", 25.0, date.today() + timedelta(days=2), "Section A")
    assert v4 is False


def test_validate_harvest_entry():
    """Test harvest observation validation."""
    valid, _ = validate_harvest_entry("READY_TO_PLUCK", 100, date.today())
    assert valid is True

    # Invalid stage
    inv_stage, _ = validate_harvest_entry("INVALID_STAGE", 100, date.today())
    assert inv_stage is False

    # Zero quantity
    inv_qty, _ = validate_harvest_entry("READY_TO_PLUCK", 0, date.today())
    assert inv_qty is False


def test_validate_image_file_valid_png():
    """Test image upload validation with synthetically generated test image."""
    img = Image.new("RGB", (300, 200), color=(34, 139, 34))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    mock_file = MockUploadedFile("test_jasmine_bud.png", buf.getvalue())
    is_valid, msg, meta = validate_image_file(mock_file)

    assert is_valid is True
    assert meta["width"] == 300
    assert meta["height"] == 200
    assert meta["format"] == "PNG"
    assert meta["size_kb"] > 0


def test_validate_image_file_oversized():
    """Test oversized image file rejection (>15 MB)."""
    large_data = b"0" * (16 * 1024 * 1024)
    mock_file = MockUploadedFile("huge_file.jpg", large_data)
    is_valid, msg, _ = validate_image_file(mock_file)
    assert is_valid is False
    assert "exceeds" in msg
