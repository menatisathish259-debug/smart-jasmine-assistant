"""
Validation Utilities for Smart Jasmine Farming Assistant.
Validates image uploads, soil pH, fertilizer inputs, and observation entries.
"""

from datetime import date
from typing import Tuple, Dict, Any, Optional
from io import BytesIO
from PIL import Image

from config.settings import SOIL_PH_RANGE, FLOWER_STAGES

# Supported image formats
SUPPORTED_IMAGE_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}
MAX_IMAGE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit for mobile uploads


def validate_image_file(uploaded_file) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates uploaded image file size, integrity, and dimensions.
    Returns (is_valid, error_or_success_message, metadata_dict).
    """
    if uploaded_file is None:
        return False, "No file provided.", {}

    # Size check
    file_bytes = uploaded_file.getvalue()
    size_bytes = len(file_bytes)
    size_mb = size_bytes / (1024 * 1024)

    if size_bytes > MAX_IMAGE_SIZE_BYTES:
        return (
            False,
            f"Image file exceeds maximum limit of 15 MB (File size: {size_mb:.2f} MB).",
            {},
        )

    # PIL verification
    try:
        image = Image.open(BytesIO(file_bytes))
        image.verify()  # Verify integrity
        # Re-open after verify() as verify alters image pointer
        image = Image.open(BytesIO(file_bytes))
        img_format = (image.format or "UNKNOWN").upper()
        width, height = image.size
    except Exception as e:
        return False, f"Corrupted or invalid image file: {str(e)}", {}

    if img_format not in SUPPORTED_IMAGE_FORMATS and img_format != "JPEG":
        return (
            False,
            f"Unsupported format '{img_format}'. Please upload JPG, PNG, or WEBP.",
            {},
        )

    metadata = {
        "filename": uploaded_file.name,
        "format": img_format,
        "width": width,
        "height": height,
        "size_kb": round(size_bytes / 1024, 1),
        "aspect_ratio": round(width / max(height, 1), 2),
    }

    return True, "Image verified successfully.", metadata


def validate_soil_ph(ph: float) -> Tuple[bool, str, str]:
    """
    Validates soil pH reading.
    Returns (is_valid, alert_type ['success', 'warning', 'error'], agronomic_note).
    """
    if ph < 3.0 or ph > 10.0:
        return (
            False,
            "error",
            "Unrealistic soil pH value. Valid agricultural range is 3.0 to 10.0.",
        )

    opt_min = SOIL_PH_RANGE["min_optimal"]
    opt_max = SOIL_PH_RANGE["max_optimal"]

    if opt_min <= ph <= opt_max:
        return (
            True,
            "success",
            f"Optimal pH ({ph:.1f}) for Jasminum sambac. Ideal nutrient availability for flower buds.",
        )
    elif ph < opt_min:
        return (
            True,
            "warning",
            f"Acidic soil ({ph:.1f} < {opt_min}). Iron and aluminum may become toxic, phosphorus availability reduced. Consider lime or dolomite application upon expert confirmation.",
        )
    else:
        return (
            True,
            "warning",
            f"Alkaline soil ({ph:.1f} > {opt_max}). Risk of Iron (Fe), Zinc (Zn), and Boron (B) deficiency causing yellowing leaves and bud dropping. Avoid excess lime; consider gypsum or organic manure.",
        )


def validate_fertilizer_entry(
    product_name: str,
    quantity_kg: float,
    application_date: date,
    area_treated: str,
) -> Tuple[bool, str]:
    """
    Validates fertilizer record inputs.
    Returns (is_valid, error_or_success_message).
    """
    if not product_name or not product_name.strip():
        return False, "Fertilizer product name is required."

    if quantity_kg <= 0:
        return False, "Quantity applied must be greater than 0 kg."

    if quantity_kg > 5000:
        return False, "Quantity exceeds realistic single-application threshold (max 5,000 kg). Please verify."

    if application_date > date.today():
        return False, "Application date cannot be in the future."

    if not area_treated or not area_treated.strip():
        return False, "Garden section / area treated must be specified."

    return True, "Fertilizer record validated."


def validate_harvest_entry(
    stage: str,
    flower_count_or_weight: float,
    record_date: date,
) -> Tuple[bool, str]:
    """
    Validates flower harvest/observation record.
    Returns (is_valid, error_or_success_message).
    """
    if stage not in FLOWER_STAGES:
        return False, f"Invalid flower stage '{stage}'. Must be one of {FLOWER_STAGES}."

    if flower_count_or_weight <= 0:
        return False, "Count or weight must be greater than 0."

    if record_date > date.today():
        return False, "Observation date cannot be in the future."

    return True, "Harvest entry validated."
