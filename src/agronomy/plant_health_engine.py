"""
Plant Health Symptom Observation and Diagnostic Hypotheses Engine for Jasminum sambac.
Enforces strict separation between visible physical observations and confirmed diagnoses.
Provides differential diagnostic hypotheses, missing information audits, and expert referral triggers.
Reference: TNAU Floriculture Advisory & ICAR-IIHR Crop Protection Guidelines.
"""

from typing import Dict, Any, List, Optional


# Comprehensive Catalog of Visible Symptoms
VISIBLE_SYMPTOMS_CATALOG: Dict[str, Dict[str, Any]] = {
    "yellowing_older_leaves": {
        "id": "yellowing_older_leaves",
        "name_en": "Yellowing of Older Lower Leaves",
        "name_ta": "முதிர்ந்த கீழ் இலைகள் மஞ்சள் நிறமாதல்",
        "name_te": "ముదిరిన క్రింది ఆకులు పసుపు రంగులోకి మారడం",
        "plant_part": "Older lower leaves",
        "description": "General loss of green chlorophyll starting uniformly from bottom mature leaves.",
    },
    "yellowing_young_leaves": {
        "id": "yellowing_young_leaves",
        "name_en": "Interveinal Yellowing on Young Tender Leaves",
        "name_ta": "புதிய இளந்தளிர்களில் நரம்புகளுக்கு இடையே மஞ்சள் நிறமாதல்",
        "name_te": "లేత కొత్త ఆకుల ఈనెల మధ్య పసుపు రంగులోకి మారడం",
        "plant_part": "New tender flush",
        "description": "Leaf blade turns pale yellow while veins remain sharply green (interveinal chlorosis).",
    },
    "curled_leaves_downward": {
        "id": "curled_leaves_downward",
        "name_en": "Downwards Curled / Crinkled Leaves",
        "name_ta": "இலைகள் கீழ்நோக்கி சுருங்குதல்",
        "name_te": "ఆకులు క్రిందికి ముడుచుకోవడం",
        "plant_part": "New leaves and shoot tips",
        "description": "Leaf margins curl downwards with crinkled or puckered surface texture.",
    },
    "curled_leaves_upward": {
        "id": "curled_leaves_upward",
        "name_en": "Upwards Cupping / Stippled Speckling",
        "name_ta": "இலைகள் மேல்நோக்கி கிண்ணம் போல் சுருங்குதல்",
        "name_te": "ఆకులు పైకి దోనెలా ముడుచుకోవడం",
        "plant_part": "Mid to upper foliage",
        "description": "Leaves cup upwards, fine speckling/bronzing, dusty look on leaf underside.",
    },
    "bud_bore_holes": {
        "id": "bud_bore_holes",
        "name_en": "Bore Holes with Frass in Flower Buds",
        "name_ta": "மொட்டுகளில் துளையிடப்பட்டு புழு கழிவுகள் இருத்தல்",
        "name_te": "మొగ్గలలో రంధ్రాలు మరియు పురుగు విసర్జన ఉండటం",
        "plant_part": "Flower buds",
        "description": "Small circular entry holes bored into flower buds with dark brownish fecal pellets (frass).",
    },
    "bud_webbing": {
        "id": "bud_webbing",
        "name_en": "Silken Webbing Binding Flower Clusters",
        "name_ta": "மொட்டு கொத்துக்கள் வலைப் பின்னலால் இணைக்கப்பட்டிருத்தல்",
        "name_te": "మొగ్గల గుత్తులు దారపు వలలా అల్లుకుపోవడం",
        "plant_part": "Flower bud cymes",
        "description": "Multiple flower buds webbed together with fine silk threads, hollowed inside.",
    },
    "bud_dropping_pale": {
        "id": "bud_dropping_pale",
        "name_en": "Premature Pale / Pinkish Bud Drop",
        "name_ta": "மொட்டுகள் வெளிர்/இளஞ்சிவப்பு நிறமாகி உதிர்தல்",
        "name_te": "లేత గులాబీ లేదా పాలిపోయిన మొగ్గలు రాలిపోవడం",
        "plant_part": "Flower buds and pedicels",
        "description": "Buds turn sickly pale or reddish-pink at the base, drying and detaching before harvest size.",
    },
    "stunted_shoots_wilt": {
        "id": "stunted_shoots_wilt",
        "name_en": "Stunted Shoots & Daytime Foliar Wilting",
        "name_ta": "வளர்ச்சி குன்றி பகலில் வாடுதல்",
        "name_te": "ఎదుగుదల లోపించి పగటిపూట ఆకులు వాలిపోవడం",
        "plant_part": "Entire branch or bush",
        "description": "Leaves droop during sunny midday despite moist ground; shoots exhibit short internodes.",
    },
    "black_sooty_coating": {
        "id": "black_sooty_coating",
        "name_en": "Black Powdery Film on Leaf Surface",
        "name_ta": "இலைகளின் மேல் கரும்பூஞ்சாணம் படர்தல்",
        "name_te": "ఆకుల ఉపరితలంపై నల్లటి మసి పూత ఏర్పడటం",
        "plant_part": "Upper leaf surface",
        "description": "Superficial black mold wiping off with finger pressure, following sticky honeydew deposits.",
    },
}


