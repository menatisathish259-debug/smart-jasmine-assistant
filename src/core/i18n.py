"""
Internationalization (i18n) Engine for Smart Jasmine Farming Assistant.
Provides pure, unmixed language presentation for English, Tamil (தமிழ்), and Telugu (తెలుగు).
Ensures that when a language is selected, all UI elements, labels, guidance, and metrics
display exclusively in that language without mixed scripts or bilingual slashes.
"""

from typing import Dict, Any, List, Optional


SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "தமிழ்",
    "te": "తెలుగు",
}

DEFAULT_LANGUAGE = "en"


def normalize_lang(lang: Optional[str] = None, is_tamil: Optional[bool] = None) -> str:
    """Normalizes input language string or legacy boolean to 'en', 'ta', or 'te'."""
    if lang is not None:
        l = str(lang).strip().lower()
        if l in ("ta", "tamil", "தமிழ்"):
            return "ta"
        if l in ("te", "telugu", "తెలుగు"):
            return "te"
        if l in ("en", "english"):
            return "en"
    if is_tamil is True:
        return "ta"
    return DEFAULT_LANGUAGE


# Canonical Navigation Page Keys (Internal Identifiers)
PAGE_KEYS = [
    "Dashboard",
    "Flower Analysis",
    "Dataset and Labeling",
    "Plant Health",
    "Fertilizer Records",
    "Soil Health",
    "Weather and Irrigation",
    "Farm History",
]

# Navigation Page Names in Pure Script
NAV_NAMES: Dict[str, Dict[str, str]] = {
    "en": {
        "Dashboard": "Dashboard",
        "Flower Analysis": "Flower Analysis",
        "Dataset and Labeling": "Dataset and Labeling",
        "Plant Health": "Plant Health",
        "Fertilizer Records": "Fertilizer Records",
        "Soil Health": "Soil Health",
        "Weather and Irrigation": "Weather and Irrigation",
        "Farm History": "Farm History",
    },
    "ta": {
        "Dashboard": "முகப்பு",
        "Flower Analysis": "மலர் பகுப்பாய்வு",
        "Dataset and Labeling": "தரவுத்தொகுப்பு மற்றும் லேபிளிங்",
        "Plant Health": "பயிர் நலம்",
        "Fertilizer Records": "உர பதிவுகள்",
        "Soil Health": "மண் நலம்",
        "Weather and Irrigation": "வானிலை மற்றும் பாசனம்",
        "Farm History": "பண்ணை வரலாறு",
    },
    "te": {
        "Dashboard": "డాష్‌బోర్డ్",
        "Flower Analysis": "పూల విశ్లేషణ",
        "Dataset and Labeling": "డేటాసెట్ మరియు లేబులింగ్",
        "Plant Health": "మొక్కల ఆరోగ్యం",
        "Fertilizer Records": "ఎరువుల రికార్డులు",
        "Soil Health": "నేల ఆరోగ్యం",
        "Weather and Irrigation": "వాతావరణం మరియు నీటిపారుదల",
        "Farm History": "తోట చరిత్ర",
    },
}

# Flower Maturity Stages in Pure Script
STAGE_NAMES: Dict[str, Dict[str, str]] = {
    "en": {
        "READY_TO_PLUCK": "Ready to Pluck",
        "NOT_READY": "Not Ready",
        "TOO_OPEN": "Too Open",
        "DAMAGED_OR_ABNORMAL": "Damaged or Abnormal",
    },
    "ta": {
        "READY_TO_PLUCK": "பறிக்கத் தயார்",
        "NOT_READY": "இன்னும் முதிரவில்லை",
        "TOO_OPEN": "அதிகம் விரிந்தது",
        "DAMAGED_OR_ABNORMAL": "சேதமடைந்தது அல்லது அசாதாரணமானது",
    },
    "te": {
        "READY_TO_PLUCK": "కోతకు సిద్ధం",
        "NOT_READY": "ఇంకా సిద్ధంగా లేదు",
        "TOO_OPEN": "బాగా విచ్చుకుంది",
        "DAMAGED_OR_ABNORMAL": "దెబ్బతిన్నది లేదా అసాధారణం",
    },
}

# Crop Botanical & Common Names
CROP_NAMES: Dict[str, str] = {
    "en": "Jasminum sambac (Jasmine)",
    "ta": "குண்டு மல்லி",
    "te": "గుండు మల్లె",
}

# Garden Sections
SECTION_NAMES: Dict[str, Dict[str, str]] = {
    "en": {
        "sec_a": "Section A (North Bed)",
        "sec_b": "Section B (South Bed)",
        "sec_c": "Section C (East Plot)",
        "sec_d": "Section D (West Plot)",
    },
    "ta": {
        "sec_a": "பாத்தி அ (வடக்கு பாத்தி)",
        "sec_b": "பாத்தி ஆ (தெற்கு பாத்தி)",
        "sec_c": "பாத்தி இ (கிழக்கு பகுதி)",
        "sec_d": "பாத்தி ஈ (மேற்கு பகுதி)",
    },
    "te": {
        "sec_a": "విభాగం ఎ (ఉత్తర మడి)",
        "sec_b": "విభాగం బి (దక్షిణ మడి)",
        "sec_c": "విభాగం సి (తూర్పు పొలం)",
        "sec_d": "విభాగం డి (పడమర పొలం)",
    },
}

