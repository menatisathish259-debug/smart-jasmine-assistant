"""
Fertilizer Formulations, Label Verification, and Nutrient Input Calculations for Jasminum sambac.
Reference: Tamil Nadu Agricultural University (TNAU) Agritech Portal Floriculture &
Fertilizer (Inorganic, Organic or Mixed) (Control) Order (FCO), Government of India.
"""

from typing import Dict, Any, Optional, Tuple


# Standard Fertilizer Reference Database with FCO Guaranteed Analyses
STANDARD_FERTILIZER_DATABASE: Dict[str, Dict[str, Any]] = {
    "Urea": {
        "category": "Chemical / Mineral",
        "n_pct": 46.0,
        "p_pct": 0.0,
        "k_pct": 0.0,
        "secondary_nutrients": "None",
        "description": "High nitrogen concentrated granular fertilizer. Prone to volatilization and leaching.",
        "fco_standard": True,
    },
    "MOP (Muriate of Potash)": {
        "category": "Chemical / Mineral",
        "n_pct": 0.0,
        "p_pct": 0.0,
        "k_pct": 60.0,
        "secondary_nutrients": "Chloride (Cl-)",
        "description": "Potassium chloride. Essential for bud firming, petal elongation, and drought tolerance.",
        "fco_standard": True,
    },
    "SSP (Single Super Phosphate)": {
        "category": "Chemical / Mineral",
        "n_pct": 0.0,
        "p_pct": 16.0,
        "k_pct": 0.0,
        "secondary_nutrients": "Sulphur (11%), Calcium (19%)",
        "description": "Phosphatic fertilizer with beneficial sulphur and calcium for soil structure.",
        "fco_standard": True,
    },
    "DAP (Di-Ammonium Phosphate)": {
        "category": "Chemical / Mineral",
        "n_pct": 18.0,
        "p_pct": 46.0,
        "k_pct": 0.0,
        "secondary_nutrients": "None",
        "description": "Highly soluble nitrogen and phosphate. Best applied as basal dose in root zone.",
        "fco_standard": True,
    },
    "Complex 17-17-17": {
        "category": "Chemical / Mineral",
        "n_pct": 17.0,
        "p_pct": 17.0,
        "k_pct": 17.0,
        "secondary_nutrients": "None",
        "description": "Balanced granular NPK complex. Commonly applied around jasmine basins.",
        "fco_standard": True,
    },
    "Complex 20-20-0-13S": {
        "category": "Chemical / Mineral",
        "n_pct": 20.0,
        "p_pct": 20.0,
        "k_pct": 0.0,
        "secondary_nutrients": "Sulphur (13%)",
        "description": "Ammonium phosphate sulphate. Excellent sulphur source for essential oil synthesis.",
        "fco_standard": True,
    },
    "Complex 19-19-19 (Water Soluble)": {
        "category": "Chemical / Mineral",
        "n_pct": 19.0,
        "p_pct": 19.0,
        "k_pct": 19.0,
        "secondary_nutrients": "Trace elements",
        "description": "100% water-soluble foliar spray / fertigation fertilizer for quick absorption.",
        "fco_standard": True,
    },
    "Potassium Nitrate (13-0-45)": {
        "category": "Chemical / Mineral",
        "n_pct": 13.0,
        "p_pct": 0.0,
        "k_pct": 45.0,
        "secondary_nutrients": "Nitrate-N",
        "description": "Foliar grade potassium nitrate for spray during flower bud initiation.",
        "fco_standard": True,
    },
    "Farmyard Manure (FYM)": {
        "category": "Organic Manure",
        "n_pct": 0.5,
        "p_pct": 0.2,
        "k_pct": 0.5,
        "secondary_nutrients": "Rich in organic carbon, humic matter, micro-flora",
        "description": "Well-decomposed cattle manure. Essential for soil aeration, water retention, and microbial life.",
        "fco_standard": True,
    },
    "Vermicompost": {
        "category": "Organic Manure",
        "n_pct": 1.5,
        "p_pct": 1.0,
        "k_pct": 1.5,
        "secondary_nutrients": "Micronutrients, earthworm enzymes",
        "description": "Earthworm digested organic matter with high CEC and readily available nutrients.",
        "fco_standard": True,
    },
    "Neem Cake": {
        "category": "Organic Manure",
        "n_pct": 5.0,
        "p_pct": 1.0,
        "k_pct": 1.4,
        "secondary_nutrients": "Azadirachtin (natural nematode and termite repellent)",
        "description": "De-oiled neem seed residue. Inhibits nitrification and protects root zone from root-knot nematodes.",
        "fco_standard": True,
    },
}