# Differential Diagnoses Knowledge Base
DIFFERENTIAL_DIAGNOSES: Dict[str, Dict[str, Any]] = {
    "nitrogen_deficiency": {
        "cause_name_en": "Nitrogen Deficiency",
        "cause_name_ta": "தழைச்சத்து குறைபாடு",
        "cause_name_te": "నత్రజని లోపం",
        "category": "Nutrient Imbalance",
        "matching_symptoms": ["yellowing_older_leaves"],
        "supporting_indicators": [
            "Uniform yellowing starting strictly from older bottom leaves",
            "Slow shoot elongation and overall light green canopy",
            "No leaf webbing, insect stippling, or waterlogged soil",
        ],
        "contradicting_indicators": [
            "Yellowing confined only to newly emerging leaves",
            "Persistent standing water in beds (suggests root suffocation instead)",
        ],
        "verification_steps": [
            "Check total nitrogen applied in the last 60 days via Fertilizer Records.",
            "Inspect soil test available Nitrogen level (normal is 280-560 kg/ha).",
        ],
        "missing_info_needed": [
            "Soil available N test report",
            "Recent fertilizer application dates and quantities",
        ],
        "evidence_source": "TNAU Agritech Floriculture - Soil Nutrient Deficiency Key",
    },
    "iron_chlorosis": {
        "cause_name_en": "Iron (Fe) / Zinc (Zn) Chlorosis",
        "cause_name_ta": "இரும்பு / துத்தநாக சத்து குறைபாடு (சுண்ணாம்பு நிலம்)",
        "cause_name_te": "ఇనుము / జింక్ లోపం (సున్నపు నేలలు)",
        "category": "Nutrient Imbalance",
        "matching_symptoms": ["yellowing_young_leaves"],
        "supporting_indicators": [
            "Interveinal chlorosis on fresh tender terminal flush",
            "Soil pH is alkaline or calcareous (pH > 7.5)",
            "Older leaves remain dark green while new shoots emerge ivory-yellow",
        ],
        "contradicting_indicators": [
            "Soil pH is acidic (pH < 6.5)",
            "Yellowing is concentrated only at the base of the bush",
        ],
        "verification_steps": [
            "Test soil pH and free calcium carbonate content.",
            "Verify whether chlorosis appears immediately following flush after pruning.",
        ],
        "missing_info_needed": [
            "Soil test report for pH, EC, and free calcium carbonate",
            "Foliar micronutrient spray history",
        ],
        "evidence_source": "ICAR-IIHR Jasmine Nutrient Management Guide",
    },
    "poor_drainage_root_suffocation": {
        "cause_name_en": "Waterlogging / Root Oxygen Deprivation",
        "cause_name_ta": "வடிகால் அடைப்பு / வேர் மூச்சுத்திணறல்",
        "cause_name_te": "నీరు నిల్వ ఉండటం / వేర్లకు ప్రాణవాయువు లోపం",
        "category": "Physiological / Soil Physical",
        "matching_symptoms": ["yellowing_older_leaves", "stunted_shoots_wilt"],
        "supporting_indicators": [
            "Soil remains muddy/saturated > 24 hours after rain or irrigation",
            "Lower leaves turn yellow and drop readily upon slight touch",
            "Clayey soil texture with sluggish water infiltration",
        ],
        "contradicting_indicators": [
            "Well-drained sandy loam soil with rapid water percolation",
            "Soil surface dry and powdery",
        ],
        "verification_steps": [
            "Dig a small 15 cm inspection pit in the bed to observe subsoil standing water.",
            "Smell subsoil sample: foul or stagnant anaerobic odor indicates root suffocation.",
        ],
        "missing_info_needed": [
            "Recent irrigation frequency and rainfall amounts",
            "Bed drainage status and subsoil percolation test",
        ],
        "evidence_source": "TNAU Floriculture - Jasmine Water Management & Drainage Guidelines",
    },
    "jasmine_bud_worm": {
        "cause_name_en": "Jasmine Bud Worm (Hendecasis duplifascialis)",
        "cause_name_ta": "மல்லி மொட்டுப்புழு தாக்குதல்",
        "cause_name_te": "మల్లె మొగ్గ తొలుచు పురుగు",
        "category": "Entomological Pest",
        "matching_symptoms": ["bud_bore_holes", "bud_webbing"],
        "supporting_indicators": [
            "Circular entry holes bored into floral buds with dark frass pellets",
            "Flower buds webbed together by silk threads",
            "Green caterpillar with dark head found inside hollowed buds",
        ],
        "contradicting_indicators": [
            "Buds drop smoothly without holes or silken webbing",
        ],
        "verification_steps": [
            "Pick 10 bored buds and slice open longitudinally with a razor.",
            "Confirm presence of greenish caterpillar or frass granules inside petal whorls.",
        ],
        "missing_info_needed": [
            "Percentage of total flower buds bored in the section (economic threshold is >10%)",
            "Light trap catches or nocturnal moth activity in garden",
        ],
        "evidence_source": "TNAU Agritech Portal - Crop Protection: Jasmine Pest Management",
    },
    "blossom_midge": {
        "cause_name_en": "Jasmine Blossom Midge (Contarinia maculipennis)",
        "cause_name_ta": "மல்லி மொட்டு ஈ தாக்குதல்",
        "cause_name_te": "మల్లె మొగ్గ ఈగ",
        "category": "Entomological Pest",
        "matching_symptoms": ["bud_dropping_pale"],
        "supporting_indicators": [
            "Buds turn pale or pinkish-purple at base and drop before opening",
            "Swelling or slight distortion at the bud calyx base",
            "Tiny yellow-orange maggots visible inside fallen buds",
        ],
        "contradicting_indicators": [
            "Bore holes and silken webbing present (indicates bud worm instead)",
        ],
        "verification_steps": [
            "Collect freshly fallen buds from ground and dissect under 10x lens.",
            "Look for jumping yellow-orange maggots (midge larvae) inside the corolla tube base.",
        ],
        "missing_info_needed": [
            "Fallen bud count per square meter under the canopy",
            "Recent morning humidity and shade conditions",
        ],
        "evidence_source": "TNAU Horticultural Research Station (HRS) Ooty / Yercaud Jasmine Advisory",
    },
    "red_spider_mites": {
        "cause_name_en": "Red Spider Mite (Tetranychus urticae)",
        "cause_name_ta": "செம்பேன் தாக்குதல்",
        "cause_name_te": "ఎర్ర నల్లి",
        "category": "Acarological Pest",
        "matching_symptoms": ["curled_leaves_upward"],
        "supporting_indicators": [
            "Fine pale yellow stippling and speckling on upper leaf surface",
            "Silken dust-like webbing on underside of leaves",
            "Severe during hot, dry summer months (March - June)",
        ],
        "contradicting_indicators": [
            "Wet, rainy weather with frequent downpours",
        ],
        "verification_steps": [
            "Tap a suspected branch over a clean sheet of white paper.",
            "Observe paper in bright sunlight for tiny reddish-brown walking specks.",
        ],
        "missing_info_needed": [
            "10x hand lens underleaf inspection result",
            "Current daytime temperature and relative humidity",
        ],
        "evidence_source": "ICAR-IIHR Integrated Pest Management in Commercial Floriculture",
    },
    "thrips": {
        "cause_name_en": "Jasmine Thrips (Thrips orientalis)",
        "cause_name_ta": "மல்லி இலைப்பேன்",
        "cause_name_te": "తామర పురుగులు",
        "category": "Entomological Pest",
        "matching_symptoms": ["curled_leaves_downward"],
        "supporting_indicators": [
            "Curling and crinkling of tender shoots and leaves",
            "Silvering or brownish streaks on petals and leaf margins",
            "Slender tiny black/yellow active insects found inside bud whorls",
        ],
        "contradicting_indicators": [
            "No curling on tender shoots; only bottom mature leaves affected",
        ],
        "verification_steps": [
            "Tap fresh tender flush over palm or white paper to detect rapidly moving slender insects.",
        ],
        "missing_info_needed": [
            "Visual count of thrips per shoot terminal",
        ],
        "evidence_source": "TNAU Floriculture Advisory - Jasmine Sucking Pest Management",
    },
    "root_rot_collar_rot": {
        "cause_name_en": "Collar Rot / Root Rot (Sclerotium rolfsii / Fusarium)",
        "cause_name_ta": "வேரழுகல் / தண்டு அழுகல் நோய்",
        "cause_name_te": "మొదలు కుళ్లు / వేరు కుళ్లు తెగులు",
        "category": "Fungal Plant Disease",
        "matching_symptoms": ["stunted_shoots_wilt", "yellowing_older_leaves"],
        "supporting_indicators": [
            "Sudden wilting and drying of whole branches or bushes in patches",
            "Foliage dries brown while remaining attached to dead branches",
            "Brownish decay and white mycelial fan at soil-line collar region",
        ],
        "contradicting_indicators": [
            "Only leaf margins yellowing without branch wilting",
            "Bush recovers completely after morning irrigation",
        ],
        "verification_steps": [
            "Gently scrape bark at the collar zone (ground level): brown/black dead vascular tissue indicates collar rot.",
            "Check for small mustard-seed-like brownish resting bodies (sclerotia) near soil line.",
        ],
        "missing_info_needed": [
            "Collar zone visual inspection report",
            "History of soil water stagnation or previous rot occurrences",
        ],
        "evidence_source": "TNAU Department of Plant Pathology - Jasmine Disease Guide",
    },
}