# Main Application & Common UI Strings
STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        # General & Sidebar
        "app_title": "Smart Jasmine",
        "app_subtitle": "Jasmine Farming Assistant",
        "display_language": "Display Language",
        "navigate_modules": "Navigate Modules",
        "garden_context_title": "Garden Profile",
        "garden_crop": "Crop",
        "cultivation_method": "Cultivation Method",
        "cultivation_val": "Ground Soil Cultivation",
        "target_ph": "Target pH",
        "system_status": "System Status",
        "active": "Active",
        "agricultural_safety_notice": "Agricultural Safety Notice",
        "ai_status": "AI Status",
        "quick_nav": "Quick Navigation",
        "recent_activity": "Recent Activity",

        # Actions & Buttons
        "btn_save": "Save Record",
        "btn_submit": "Submit Inspection",
        "btn_export_csv": "Export Records (CSV)",
        "btn_run_ai": "Run AI Maturity Prediction",
        "btn_audit_dupes": "Run Perceptual Duplicate Audit",
        "btn_generate_splits": "Generate Train / Val / Test Splits",
        "btn_train_model": "Launch Training Pipeline",
        "btn_calculate": "Calculate Active Nutrients",
        "btn_verify_label": "Verify Formulation Integrity",

        # Dashboard Page
        "dash_title": "Jasmine Garden Dashboard",
        "dash_sub": "Real-time farm overview, harvest readiness, and crop management tasks",
        "dash_ai_desc": "System Active. Data entry and agronomic validation verified.",
        "kpi_harvests": "Harvest Observations",
        "kpi_health": "Health Observations",
        "kpi_fertilizers": "Fertilizer Inputs",
        "kpi_soil": "Soil Test Records",
        "sub_staged": "Staged records",
        "sub_investigation": "Under investigation",
        "sub_applications": "Active applications",
        "profile_plot_size": "Plot Size: Approximately 0.25 to 1.0 Acre",
        "profile_pruning": "Pruning Cycle: Annual winter pruning (Late Nov - Dec) for spring-summer flush",
        "profile_sunlight": "Sunlight Exposure: Full Sun (Min. 6 hours direct daily)",
        "profile_watering": "Watering Strategy: Avoid waterlogging; check 15 cm soil depth before irrigation",
        "field_checklist_title": "Daily Jasmine Field Checklist",
        "checklist_1_title": "1. Morning Plucking Window",
        "checklist_1_desc": "Harvest between 6:00 AM and 8:30 AM before direct sunlight opens petals and evaporates volatile fragrance oils.",
        "checklist_2_title": "2. Premature Bud Drop Inspection",
        "checklist_2_desc": "Inspect bushes for fallen buds. Split a fallen bud with a blade to check for yellow-orange blossom midge maggots.",
        "checklist_3_title": "3. Moisture & Drainage Check",
        "checklist_3_desc": "Check soil at 15–20 cm depth. Jasmine roots suffocate quickly in waterlogged soil.",
        "checklist_4_title": "4. Leaf Underside Scouting",
        "checklist_4_desc": "Check tender flush undersides for thrips or tiny webbing before assuming nutrient deficiency.",
        "latest_harvest": "Latest Harvest Observation",
        "latest_fertilizer": "Latest Fertilizer Application",

        # Flower Analysis Page
        "flower_title": "Flower Maturity Analysis",
        "flower_sub": "Examine bud maturity, verify harvest readiness, and stage photographs",
        "flower_ai_desc": "Dataset Staging Phase. Grower labeling serves as ground truth.",
        "flower_safety": "Do not rely on unvalidated computer models for harvest decisions. The grower's experienced judgment is the ground truth.",
        "upload_bud_photo": "Upload Bud Photograph",
        "upload_bud_prompt": "Choose a close-up jasmine bud photograph (JPG, PNG, WEBP):",
        "upload_help": "Take clear photographs in morning daylight for best evaluation.",
        "grower_assessment": "Grower Assessment & Ground Truth",
        "grower_caption": "Record your harvest judgment to build the verified dataset for training.",
        "maturity_stage": "Maturity Stage",
        "garden_section": "Garden Section",
        "harvest_quantity": "Estimated Quantity",
        "harvest_unit": "Unit",
        "kg": "Kilograms (kg)",
        "grams": "Grams (g)",
        "buds_count": "Bud Count",
        "notes": "Field Notes & Observations",
        "notes_placeholder": "e.g., Morning harvest from rows 1-4, healthy white buds",
        "save_observation": "Save Harvest Observation",
        "harvest_guidance_title": "Botanical Harvest Guidance",
        "ai_prediction_box": "Experimental AI Inspection",
        "predicted_stage": "Predicted Stage",
        "confidence": "Model Confidence",
        "uncertainty": "Uncertainty Score",
        "prob_dist": "View Probability Distribution",

        # Dataset & Labeling Page
        "dataset_title": "Dataset Organization & Labeling Workflow",
        "dataset_sub": "Curate the jasmine dataset, detect duplicates, and generate leak-free training splits",
        "dataset_ai_desc": "Dataset Curation Phase. Whole-plant photos are segregated. Small dataset warnings strictly enforced.",
        "dataset_safety": "Do not claim that a small starter dataset is sufficient for training a reliable model. Gather diverse photos across morning lighting, varying bush ages, and damage types.",
        "tab_labeling": "Image Labeling",
        "tab_duplicates": "Duplicate Audit",
        "tab_splits": "Train / Val / Test Splits",
        "tab_training": "Model Training & Eval",
        "tab_guidelines": "Field Photography Guide",
        "tab_whole_plant": "Whole-Plant Holding",

        # Plant Health Page
        "health_title": "Plant Health & Damage Observations",
        "health_sub": "Record visible crop abnormalities while strictly separating physical observations from confirmed diagnoses",
        "health_ai_desc": "Evidence-Based Diagnostic Engine Active. Separates visible symptoms from inferred causes.",
        "health_safety": "NEVER prescribe chemical pesticides or fertilizer rates based solely on photographs. Always verify root depth moisture, check underleaf pests with a 10x lens, test soil pH, and seek local extension advice.",
        "tab_log_symptoms": "Log Symptoms & Analyze",
        "tab_obs_history": "Observation History & Confirmation",
        "tab_scout_guide": "Scientific Scouting Guide",
        "obs_date": "Observation Date",
        "visible_symptoms_header": "Visible Physical Symptoms Checklist",
        "affected_part": "Primary Affected Part",
        "damage_severity": "Damage Severity",
        "new_flush": "New tender flush",
        "older_leaves": "Older lower leaves",
        "flower_buds": "Flower buds and cymes",
        "entire_bush": "Entire branch or whole bush",
        "mild": "Mild (<10% affected)",
        "moderate": "Moderate (10-30% affected)",
        "severe": "Severe (>30% affected)",
        "diagnostic_hypotheses": "Differential Diagnostic Hypotheses",
        "missing_info": "Missing Information Required Before Confirmation",
        "confirm_diagnosis": "Confirm Final Diagnosis",

        # Fertilizer Page
        "fert_title": "Fertilizer Identification & Management",
        "fert_sub": "Verify fertilizer formulations, calculate active NPK inputs, and align with horticultural standards",
        "fert_ai_desc": "Nutrient Accounting & Formulation Verifier Active. Calculates elemental NPK delivered per bush.",
        "fert_safety": "NEVER identify fertilizer solely by package color or shape. Excessive nitrogen produces lush vegetative shoots with fewer flower buds, and causes chemical root burn in dry ground.",
        "tab_log_fert": "Log Application & Calculate NPK",
        "tab_verify_fert": "Formulation Verifier & Label Entry",
        "tab_budget_fert": "Seasonal Nutrient Budget",
        "app_date": "Application Date",
        "fert_product": "Fertilizer Product",
        "quantity_kg": "Total Quantity Applied (kg)",
        "active_nutrients_delivered": "Active Nutrients Delivered",

        # Soil Health Page
        "soil_title": "Soil Health & Nutrient Analysis",
        "soil_sub": "Track soil test reports, evaluate pH constraints (6.0-7.0), and assess drainage conditions",
        "soil_ai_desc": "Soil Rule Engine Active. Target pH range (6.0-7.0) based on horticultural standards.",
        "soil_safety": "Sandy loam is not the only suitable soil; well-drained red loams and clay loams with ample organic matter are also productive. Never guess missing nutrient figures; verify with an official soil test laboratory.",
        "test_date": "Test Date",
        "sample_location": "Sampling Depth & Location",
        "soil_ph": "Soil pH",
        "soil_ec": "Electrical Conductivity (EC dS/m)",
        "organic_carbon": "Organic Carbon (%)",
        "avail_n": "Available Nitrogen (kg/ha)",
        "avail_p": "Available Phosphorus (kg/ha)",
        "avail_k": "Available Potassium (kg/ha)",
        "soil_texture": "Soil Texture & Drainage",

        # Weather Page
        "weather_title": "Weather & Irrigation Tracking",
        "weather_sub": "Track temperature, rainfall, and root-zone moisture to optimize irrigation and fertilization timing",
        "weather_ai_desc": "Field Observation & Advisory Active. Cross-references climatic data with soil moisture and fertilizer safety rules.",
        "weather_safety": "Do not determine irrigation requirements or diagnose disease from weather data alone. Always verify soil moisture at 15–30 cm root depth before running irrigation.",
        "day_temp": "Day Temperature (°C)",
        "rel_humidity": "Relative Humidity (%)",
        "rainfall_today": "Rainfall Today (mm)",
        "rainfall_forecast": "Forecast 24h Rain (mm)",
        "irrig_applied": "Irrigation Applied Today",
        "irrig_method": "Irrigation Method",
        "soil_moisture_level": "Soil Moisture Condition",

        # Farm History Page
        "history_title": "Farm History & Integrated Logs",
        "history_sub": "Review chronological farm management logs, inspect trends, and export dataset records",
        "history_ai_desc": "Persistent Database Active. All records saved in ACID-compliant tables.",
    },

    "ta": {
        # General & Sidebar
        "app_title": "ஸ்மார்ட் மல்லி",
        "app_subtitle": "மல்லி விவசாய உதவியாளர்",
        "display_language": "காட்சி மொழி",
        "navigate_modules": "பகுதிகள்",
        "garden_context_title": "தோட்ட விபரம்",
        "garden_crop": "பயிர்",
        "cultivation_method": "பயிரிடும் முறை",
        "cultivation_val": "தரை மண் பயிரிடுதல்",
        "target_ph": "இலக்கு கார அமில நிலை",
        "system_status": "அமைப்பின் நிலை",
        "active": "செயலில் உள்ளது",
        "agricultural_safety_notice": "விவசாய பாதுகாப்பு அறிவிப்பு",
        "ai_status": "செயற்கை நுண்ணறிவு நிலை",
        "quick_nav": "விரைவுச் செல்",
        "recent_activity": "சமீபத்திய பதிவுகள்",

        # Actions & Buttons
        "btn_save": "பதிவைச் சேமி",
        "btn_submit": "ஆய்வைச் சமர்ப்பி",
        "btn_export_csv": "பதிவுகளைப் பதிவிறக்கு",
        "btn_run_ai": "கணிப்பை இயக்கு",
        "btn_audit_dupes": "நகல்கள் தணிக்கை",
        "btn_generate_splits": "தரவுப் பிரிவுகளை உருவாக்கு",
        "btn_train_model": "பயிற்சியைத் தொடங்கு",
        "btn_calculate": "ஊட்டச்சத்தை கணக்கிடு",
        "btn_verify_label": "உரத்தை சரிபார்",

        # Dashboard Page
        "dash_title": "மல்லி பண்ணை முகப்பு",
        "dash_sub": "நிகழ்நேர தோட்ட மேற்பார்வை, அறுவடை நிலவரம் மற்றும் பயிர் மேலாண்மை பணிகள்",
        "dash_ai_desc": "அமைப்பு செயலில் உள்ளது. களத் தரவு மற்றும் வேளாண் விதிகள் சரிபார்க்கப்பட்டன.",
        "kpi_harvests": "அறுவடை ஆய்வுகள்",
        "kpi_health": "பயிர் நலம்",
        "kpi_fertilizers": "உரமிடுதல்",
        "kpi_soil": "மண் பரிசோதனைகள்",
        "sub_staged": "பதிவான பதிவுகள்",
        "sub_investigation": "ஆய்வில் உள்ளவை",
        "sub_applications": "செயலில் உள்ள உரங்கள்",
        "profile_plot_size": "நில அளவு: சுமார் கால் முதல் ஒரு ஏக்கர் வரை",
        "profile_pruning": "கவாத்து சுழற்சி: நவம்பர் இறுதி முதல் டிசம்பர் வரை வருடாந்திர குளிர் கால கவாத்து",
        "profile_sunlight": "சூரிய ஒளி: தினமும் குறைந்தது ஆறு மணி நேரம் நேரடி வெயில்",
        "profile_watering": "பாசன உத்தி: நீர் தேங்குவதை தவிர்த்து பதினைந்து சென்டிமீட்டர் ஆழ ஈரப்பதம் பார்த்து நீர் பாய்ச்சவும்",
        "field_checklist_title": "தினசரி மல்லி தோட்ட சரிபார்ப்பு",
        "checklist_1_title": "1. காலை அறுவடை நேரம்",
        "checklist_1_desc": "சூரிய வெப்பத்தால் இதழ்கள் விரிந்து நறுமண எண்ணெய் ஆவியாவதற்கு முன் காலை ஆறு முதல் எட்டரை மணிக்குள் பறிக்கவும்.",
        "checklist_2_title": "2. உதிர்ந்த மொட்டுகள் ஆய்வு",
        "checklist_2_desc": "செடியின் அடியில் உதிர்ந்த மொட்டுகளை பிளந்து பார்த்து மஞ்சள்-ஆரஞ்சு மொட்டு ஈ புழுக்கள் உள்ளதா என கவனிக்கவும்.",
        "checklist_3_title": "3. ஈரப்பதம் மற்றும் வடிகால்",
        "checklist_3_desc": "பதினைந்து முதல் இருபது சென்டிமீட்டர் ஆழத்தில் மண்ணை சோதிக்கவும். நீர் தேங்கினால் வேர்கள் மூச்சுத்திணறும்.",
        "checklist_4_title": "4. இலைக்கு அடியில் ஆய்வு",
        "checklist_4_desc": "இளந்தளிர்களின் அடிப்பகுதியில் இலைப்பேன் அல்லது வலைப்பின்னல் உள்ளதா என பார்த்த பின்பே சத்துக்குறைபாட்டை தீர்மானிக்கவும்.",
        "latest_harvest": "சமீபத்திய அறுவடை பதிவு",
        "latest_fertilizer": "சமீபத்திய உரமிடுதல் பதிவு",

        # Flower Analysis Page
        "flower_title": "மலர் முதிர்ச்சி பகுப்பாய்வு",
        "flower_sub": "மொட்டு முதிர்ச்சியை ஆராயவும், அறுவடை நிலையை உறுதிப்படுத்தவும், புகைப்படங்களை சேமிக்கவும்",
        "flower_ai_desc": "தரவு சேகரிப்பு நிலை. விவசாயியின் மதிப்பீடே முதன்மை உண்மை.",
        "flower_safety": "சரிபார்க்கப்படாத மாதிரிகளை நம்ப வேண்டாம். விவசாயியின் கள அனுபவமே இந்த அமைப்பின் முதன்மை உண்மை.",
        "upload_bud_photo": "மொட்டு புகைப்படம் பதிவேற்றுக",
        "upload_bud_prompt": "அருகில் எடுத்த மல்லி மொட்டு புகைப்படத்தை தேர்ந்தெடுக்கவும்:",
        "upload_help": "காலை வெளிச்சத்தில் தெளிவான புகைப்படங்களை எடுக்கவும்.",
        "grower_assessment": "விவசாயியின் கள மதிப்பீடு",
        "grower_caption": "பயிற்சிக்கு பயன்படும் வகையில் உங்கள் அறுவடை முடிவை பதிவுசெய்யவும்.",
        "maturity_stage": "முதிர்ச்சி நிலை",
        "garden_section": "தோட்டப் பாத்தி",
        "harvest_quantity": "தோராயமான அளவு",
        "harvest_unit": "அளவீடு",
        "kg": "கிலோகிராம்",
        "grams": "கிராம்",
        "buds_count": "மொட்டுகளின் எண்ணிக்கை",
        "notes": "களக் குறிப்புகள் மற்றும் அவதானிப்புகள்",
        "notes_placeholder": "எடுத்துக்காட்டு: காலை அறுவடை, தரமான வெள்ளை மொட்டுகள்",
        "save_observation": "அறுவடைப் பதிவைச் சேமிக்கவும்",
        "harvest_guidance_title": "தாவரவியல் அறுவடை வழிகாட்டுதல்",
        "ai_prediction_box": "செயற்கை நுண்ணறிவு ஆய்வு",
        "predicted_stage": "கணிக்கப்பட்ட நிலை",
        "confidence": "நம்பகத்தன்மை",
        "uncertainty": "நிச்சயமற்ற தன்மை",
        "prob_dist": "சாத்தியக்கூறுகளின் விபரம்",

        # Dataset & Labeling Page
        "dataset_title": "தரவுத்தொகுப்பு மேலாண்மை மற்றும் லேபிளிங்",
        "dataset_sub": "குடும்ப மல்லி புகைப்படங்களை நிர்வகிக்கவும், நகல்களை தவிர்க்கவும், பயிற்சிப் பிரிவுகளை உருவாக்கவும்",
        "dataset_ai_desc": "தரவு தொகுப்பு நிலை. முழு செடி புகைப்படங்கள் தனித்தனியாக பிரிக்கப்பட்டுள்ளன.",
        "dataset_safety": "குறைந்த புகைப்படங்களை வைத்து நம்பகமான மாதிரி உருவாகிவிடும் என்று கருதக்கூடாது. பல்வேறு காலை வெளிச்சம், செடி வயது மற்றும் சேத வகைகளை தொடர்ந்து சேகரிக்கவும்.",
        "tab_labeling": "பட லேபிளிங்",
        "tab_duplicates": "நகல்கள் தணிக்கை",
        "tab_splits": "தரவுப் பிரிப்புகள்",
        "tab_training": "மாதிரி பயிற்சி மற்றும் மதிப்பீடு",
        "tab_guidelines": "புகைப்பட வழிகாட்டி",
        "tab_whole_plant": "முழு செடி சேமிப்பு",

        # Plant Health Page
        "health_title": "பயிர் நலம் மற்றும் சேதக் கண்காணிப்பு",
        "health_sub": "தென்படும் அறிகுறிகளைப் பதிவுசெய்து, சந்தேகிக்கப்படும் காரணங்களை முறைப்படி ஆராய்க",
        "health_ai_desc": "ஆதார அடிப்படையிலான பகுப்பாய்வு இயங்குகிறது. வெளிப்படையான அறிகுறிகள் மற்றும் உத்தேச காரணங்கள் தனித்தனியாக கையாளப்படுகின்றன.",
        "health_safety": "புகைப்படத்தை மட்டுமே கொண்டு பூச்சிக்கொல்லிகளையோ உரங்களையோ பயன்படுத்த வேண்டாம். மண் ஈரப்பதம், வேர் நலம் மற்றும் இலைக்கு அடியில் உள்ள பூச்சிகளை ஆய்வு செய்து உறுதிப்படுத்தவும்.",
        "tab_log_symptoms": "அறிகுறிகள் பதிவு மற்றும் பகுப்பாய்வு",
        "tab_obs_history": "முந்தைய ஆய்வுகள் மற்றும் உறுதிப்படுத்தல்",
        "tab_scout_guide": "அறிவியல் கள ஆய்வு வழிகாட்டி",
        "obs_date": "ஆய்வு தேதி",
        "visible_symptoms_header": "தென்படும் கள அறிகுறிகள் பட்டியல்",
        "affected_part": "பாதிக்கப்பட்ட முக்கிய பகுதி",
        "damage_severity": "சேதத்தின் தீவிரம்",
        "new_flush": "புதிய இளந்தளிர்கள்",
        "older_leaves": "முதிர்ந்த கீழ் இலைகள்",
        "flower_buds": "மலர் மொட்டுகள்",
        "entire_bush": "முழு கிளை அல்லது முழு செடி",
        "mild": "குறைவான சேதம் (பத்து சதவீதத்திற்கும் கீழ்)",
        "moderate": "மிதமான சேதம் (பத்து முதல் முப்பது சதவீதம்)",
        "severe": "தீவிர சேதம் (முப்பது சதவீதத்திற்கு மேல்)",
        "diagnostic_hypotheses": "சந்தேகிக்கப்படும் காரணங்கள்",
        "missing_info": "முடிவுக்கு வர தேவையான கூடுதல் தகவல்கள்",
        "confirm_diagnosis": "இறுதி காரணத்தை உறுதிப்படுத்து",

        # Fertilizer Page
        "fert_title": "உர மேலாண்மை மற்றும் ஊட்டச்சத்து கணக்கீடு",
        "fert_sub": "உரங்களை முறைப்படி சரிபார்த்து, பயிருக்கு கிடைத்த தழை, மணி, சாம்பல் சத்துக்களை கணக்கிடுங்கள்",
        "fert_ai_desc": "ஊட்டச்சத்து கணக்கீடு செயலில் உள்ளது. ஒவ்வொரு செடிக்கும் கிடைத்த சத்துக்கள் கணக்கிடப்படுகின்றன.",
        "fert_safety": "பையின் நிறம் அல்லது வடிவத்தை மட்டும் வைத்து உரத்தை அடையாளம் காணாதீர்கள். அதிக தழைச்சத்து இலை வளர்ச்சியை மட்டுமே கூட்டி பூக்களை குறைத்துவிடும்.",
        "tab_log_fert": "உரமிடுதல் பதிவு மற்றும் கணக்கீடு",
        "tab_verify_fert": "உர ஆய்வு மற்றும் லேபிள் பதிவு",
        "tab_budget_fert": "ஊட்டச்சத்து இருப்பு மற்றும் இலக்கு",
        "app_date": "உரமிட்ட தேதி",
        "fert_product": "உரப் பொருள்",
        "quantity_kg": "பயன்படுத்திய மொத்த அளவு (கிலோகிராம்)",
        "active_nutrients_delivered": "செடிக்குக் கிடைத்த உண்மையான சத்துக்கள்",

        # Soil Health Page
        "soil_title": "மண் நலம் மற்றும் பரிசோதனை முடிவுகள்",
        "soil_sub": "மண் பரிசோதனை முடிவுகளைப் பதிவுசெய்து, கார அமில நிலை மற்றும் வடிகால் வசதியை ஆராய்க",
        "soil_ai_desc": "மண் விதி அமைப்பு செயலில் உள்ளது. உகந்த கார அமில அளவு ஆறு முதல் ஏழு ஆகும்.",
        "soil_safety": "செம்மண் மற்றும் களிமண் கலந்த நல்ல வடிகால் வசதி கொண்ட நிலங்களும் மல்லிக்கு ஏற்றவை. விடுபட்ட தகவல்களை சுயமாக யூகிக்காமல் முறையான மண் பரிசோதனை அறிக்கையை பயன்படுத்தவும்.",
        "test_date": "பரிசோதனை தேதி",
        "sample_location": "மண் எடுத்த இடம் மற்றும் ஆழம்",
        "soil_ph": "கார அமில நிலை",
        "soil_ec": "மின் கடத்துத்திறன்",
        "organic_carbon": "கரிம கரிமச்சத்து சதவீதம்",
        "avail_n": "கிடைக்கும் தழைச்சத்து (கிலோ/ஹெக்டேர்)",
        "avail_p": "கிடைக்கும் மணிச்சத்து (கிலோ/ஹெக்டேர்)",
        "avail_k": "கிடைக்கும் சாம்பல் சத்து (கிலோ/ஹெக்டேர்)",
        "soil_texture": "மண் தன்மை மற்றும் வடிகால்",

        # Weather Page
        "weather_title": "வானிலை மற்றும் பாசன மேலாண்மை",
        "weather_sub": "வெப்பநிலை, மழை மற்றும் வேர்ப்பகுதி ஈரப்பதத்தை கண்காணித்து சரியான பாசன முடிவுகளை எடுங்கள்",
        "weather_ai_desc": "களக் கண்காணிப்பு செயலில் உள்ளது. காலநிலை மற்றும் மண் விதிகள் ஒருங்கிணைக்கப்படுகின்றன.",
        "weather_safety": "வானிலை தகவலை மட்டும் வைத்து பாசன முடிவையோ அல்லது நோய் தாக்குதலையோ கணிக்க வேண்டாம். வேர்ப்பகுதி ஈரப்பதத்தை நேரில் பார்த்து பாசனம் செய்யவும்.",
        "day_temp": "பகல் வெப்பநிலை (டிகிரி செல்சியஸ்)",
        "rel_humidity": "காற்றின் ஈரப்பதம் சதவீதம்",
        "rainfall_today": "இன்றைய மழையளவு (மில்லிமீட்டர்)",
        "rainfall_forecast": "அடுத்த நாள் மழை முன்னறிவிப்பு (மில்லிமீட்டர்)",
        "irrig_applied": "இன்று நீர் பாய்ச்சப்பட்டதா",
        "irrig_method": "பாசன முறை",
        "soil_moisture_level": "மண் ஈரப்பத நிலை",

        # Farm History Page
        "history_title": "பண்ணை வரலாற்றுப் பதிவுகள் மற்றும் மேலாண்மை",
        "history_sub": "அனைத்து பதிவுகளையும் ஒரே இடத்தில் ஆராய்ந்து, தரவுகளைப் பதிவிறக்கம் செய்துகொள்ளுங்கள்",
        "history_ai_desc": "நிரந்தர தரவுத்தளம் செயலில் உள்ளது. அனைத்து தகவல்களும் முறையாக சேமிக்கப்படுகின்றன.",
    },

    "te": {
        # General & Sidebar
        "app_title": "స్మార్ట్ మల్లె",
        "app_subtitle": "మల్లె వ్యవసాయ సహాయకుడు",
        "display_language": "భాష ఎంపిక",
        "navigate_modules": "విభాగాలు",
        "garden_context_title": "తోట వివరాలు",
        "garden_crop": "పంట",
        "cultivation_method": "సాగు పద్ధతి",
        "cultivation_val": "నేల సాగు",
        "target_ph": "లక్ష్య పి.హెచ్ స్థాయి",
        "system_status": "వ్యవస్థ స్థితి",
        "active": "అందుబాటులో ఉంది",
        "agricultural_safety_notice": "వ్యవసాయ భద్రతా సమాచారం",
        "ai_status": "కృత్రిమ మేధస్సు స్థితి",
        "quick_nav": "త్వరిత నావిగేషన్",
        "recent_activity": "ఇటీవలి వివరాలు",

        # Actions & Buttons
        "btn_save": "వివరాలను భద్రపరచు",
        "btn_submit": "పరిశీలనను సమర్పించు",
        "btn_export_csv": "రికార్డులను డౌన్‌లోడ్ చేయి",
        "btn_run_ai": "అంచనాను లెక్కించు",
        "btn_audit_dupes": "నకిలీ ఫోటోల తనిఖీ",
        "btn_generate_splits": "డేటా విభజనలను రూపొందించు",
        "btn_train_model": "శిక్షణను ప్రారంభించు",
        "btn_calculate": "పోషకాలను లెక్కించు",
        "btn_verify_label": "ఎరువుల లేబుల్ తనిఖీ",

        # Dashboard Page
        "dash_title": "మల్లె తోట డాష్‌బోర్డ్",
        "dash_sub": "తోట ప్రస్తుత స్థితి, కోత సంసిద్ధత మరియు పంట నిర్వహణ పనులు",
        "dash_ai_desc": "వ్యవస్థ సిద్ధంగా ఉంది. క్షేత్ర స్థాయి డేటా నమోదు మరియు వ్యవసాయ నియమాలు ధృవీకరించబడ్డాయి.",
        "kpi_harvests": "కోత పరిశీలనలు",
        "kpi_health": "మొక్కల ఆరోగ్యం",
        "kpi_fertilizers": "ఎరువుల నిర్వహణ",
        "kpi_soil": "నేల పరీక్షలు",
        "sub_staged": "నమోదైన వివరాలు",
        "sub_investigation": "పరిశీలనలో ఉన్నవి",
        "sub_applications": "వేసిన ఎరువులు",
        "profile_plot_size": "తోట విస్తీర్ణం: సుమారు పావు ఎకరం నుండి ఒక ఎకరం",
        "profile_pruning": "కత్తిరింపు సమయం: వసంత కాల పూత కోసం నవంబర్ చివరి నుండి డిసెంబర్ లోపు కత్తిరింపు",
        "profile_sunlight": "ఎండ తీవ్రత: రోజుకు కనీసం ఆరు గంటల ప్రత్యక్ష సూర్యరశ్మి",
        "profile_watering": "నీటి యాజమాన్యం: నీరు నిల్వ ఉండకుండా చూసుకోవాలి, పదిహేను సెం.మీ లోతులో తేమ చూసి నీరు పెట్టాలి",
        "field_checklist_title": "రోజువారీ మల్లె తోట తనిఖీ జాబితా",
        "checklist_1_title": "1. ఉదయపు మొగ్గల కోత సమయం",
        "checklist_1_desc": "ఎండ వేడికి రేకలు విచ్చుకోకముందే ఉదయం ఆరు గంటల నుండి ఎనిమిదిన్నర లోపు కోత పూర్తి చేయాలి.",
        "checklist_2_title": "2. రాలిన మొగ్గల పరిశీలన",
        "checklist_2_desc": "రాలిన మొగ్గలను చీల్చి చూసి నారింజ రంగు మొగ్గ ఈగ పురుగులు ఉన్నాయో లేదో గమనించాలి.",
        "checklist_3_title": "3. నేలలో తేమ మరియు నీటి పారుదల",
        "checklist_3_desc": "పదిహేను నుండి ఇరవై సెం.మీ లోతులో తేమను చూడాలి. నీరు నిలిస్తే వేర్లు కుళ్లిపోతాయి.",
        "checklist_4_title": "4. ఆకుల అడుగు భాగం పరిశీలన",
        "checklist_4_desc": "లేత ఆకుల అడుగున తామర పురుగులు లేదా సాలీడు గూళ్లు ఉన్నాయో లేదో చూసిన తర్వాతే లోపాలను నిర్ధారించాలి.",
        "latest_harvest": "ఇటీవలి కోత నమోదు",
        "latest_fertilizer": "ఇటీవలి ఎరువుల నమోదు",

        # Flower Analysis Page
        "flower_title": "పూల పరిపక్వత విశ్లేషణ",
        "flower_sub": "మొగ్గల పరిపక్వతను పరిశీలించి, కోత సంసిద్ధతను నిర్ధారించి, ఫోటోలను భద్రపరచండి",
        "flower_ai_desc": "డేటా సేకరణ దశ. రైతు క్షేత్ర అనుభవమే ప్రామాణికం.",
        "flower_safety": "ధృవీకరించని కంప్యూటర్ అంచనాలపై ఆధారపడవద్దు. రైతు క్షేత్ర అనుభవమే తుది ప్రామాణికం.",
        "upload_bud_photo": "మొగ్గ ఫోటోను అప్‌లోడ్ చేయండి",
        "upload_bud_prompt": "స్పష్టమైన మల్లె మొగ్గ ఫోటోను ఎంచుకోండి:",
        "upload_help": "మంచి ఫలితాల కోసం ఉదయపు వెలుతురులో స్పష్టమైన ఫోటోలను తీయండి.",
        "grower_assessment": "రైతు క్షేత్ర పరిశీలన",
        "grower_caption": "నమూనా శిక్షణ కోసం మీ అనుభవంతో కూడిన తీర్పును నమోదు చేయండి.",
        "maturity_stage": "పరిపక్వత దశ",
        "garden_section": "తోట విభాగం",
        "harvest_quantity": "అంచనా పరిమాణం",
        "harvest_unit": "కొలత ప్రమాణం",
        "kg": "కిలోగ్రాములు",
        "grams": "గ్రాములు",
        "buds_count": "మొగ్గల సంఖ్య",
        "notes": "క్షేత్ర గమనికలు మరియు వివరాలు",
        "notes_placeholder": "ఉదాహరణ: ఉదయపు కోత, నాణ్యమైన తెల్లటి మొగ్గలు",
        "save_observation": "కోత వివరాలను భద్రపరచు",
        "harvest_guidance_title": "మొక్కల శాస్త్రీయ కోత సూచనలు",
        "ai_prediction_box": "కృత్రిమ మేధస్సు పరిశీలన",
        "predicted_stage": "అంచనా వేసిన దశ",
        "confidence": "ఖచ్చితత్వ శాతం",
        "uncertainty": "అనిశ్చితి స్థాయి",
        "prob_dist": "సంభావ్యత వివరాలు",

        # Dataset & Labeling Page
        "dataset_title": "డేటాసెట్ నిర్వహణ మరియు లేబులింగ్",
        "dataset_sub": "తోట ఫోటోలను నిర్వహించండి, నకిలీలను గుర్తించండి, శిక్షణ విభజనలను రూపొందించండి",
        "dataset_ai_desc": "డేటా నిర్వహణ దశ. మొత్తం మొక్క ఫోటోలు ప్రత్యేకంగా భద్రపరచబడ్డాయి.",
        "dataset_safety": "తక్కువ ఫోటోలతో నమ్మకమైన నమూనా రాదు. వివిధ సమయాలు, ఎండ వెలుతురు మరియు తెగుళ్ల ఫోటోలను క్రమం తప్పకుండా సేకరించండి.",
        "tab_labeling": "ఫోటోల లేబులింగ్",
        "tab_duplicates": "నకిలీల తనిఖీ",
        "tab_splits": "డేటా విభజనలు",
        "tab_training": "నమూనా శిక్షణ మరియు మూల్యాంకనం",
        "tab_guidelines": "ఫోటోగ్రఫీ మార్గదర్శకాలు",
        "tab_whole_plant": "మొత్తం మొక్కల నిల్వ",

        # Plant Health Page
        "health_title": "మొక్కల ఆరోగ్యం మరియు నష్టాల పరిశీలన",
        "health_sub": "కనిపించే లక్షణాలను నమోదు చేసి, అనుమానిత కారణాలను పద్ధతి ప్రకారం విశ్లేషించండి",
        "health_ai_desc": "ఆధారాల ఆధారిత విశ్లేషణ సిద్ధంగా ఉంది. కనిపించే లక్షణాలు మరియు అనుమానిత కారణాలు వేరుగా విశ్లేషించబడతాయి.",
        "health_safety": "ఫోటోలను మాత్రమే చూసి పురుగుమందులు లేదా ఎరువుల మోతాదులను నిర్ణయించవద్దు. నేల తేమ, వేర్లు మరియు ఆకుల క్రింది పురుగులను పరిశీలించి నిర్ధారించండి.",
        "tab_log_symptoms": "లక్షణాల నమోదు మరియు విశ్లేషణ",
        "tab_obs_history": "గత పరిశీలనలు మరియు నిర్ధారణ",
        "tab_scout_guide": "శాస్త్రీయ క్షేత్ర తనిఖీ సూచిక",
        "obs_date": "పరిశీలన తేదీ",
        "visible_symptoms_header": "కనిపించే క్షేత్ర లక్షణాల జాబితా",
        "affected_part": "ప్రధానంగా దెబ్బతిన్న భాగం",
        "damage_severity": "నష్ట తీవ్రత",
        "new_flush": "కొత్త లేత చిగుళ్లు",
        "older_leaves": "క్రింది ముదిరిన ఆకులు",
        "flower_buds": "పూల మొగ్గలు",
        "entire_bush": "మొత్తం కొమ్మ లేదా మొక్క",
        "mild": "స్వల్ప నష్టం (పది శాతం లోపు)",
        "moderate": "మధ్యస్థ నష్టం (పది నుండి ముప్పై శాతం)",
        "severe": "తీవ్ర నష్టం (ముప్పై శాతానికి పైగా)",
        "diagnostic_hypotheses": "అనుమానిత కారణాల విశ్లేషణ",
        "missing_info": "నిర్ధారణకు కావాల్సిన అదనపు సమాచారం",
        "confirm_diagnosis": "తుది కారణాన్ని నిర్ధారించు",

        # Fertilizer Page
        "fert_title": "ఎరువుల నిర్వహణ మరియు పోషకాల గణన",
        "fert_sub": "ఎరువుల ఫార్ములాను సరిచూసి, మొక్కకు అందిన నత్రజని, భాస్వరం, పొటాష్ పోషకాలను లెక్కించండి",
        "fert_ai_desc": "పోషకాల లెక్కింపు సిద్ధంగా ఉంది. ప్రతి మొక్కకు అందిన పోషకాలు ఖచ్చితంగా లెక్కించబడతాయి.",
        "fert_safety": "సంచి రంగు లేదా ఆకారాన్ని బట్టి ఎరువులను గుర్తించవద్దు. అధిక నత్రజని ఆకుల ఎదుగుదలనే పెంచి మొగ్గల సంఖ్యను తగ్గిస్తుంది.",
        "tab_log_fert": "ఎరువుల నమోదు మరియు లెక్కింపు",
        "tab_verify_fert": "ఎరువుల లేబుల్ తనిఖీ",
        "tab_budget_fert": "పోషకాల సమతుల్యత మరియు లక్ష్యం",
        "app_date": "ఎరువులు వేసిన తేదీ",
        "fert_product": "ఎరువుల రకం",
        "quantity_kg": "మొత్తం వేసిన పరిమాణం (కిలోలు)",
        "active_nutrients_delivered": "మొక్కకు లభించిన అసలు పోషకాలు",

        # Soil Health Page
        "soil_title": "నేల ఆరోగ్యం మరియు పోషకాల విశ్లేషణ",
        "soil_sub": "నేల పరీక్ష నివేదికలను నమోదు చేసి, పి.హెచ్ స్థాయి మరియు నీటి పారుదల సౌలభ్యాన్ని పరిశీలించండి",
        "soil_ai_desc": "నేల నియమాల ఇంజిన్ సిద్ధంగా ఉంది. మల్లెకు అనువైన పి.హెచ్ పరిధి ఆరు నుండి ఏడు.",
        "soil_safety": "ఎర్ర నేలలు మరియు సేంద్రీయ కర్బనం గల బంక నేలలు కూడా మల్లెకు ఎంతో అనుకూలం. అంచనాలతో కాకుండా అధికారిక నేల పరీక్ష నివేదిక ఆధారంగా నిర్ణయాలు తీసుకోండి.",
        "test_date": "పరీక్ష తేదీ",
        "sample_location": "నమూనా తీసిన లోతు మరియు స్థలం",
        "soil_ph": "నేల పి.హెచ్ స్థాయి",
        "soil_ec": "విద్యుత్ వాహకత",
        "organic_carbon": "సేంద్రీయ కర్బనం శాతం",
        "avail_n": "అందుబాటులో ఉన్న నత్రజని (కిలో/హెక్టారు)",
        "avail_p": "అందుబాటులో ఉన్న భాస్వరం (కిలో/హెక్టారు)",
        "avail_k": "అందుబాటులో ఉన్న పొటాష్ (కిలో/హెక్టారు)",
        "soil_texture": "నేల స్వభావం మరియు పారుదల",

        # Weather Page
        "weather_title": "వాతావరణం మరియు నీటిపారుదల నిర్వహణ",
        "weather_sub": "ఉష్ణోగ్రత, వర్షపాతం మరియు వేర్ల తేమను పరిశీలించి సకాలంలో నీటి యాజమాన్య నిర్ణయాలు తీసుకోండి",
        "weather_ai_desc": "క్షేత్ర పరిశీలన సిద్ధంగా ఉంది. వాతావరణం మరియు నేల నియమాలు సమన్వయం చేయబడ్డాయి.",
        "weather_safety": "వాతావరణ సమాచారం ఆధారంగా మాత్రమే నీరు పెట్టవద్దు. వేర్ల భాగంలో తేమను స్వయంగా చూసి నీటిని అందించండి.",
        "day_temp": "పగటి ఉష్ణోగ్రత (డిగ్రీల సెల్సియస్)",
        "rel_humidity": "గాలిలో తేమ శాతం",
        "rainfall_today": "నేటి వర్షపాతం (మిల్లీమీటర్లు)",
        "rainfall_forecast": "తదుపరి వర్ష సూచన (మిల్లీమీటర్లు)",
        "irrig_applied": "నేడు నీరు పెట్టారా",
        "irrig_method": "నీటి పారుదల పద్ధతి",
        "soil_moisture_level": "నేలలో తేమ స్థితి",

        # Farm History Page
        "history_title": "తోట సమగ్ర చరిత్ర మరియు రికార్డులు",
        "history_sub": "గత నిర్వహణ రికార్డులను సమీక్షించి, పోకడలను గమనించండి మరియు డేటాను డౌన్‌లోడ్ చేయండి",
        "history_ai_desc": "శాశ్వత డేటాబేస్ సిద్ధంగా ఉంది. అన్ని రికార్డులు సురక్షితంగా భద్రపరచబడ్డాయి.",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """
    Translates a key into the target language.
    Guarantees pure unmixed string output for the chosen language.
    """
    l = normalize_lang(lang)
    lang_dict = STRINGS.get(l, STRINGS["en"])
    val = lang_dict.get(key, STRINGS["en"].get(key, key))
    if kwargs:
        try:
            return val.format(**kwargs)
        except Exception:
            return val
    return val


def get_nav_name(page_key: str, lang: str = "en") -> str:
    """Returns pure navigation page name for given language."""
    l = normalize_lang(lang)
    return NAV_NAMES.get(l, NAV_NAMES["en"]).get(page_key, page_key)


def get_page_display_names(lang: str = "en") -> List[str]:
    """Returns the ordered list of pure page display names for the selected language."""
    l = normalize_lang(lang)
    mapping = NAV_NAMES.get(l, NAV_NAMES["en"])
    return [mapping.get(k, k) for k in PAGE_KEYS]


def get_page_key_from_display(display_name: str, lang: str = "en") -> str:
    """Resolves localized display name back to canonical PAGE_KEY."""
    l = normalize_lang(lang)
    mapping = NAV_NAMES.get(l, NAV_NAMES["en"])
    for key, name in mapping.items():
        if name == display_name:
            return key
    # Fallback search across all languages
    for each_lang in NAV_NAMES.values():
        for key, name in each_lang.items():
            if name == display_name:
                return key
    return PAGE_KEYS[0]


def get_stage_name(stage_key: str, lang: str = "en") -> str:
    """Returns pure single-language flower stage name."""
    l = normalize_lang(lang)
    return STAGE_NAMES.get(l, STAGE_NAMES["en"]).get(stage_key, stage_key)


def get_stage_key_from_name(stage_display: str, lang: str = "en") -> str:
    """Resolves localized stage display string back to canonical stage key."""
    l = normalize_lang(lang)
    mapping = STAGE_NAMES.get(l, STAGE_NAMES["en"])
    for key, val in mapping.items():
        if val == stage_display:
            return key
    # Fallback across all languages
    for each_dict in STAGE_NAMES.values():
        for key, val in each_dict.items():
            if val == stage_display:
                return key
    return "READY_TO_PLUCK"


def get_crop_name(lang: str = "en") -> str:
    """Returns botanical and common crop name in pure script."""
    l = normalize_lang(lang)
    return CROP_NAMES.get(l, CROP_NAMES["en"])


def get_section_options(lang: str = "en") -> List[str]:
    """Returns pure localized section names."""
    l = normalize_lang(lang)
    return list(SECTION_NAMES.get(l, SECTION_NAMES["en"]).values())