# TNAU Recommended Annual Dose per Mature Bearing Bush (Jasminum sambac / Gundu Malli)
# 60 g N : 120 g P2O5 : 120 g K2O / plant / year, plus 10-20 kg FYM / plant / year
TNAU_ANNUAL_DOSE_G_PER_PLANT = {
    "N": 60.0,
    "P": 120.0,
    "K": 120.0,
    "FYM_kg": 15.0,
}


def verify_fertilizer_formulation(
    product_name: str,
    category: str,
    n_pct: float,
    p_pct: float,
    k_pct: float,
    secondary_nutrients: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validates fertilizer guaranteed analysis percentages and formulation plausibility.
    Checks consistency against Fertilizer Control Order (FCO) benchmarks.
    """
    errors = []
    warnings = []

    # 1. Bounds checks
    for elem, val in [("Nitrogen (N)", n_pct), ("Phosphorus (P2O5)", p_pct), ("Potassium (K2O)", k_pct)]:
        if val < 0.0:
            errors.append(f"{elem} percentage cannot be negative (got {val}%).")
        if val > 100.0:
            errors.append(f"{elem} percentage cannot exceed 100% (got {val}%).")

    if errors:
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": warnings,
            "product_name": product_name,
        }

    total_macro = n_pct + p_pct + k_pct
    if total_macro > 100.0:
        errors.append(f"Combined N+P2O5+K2O total is {total_macro:.1f}%, which exceeds 100% physically.")
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": warnings,
            "product_name": product_name,
        }

    # 2. Category plausibility checks
    if "Organic" in category:
        if total_macro > 15.0:
            warnings.append(
                f"Total NPK is {total_macro:.1f}%. Natural organic manures (FYM, compost, cakes) typically contain <12% total NPK. Verify if this is fortified with mineral salts."
            )
    elif "Chemical" in category or "Mineral" in category:
        if total_macro < 5.0 and total_macro > 0:
            warnings.append(
                f"Total NPK of {total_macro:.1f}% is unusually low for commercial mineral fertilizer. Verify label."
            )

    # 3. Known product consistency check
    matched_std = None
    for std_name, std_data in STANDARD_FERTILIZER_DATABASE.items():
        if std_name.lower() in product_name.lower() or product_name.lower() in std_name.lower():
            matched_std = (std_name, std_data)
            break

    if matched_std:
        std_name, std_data = matched_std
        # Check if deviation exceeds 5%
        if abs(n_pct - std_data["n_pct"]) > 5.0 or abs(p_pct - std_data["p_pct"]) > 5.0 or abs(k_pct - std_data["k_pct"]) > 5.0:
            warnings.append(
                f"Formulation differs from standard {std_name} ({std_data['n_pct']}-{std_data['p_pct']}-{std_data['k_pct']}). Please double check your bag's printed Guaranteed Analysis."
            )

    return {
        "is_valid": True,
        "errors": [],
        "warnings": warnings,
        "product_name": product_name,
        "category": category,
        "formulation": {
            "n_pct": round(n_pct, 2),
            "p_pct": round(p_pct, 2),
            "k_pct": round(k_pct, 2),
            "secondary": secondary_nutrients or "None specified",
        },
        "total_active_macro_pct": round(total_macro, 2),
    }


def calculate_nutrient_inputs(
    quantity_kg: float,
    n_pct: float,
    p_pct: float,
    k_pct: float,
    plant_count: Optional[int] = None,
    area_acres: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Calculates active elemental nutrients (N, P2O5, K2O) delivered from a fertilizer application.
    Computes whole-application kilograms, per-plant grams, and per-acre kilograms.
    """
    if quantity_kg <= 0:
        raise ValueError(f"Quantity applied must be positive (got {quantity_kg} kg).")

    # Elemental kilograms delivered
    n_kg = round(quantity_kg * (n_pct / 100.0), 3)
    p_kg = round(quantity_kg * (p_pct / 100.0), 3)
    k_kg = round(quantity_kg * (k_pct / 100.0), 3)

    result: Dict[str, Any] = {
        "quantity_applied_kg": quantity_kg,
        "nutrients_delivered_kg": {
            "N": n_kg,
            "P2O5": p_kg,
            "K2O": k_kg,
        },
    }

    # Per-plant calculations (grams per bush)
    if plant_count and plant_count > 0:
        n_g_plant = round((n_kg * 1000.0) / plant_count, 2)
        p_g_plant = round((p_kg * 1000.0) / plant_count, 2)
        k_g_plant = round((k_kg * 1000.0) / plant_count, 2)
        result["per_plant_g"] = {
            "plant_count": plant_count,
            "N_g": n_g_plant,
            "P2O5_g": p_g_plant,
            "K2O_g": k_g_plant,
        }

    # Per-acre calculations (kg per acre)
    if area_acres and area_acres > 0:
        result["per_acre_kg"] = {
            "area_acres": area_acres,
            "N_kg_acre": round(n_kg / area_acres, 2),
            "P2O5_kg_acre": round(p_kg / area_acres, 2),
            "K2O_kg_acre": round(k_kg / area_acres, 2),
        }

    return result


def evaluate_jasmine_fertilizer_split(
    n_applied_g_plant: float,
    p_applied_g_plant: float,
    k_applied_g_plant: float,
    split_stage: str = "flowering_flush",
) -> Dict[str, Any]:
    """
    Compares applied nutrients per plant against TNAU Jasmine recommendations.
    Provides agronomic warnings against over-fertilization, nitrogen surges, or nutrient imbalances.
    """
    eval_notes = []
    safety_alerts = []

    # Target doses according to TNAU Agritech Floriculture Schedule:
    # 1. Post-Pruning Split (Dec-Jan): 30g N : 120g P2O5 : 60g K2O
    # 2. Flowering Flush Split (Mar-Apr): 30g N : 0g P2O5 : 60g K2O
    if split_stage == "post_pruning":
        target = {"N_g": 30.0, "P2O5_g": 120.0, "K2O_g": 60.0}
        stage_title = "Post-Pruning Basal Split (Dec-Jan)"
    else:
        target = {"N_g": 30.0, "P2O5_g": 0.0, "K2O_g": 60.0}
        stage_title = "Peak Flowering Flush Split (March-April)"

    # Nitrogen Safety Checks
    if n_applied_g_plant > 40.0:
        safety_alerts.append(
            f"⚠️ EXCESS NITROGEN SURGE ({n_applied_g_plant} g N/bush vs ~30 g recommended). "
            "High nitrogen causes excessive tender vegetative shoots, delays bud maturation, causes flower bud fall, "
            "and increases susceptibility to Jasmine Bud Worm (Hendecasis) and Mites."
        )
    elif n_applied_g_plant < 15.0:
        eval_notes.append(f"Nitrogen level ({n_applied_g_plant} g N/bush) is below the full split dose (30 g).")

    # Potassium Balance Checks
    if k_applied_g_plant > 0:
        ratio_nk = round(n_applied_g_plant / max(k_applied_g_plant, 0.1), 2)
        if ratio_nk > 1.5:
            eval_notes.append(
                f"High N:K ratio ({ratio_nk}:1). In jasmine, potassium should balance or exceed nitrogen during flowering to ensure bud firmness."
            )
    else:
        eval_notes.append("No potassium supplied in this application. Potash (MOP) is required for petal strength and fragrance retention.")

    # Phosphorus Placement Notice
    if p_applied_g_plant > 0 and split_stage == "flowering_flush":
        eval_notes.append(
            "Note: TNAU advises applying the entire annual phosphorus quota (120 g P2O5) as a single basal dose during annual winter pruning, because phosphorus has low soil mobility."
        )

    return {
        "split_stage": split_stage,
        "stage_title": stage_title,
        "target_g_plant": target,
        "applied_g_plant": {
            "N_g": n_applied_g_plant,
            "P2O5_g": p_applied_g_plant,
            "K2O_g": k_applied_g_plant,
        },
        "evaluation_notes": eval_notes,
        "safety_alerts": safety_alerts,
        "is_safe": len(safety_alerts) == 0,
        "evidence_source": "TNAU Agritech Portal Floriculture - Jasminum sambac Package of Practices",
    }
