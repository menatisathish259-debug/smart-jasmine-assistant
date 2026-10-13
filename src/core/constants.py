"""
Domain Constants and Evidence-Based Agricultural Guidelines for Jasminum sambac.
Reference: Tamil Nadu Agricultural University (TNAU) Floriculture Guidelines & Local Agronomy.
"""

from enum import Enum
from typing import Dict, Any


class FlowerMaturityStage(str, Enum):
    """Maturity stages for Jasminum sambac flower buds."""
    READY_TO_PLUCK = "READY_TO_PLUCK"
    NOT_READY = "NOT_READY"
    TOO_OPEN = "TOO_OPEN"
    DAMAGED_OR_ABNORMAL = "DAMAGED_OR_ABNORMAL"


# Actionable Harvest Guidance per Stage
HARVEST_GUIDANCE: Dict[str, Dict[str, str]] = {
    FlowerMaturityStage.READY_TO_PLUCK.value: {
        "status_title": "Ready to Pluck / பறிக்கத் தயார்",
        "description": "Firm, unopened white bud with elongated corolla tube. Ideal commercial maturity.",
        "recommended_action": (
            "Pluck early in the morning (6:00 AM - 8:30 AM) with stalk attached. "
            "Keep in shade or moist muslin cloth to retain moisture and shelf life for market sale."
        ),
        "commercial_grade": "Premium Grade A (Highest market value)",
    },
    FlowerMaturityStage.NOT_READY.value: {
        "status_title": "Not Ready / முதிரவில்லை",
        "description": "Small, tight greenish or compact bud. Petals have not reached full length.",
        "recommended_action": (
            "Do not harvest today. Retain on the plant. Re-check in 24 to 48 hours for maturity."
        ),
        "commercial_grade": "Immature (Weight loss & poor opening if picked prematurely)",
    },
    FlowerMaturityStage.TOO_OPEN.value: {
        "status_title": "Over-Open / மலர்ந்துவிட்டது",
        "description": "Flower petals have opened and exposed internal parts. Fragrance volatile oils are dissipating.",
        "recommended_action": (
            "Pick immediately to prevent energy drain on plant. Use for home puja, garlands, or immediate domestic use. "
            "Not suited for long-distance market transport as petals will bruise brown."
        ),
        "commercial_grade": "Grade C / Local Consumption Only",
    },
    FlowerMaturityStage.DAMAGED_OR_ABNORMAL.value: {
        "status_title": "Damaged or Abnormal / சேதமடைந்தது",
        "description": "Bud shows boreholes, brown discoloration, rot, webbed silk, or distorted growth.",
        "recommended_action": (
            "Collect and destroy in a separate container (do not drop in garden soil). "
            "Inspect plant for Jasmine Bud Worm (Hendecasis duplifascialis) or Blossom Midge larvae."
        ),
        "commercial_grade": "Rejected / Non-marketable",
    },
}


# Visible Symptom Reference (Module C & Module H)
VISIBLE_SYMPTOMS: Dict[str, Dict[str, Any]] = {
    "yellowing_leaves": {
        "name_en": "Yellowing Leaves (Chlorosis)",
        "name_ta": "இலைகள் மஞ்சள் நிறமாதல்",
        "observations": "Loss of green chlorophyll in older or newer leaves.",
        "potential_causes": [
            "Nitrogen deficiency (older lower leaves first)",
            "Iron/Zinc deficiency (interveinal yellowing on new leaves)",
            "Waterlogging or poor soil drainage causing root suffocation",
            "Root-knot nematode or collar rot damaging root uptake",
        ],
        "investigation_step": "Check soil moisture depth, drainage condition, and recent fertilizer history before applying chemicals.",
    },
    "curled_leaves": {
        "name_en": "Curled / Distorted Leaves",
        "name_ta": "இலைகள் சுருங்குதல்",
        "observations": "Leaves cupping upwards or downwards, crinkled edges.",
        "potential_causes": [
            "Sap-sucking pests (Thrips or Aphids on undersides of leaves)",
            "Red spider mites (fine webbing under dry, hot weather)",
            "Moisture stress or sudden temperature fluctuation",
        ],
        "investigation_step": "Use a 10x hand lens under leaves to inspect for micro-insects before assuming a viral disease.",
    },
    "bud_dropping": {
        "name_en": "Premature Flower Bud Dropping",
        "name_ta": "மொட்டுக்கள் உதிர்தல்",
        "observations": "Buds turn pale or dry at the stalk base and detach before opening.",
        "potential_causes": [
            "Blossom midge (Contarinia maculipennis) infestation at bud base",
            "Water stress (excessive watering or acute dry spells)",
            "Boron or Calcium micronutrient deficiency",
            "High daytime heat and severe dry winds",
        ],
        "investigation_step": "Split fallen buds longitudinally with a clean razor to check for yellow-orange midge maggots.",
    },
    "low_flowering": {
        "name_en": "Low Flower Count / Reduced Flush",
        "name_ta": "குறைந்த பூ உற்பத்தி",
        "observations": "Bush produces vegetative foliage with few or no flower cymes.",
        "potential_causes": [
            "Excessive nitrogen (Urea) promoting vegetative foliage over flowering",
            "Insufficient direct sunlight (requires minimum 6 hours/day)",
            "Lack of scheduled pruning or pruning at improper season",
            "Inadequate phosphorus and potassium availability during bud initiation",
        ],
        "investigation_step": "Review pruning date, nitrogen application amounts, and daily sunlight hours before adding more fertilizer.",
    },
}


# Standard NPK Values of Common Fertilizers (% N - P2O5 - K2O)
STANDARD_FERTILIZER_NPK: Dict[str, Dict[str, float]] = {
    "Urea": {"N": 46.0, "P": 0.0, "K": 0.0},
    "MOP (Muriate of Potash)": {"N": 0.0, "P": 0.0, "K": 60.0},
    "SSP (Single Super Phosphate)": {"N": 0.0, "P": 16.0, "K": 0.0},
    "DAP (Di-Ammonium Phosphate)": {"N": 18.0, "P": 46.0, "K": 0.0},
    "Complex 17-17-17": {"N": 17.0, "P": 17.0, "K": 17.0},
    "Complex 20-20-0-13S": {"N": 20.0, "P": 20.0, "K": 0.0},
    "Complex 19-19-19 (Water Soluble)": {"N": 19.0, "P": 19.0, "K": 19.0},
    "Potassium Nitrate (13-0-45)": {"N": 13.0, "P": 0.0, "K": 45.0},
    "Farmyard Manure (FYM - average dry)": {"N": 0.5, "P": 0.2, "K": 0.5},
    "Vermicompost (average dry)": {"N": 1.5, "P": 1.0, "K": 1.5},
}