def analyze_plant_health_observations(
    reported_symptom_ids: List[str],
    affected_part: str,
    severity: str,
    has_image: bool = False,
    soil_ph: Optional[float] = None,
    soil_drainage: Optional[str] = None,
    recent_temp_c: Optional[float] = None,
    recent_rain_mm: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Analyzes visible crop symptoms and generates ranked differential diagnostic hypotheses.
    Enforces strict separation of visible symptoms from confirmed causes.
    Identifies missing ground truth information and produces safety disclaimers.
    """
    if not reported_symptom_ids:
        return {
            "status": "NO_SYMPTOMS",
            "message": "No visible symptoms selected. Please select at least one physical observation.",
            "hypotheses": [],
            "missing_information": [],
            "expert_referral": None,
        }

    # 1. Match Symptoms to Hypotheses
    candidate_hypotheses = []

    for diag_key, diag_info in DIFFERENTIAL_DIAGNOSES.items():
        matching = set(reported_symptom_ids).intersection(set(diag_info["matching_symptoms"]))
        if matching:
            score = len(matching) * 10

            # Contextual modifiers based on field environment
            # A. Soil pH context
            if diag_key == "iron_chlorosis":
                if soil_ph is not None:
                    if soil_ph >= 7.5:
                        score += 15  # strongly supports iron chlorosis
                    elif soil_ph < 6.5:
                        score -= 10  # contradicts iron chlorosis
            elif diag_key == "nitrogen_deficiency":
                if "New tender" in affected_part:
                    score -= 8  # Nitrogen deficiency shows on older lower leaves first

            # B. Drainage & Rain context
            if diag_key == "poor_drainage_root_suffocation":
                if soil_drainage and "poor" in soil_drainage.lower():
                    score += 15
                if recent_rain_mm and recent_rain_mm > 30.0:
                    score += 10

            # C. Weather context for mites
            if diag_key == "red_spider_mites":
                if recent_temp_c and recent_temp_c >= 35.0:
                    score += 10

            # D. Bud worm / midge part specificity
            if diag_key in ("jasmine_bud_worm", "blossom_midge"):
                if "Bud" in affected_part:
                    score += 10

            candidate_hypotheses.append({
                "id": diag_key,
                "score": score,
                "cause_name_en": diag_info["cause_name_en"],
                "cause_name_ta": diag_info["cause_name_ta"],
                "category": diag_info["category"],
                "matched_symptoms_count": len(matching),
                "supporting_indicators": diag_info["supporting_indicators"],
                "contradicting_indicators": diag_info["contradicting_indicators"],
                "verification_steps": diag_info["verification_steps"],
                "missing_info_needed": diag_info["missing_info_needed"],
                "evidence_source": diag_info["evidence_source"],
                "confidence_label": "UNCONFIRMED_HYPOTHESIS (Requires field physical verification)",
            })

    # Sort hypotheses by score descending
    candidate_hypotheses.sort(key=lambda h: h["score"], reverse=True)

    # 2. Compile Unique Missing Information Needed
    all_missing_info = set()
    for h in candidate_hypotheses[:3]:
        for item in h["missing_info_needed"]:
            all_missing_info.add(item)

    if soil_ph is None:
        all_missing_info.add("Current soil pH test report (vital to differentiate iron chlorosis from root issues)")
    if soil_drainage is None:
        all_missing_info.add("Subsoil drainage and percolation assessment at 15-20 cm root depth")

    # 3. Check Expert Referral Conditions
    expert_referral = check_expert_referral_conditions(
        severity=severity,
        reported_symptom_ids=reported_symptom_ids,
        top_hypotheses=[h["id"] for h in candidate_hypotheses[:2]],
    )

    return {
        "status": "ANALYSIS_COMPLETE",
        "symptoms_reported": [
            VISIBLE_SYMPTOMS_CATALOG[sid]["name_en"]
            for sid in reported_symptom_ids
            if sid in VISIBLE_SYMPTOMS_CATALOG
        ],
        "affected_part": affected_part,
        "severity": severity,
        "hypotheses_count": len(candidate_hypotheses),
        "hypotheses": candidate_hypotheses,
        "missing_information": sorted(list(all_missing_info)),
        "expert_referral": expert_referral,
        "safety_disclaimer": (
            "⚠️ EVIDENCE-BASED AGRICULTURAL SAFETY NOTICE: "
            "These hypotheses are diagnostic possibilities generated from visual observation, "
            "NOT confirmed clinical laboratory diagnoses. "
            "NEVER apply chemical insecticides, fungicides, or synthetic fertilizers without "
            "performing the listed physical verification steps and consulting local agricultural officers."
        ),
    }


def check_expert_referral_conditions(
    severity: str,
    reported_symptom_ids: List[str],
    top_hypotheses: List[str],
) -> Optional[Dict[str, Any]]:
    """
    Evaluates whether the crop condition exceeds safe home management and requires
    referral to a qualified agricultural authority (TNAU / KVK / Horticulture Officer).
    """
    is_referral_needed = False
    reasons = []

    # Condition 1: Severe crop loss / widespread damage
    if "Severe (>30%" in severity:
        is_referral_needed = True
        reasons.append("High disease/pest pressure exceeding 30% of the garden section.")

    # Condition 2: Collar rot / sudden systemic wilt
    if "stunted_shoots_wilt" in reported_symptom_ids and "root_rot_collar_rot" in top_hypotheses:
        is_referral_needed = True
        reasons.append("Suspected systemic collar rot or vascular wilt, which can rapidly kill entire planted beds.")

    # Condition 3: Co-occurring multiple bud pests during peak harvest
    if "bud_bore_holes" in reported_symptom_ids and "bud_dropping_pale" in reported_symptom_ids:
        is_referral_needed = True
        reasons.append("Concurrent bud worm and blossom midge damage threatening total commercial yield.")

    if not is_referral_needed:
        return None

    return {
        "is_recommended": True,
        "urgency": "High - Visit or contact within 48 hours",
        "reasons": reasons,
        "recommended_authorities": [
            {
                "entity": "Krishi Vigyan Kendra (KVK) / TNAU Research Station",
                "role": "Subject Matter Specialist (Plant Protection / Horticulture)",
                "contact_info": "Visit your nearest district KVK or TNAU Floriculture Department",
            },
            {
                "entity": "Assistant Director of Horticulture (ADH) / Block Horticultural Officer",
                "role": "Government Field Extension Officer",
                "contact_info": "Taluk / Block Agricultural Extension Office (வேளாண்மை விரிவாக்க மையம்)",
            },
        ],
        "sample_collection_protocol": (
            "1. Collect 3-5 fresh twigs showing the transition zone between healthy green tissue and diseased tissue.\n"
            "2. Place inside a clean, dry paper envelope or perforated bag (do not seal airtight in plastic).\n"
            "3. If bud pests are present, collect 10-15 fallen/bored buds in a small container.\n"
            "4. Bring a 500g composite soil sample taken from 0-15 cm root depth for on-site pH/salinity check."
        ),
    }
