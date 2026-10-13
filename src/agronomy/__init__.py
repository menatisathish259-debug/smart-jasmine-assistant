"""
Agronomy and Decision Support Module for Jasminum sambac (Gundu Malli).
Implements verified agricultural guidelines, nutrient calculations, and symptom analysis.
"""

from src.agronomy.fertilizer_calculator import (
    verify_fertilizer_formulation,
    calculate_nutrient_inputs,
    evaluate_jasmine_fertilizer_split,
    STANDARD_FERTILIZER_DATABASE,
)
from src.agronomy.plant_health_engine import (
    analyze_plant_health_observations,
    check_expert_referral_conditions,
    VISIBLE_SYMPTOMS_CATALOG,
    DIFFERENTIAL_DIAGNOSES,
)
from src.agronomy.decision_support import (
    generate_integrated_agronomic_advisory,
)

__all__ = [
    "verify_fertilizer_formulation",
    "calculate_nutrient_inputs",
    "evaluate_jasmine_fertilizer_split",
    "STANDARD_FERTILIZER_DATABASE",
    "analyze_plant_health_observations",
    "check_expert_referral_conditions",
    "VISIBLE_SYMPTOMS_CATALOG",
    "DIFFERENTIAL_DIAGNOSES",
    "generate_integrated_agronomic_advisory",
]
