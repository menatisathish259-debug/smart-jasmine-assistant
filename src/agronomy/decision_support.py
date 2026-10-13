"""
Integrated Agronomic Decision Support Engine for Jasminum sambac.
Synthesizes soil test records, irrigation and fertilizer history, weather conditions,
and plant symptoms into actionable, evidence-based field advisories.
"""

from typing import Dict, Any, List, Optional
from datetime import date, datetime


def generate_integrated_agronomic_advisory(
    soil_ph: Optional[float] = None,
    soil_ec: Optional[float] = None,
    soil_texture: Optional[str] = None,
    soil_drainage: Optional[str] = None,
    days_since_irrigation: Optional[int] = None,
    root_moisture_depth_cm: Optional[str] = None,
    temp_c: Optional[float] = None,
    humidity_pct: Optional[float] = None,
    rainfall_today_mm: float = 0.0,
    forecast_rain_mm: float = 0.0,
    cumulative_n_kg: float = 0.0,
    cumulative_p_kg: float = 0.0,
    cumulative_k_kg: float = 0.0,
    plant_count: int = 500,
) -> Dict[str, Any]:
    """
    Generates multi-factor agronomic advisories by synthesizing:
    - Soil chemistry (pH, EC, drainage)
    - Root-zone water balance & irrigation schedule
    - Cumulative nutrient loading vs TNAU targets
    - Weather hazards (heat stress, heavy rainfall forecast)
    """
    advisories = []
    safety_warnings = []
    missing_data_notices = []

    # 1. Weather & Rainfall Interaction with Fertilization
    if forecast_rain_mm >= 15.0 or rainfall_today_mm >= 25.0:
        safety_warnings.append(
            f"🌧️ HEAVY RAINFALL WARNING ({max(forecast_rain_mm, rainfall_today_mm):.1f} mm): "
            "Do NOT apply topdress granular fertilizers (Urea, DAP, MOP) or foliar sprays today. "
            "Heavy rain will cause severe nitrogen leaching into groundwater, fertilizer runoff, and washed-off foliar nutrients."
        )
    elif forecast_rain_mm >= 5.0 and forecast_rain_mm < 15.0:
        advisories.append(
            "Light rain expected (5-15 mm): If applying well-rotted organic manure (FYM/vermicompost), "
            "light rain helps incorporate nutrients into the root zone."
        )

    # 2. Temperature & Heat Stress on Irrigation
    if temp_c is not None:
        if temp_c >= 36.0:
            advisories.append(
                f"☀️ HIGH TEMPERATURE ALERT ({temp_c}°C): Elevated evapotranspiration. "
                "Irrigate strictly in the early morning (6:00 - 8:30 AM) or evening. "
                "Never flood beds during midday heat (11:00 AM - 3:00 PM) to avoid scalding shallow feeder roots."
            )
    else:
        missing_data_notices.append("Daily temperature not logged.")

    # 3. Soil Moisture & Root Zone Irrigation Advisory
    if root_moisture_depth_cm:
        if "Dry and powdery" in root_moisture_depth_cm:
            if forecast_rain_mm < 10.0:
                advisories.append(
                    "💧 ROOT ZONE WATER DEFICIT: Soil at 15-20 cm depth is dry. "
                    "Irrigation is urgently required to maintain bud elongation and prevent premature bud drop."
                )
        elif "Wet and sticky" in root_moisture_depth_cm or "Saturated" in root_moisture_depth_cm:
            safety_warnings.append(
                "⚠️ ROOT ZONE WATERLOGGING: Soil is saturated. Halt all irrigation immediately. "
                "Inspect peripheral channels to ensure stagnant water drains away freely within 2 hours."
            )
    else:
        missing_data_notices.append("Soil moisture at 15-20 cm depth not inspected.")

    if days_since_irrigation is not None:
        if days_since_irrigation >= 7 and rainfall_today_mm == 0 and forecast_rain_mm < 5.0:
            advisories.append(
                f"Days since last irrigation: {days_since_irrigation} days. In jasmine ground culture, "
                "summer irrigation intervals should not exceed 4-6 days to sustain continuous flowering flushes."
            )

    # 4. Soil pH and Micronutrient Chemistry Evaluation
    if soil_ph is not None:
        if soil_ph > 7.5:
            safety_warnings.append(
                f"🧪 ALKALINE / CALCAREOUS SOIL (pH {soil_ph:.1f}): High risk of Iron (Fe) and Zinc (Zn) chlorosis. "
                "Soil-applied iron salts become chemically locked and unavailable. "
                "Agronomic Action: Apply well-rotted Farmyard Manure (FYM) to buffer soil pH, "
                "and use foliar spray of 0.5% FeSO4 + 0.5% ZnSO4 on new flushes if pale yellowing appears."
            )
        elif soil_ph < 6.0:
            safety_warnings.append(
                f"🧪 ACIDIC SOIL (pH {soil_ph:.1f}): Optimal range is 6.0 - 7.0. "
                "Acid soils fix phosphorus, rendering it insoluble, and can induce aluminum toxicity. "
                "Agronomic Action: Submit a representative soil sample to a government soil testing lab "
                "for agricultural lime / dolomite dosage calculation."
            )
        else:
            advisories.append(
                f"✓ Soil pH is optimal ({soil_ph:.1f}) within the ideal 6.0 - 7.0 range for Jasminum sambac. "
                "Nutrient uptake efficiency for N, P, and K is maximized."
            )
    else:
        missing_data_notices.append("Recent soil test pH is missing.")

    # 5. Soil Drainage Evaluation
    if soil_drainage:
        if "poor" in soil_drainage.lower() or "waterlogging" in soil_drainage.lower():
            safety_warnings.append(
                "⚠️ POOR DRAINAGE HAZARD: Jasmine roots are highly sensitive to standing water. "
                "Prolonged saturation (>24-48 hours) predisposes bushes to Collar Rot (Sclerotium rolfsii) "
                "and root-knot nematode multiplication."
            )

    # 6. Cumulative Nutrient Accounting vs TNAU Target
    if plant_count > 0:
        cum_n_g_plant = round((cumulative_n_kg * 1000.0) / plant_count, 1)
        cum_p_g_plant = round((cumulative_p_kg * 1000.0) / plant_count, 1)
        cum_k_g_plant = round((cumulative_k_kg * 1000.0) / plant_count, 1)

        # TNAU Annual Targets: 60g N : 120g P2O5 : 120g K2O per mature bush
        if cum_n_g_plant > 70.0:
            safety_warnings.append(
                f"⚠️ HIGH CUMULATIVE NITROGEN ({cum_n_g_plant} g N/bush vs 60 g annual target): "
                "Stop further nitrogen/urea applications. Excessive nitrogen induces rank vegetative foliage, "
                "reduces flower bud density, causes flower drop, and attracts bud worms."
            )
        elif cum_n_g_plant < 20.0 and cum_n_g_plant > 0:
            advisories.append(
                f"Cumulative nitrogen applied ({cum_n_g_plant} g N/bush) is currently below annual target (60 g). "
                "Maintain planned split dosing during peak flush."
            )

        nutrient_status = {
            "cumulative_delivered_kg": {"N": cumulative_n_kg, "P2O5": cumulative_p_kg, "K2O": cumulative_k_kg},
            "cumulative_g_per_plant": {"N_g": cum_n_g_plant, "P2O5_g": cum_p_g_plant, "K2O_g": cum_k_g_plant},
            "annual_target_g_plant": {"N_g": 60.0, "P2O5_g": 120.0, "K2O_g": 120.0},
        }
    else:
        nutrient_status = {}

    return {
        "status": "ADVISORY_GENERATED",
        "advisories": advisories,
        "safety_warnings": safety_warnings,
        "missing_data_notices": missing_data_notices,
        "nutrient_status": nutrient_status,
        "evidence_sources": [
            "Tamil Nadu Agricultural University (TNAU) Agritech Portal - Floriculture: Jasminum sambac",
            "ICAR Indian Institute of Horticultural Research (IIHR) - Commercial Jasmine Cultivation Manual",
        ],
        "non_prescription_guardrail": (
            "⚠️ REGULATORY & AGRONOMIC SAFEGUARD: This decision support engine provides evidence-based "
            "cultural guidance and nutrient accounting. It NEVER prescribes chemical pesticide doses or "
            "unverified fertilizer applications from photos alone. All nutrient and crop protection measures "
            "must be verified against physical field conditions and approved by local horticulture extension authorities."
        ),
    }
