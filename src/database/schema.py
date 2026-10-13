"""
Documented SQLite Database Schema for Smart Jasmine Farming Assistant.
Relational DDL for Jasminum sambac (குண்டு மல்லி) farm records.
"""

# Enable Foreign Key enforcement in SQLite
PRAGMA_FOREIGN_KEYS = "PRAGMA foreign_keys = ON;"
PRAGMA_WAL_MODE = "PRAGMA journal_mode = WAL;"

SCHEMA_DDL = """
-- 1. Farm Profile Table (General farm parameters, NO sensitive GPS coordinates)
CREATE TABLE IF NOT EXISTS farm_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_name TEXT NOT NULL,
    grower_name TEXT NOT NULL,
    crop_variety TEXT NOT NULL DEFAULT 'Jasminum sambac (குண்டு மல்லி)',
    region_district TEXT DEFAULT 'Madurai',
    total_area_acres REAL NOT NULL DEFAULT 0.5 CHECK(total_area_acres > 0),
    cultivation_method TEXT NOT NULL DEFAULT 'Ground soil cultivation',
    baseline_soil_type TEXT DEFAULT 'Red sandy loam',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Garden Sections Table (Beds, plots, age categories)
CREATE TABLE IF NOT EXISTS garden_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL REFERENCES farm_profiles(id) ON DELETE CASCADE,
    section_name TEXT NOT NULL UNIQUE,
    area_acres REAL DEFAULT 0.125 CHECK(area_acres > 0),
    plant_count INTEGER DEFAULT 100 CHECK(plant_count >= 0),
    planting_year INTEGER,
    sunlight_hours REAL DEFAULT 6.5,
    drainage_status TEXT DEFAULT 'Well-drained',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Fertilizer Products Table (Verified nutrient grades and labels)
CREATE TABLE IF NOT EXISTS fertilizer_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    npk_ratio TEXT,
    n_percent REAL DEFAULT 0.0 CHECK(n_percent >= 0 AND n_percent <= 100),
    p_percent REAL DEFAULT 0.0 CHECK(p_percent >= 0 AND p_percent <= 100),
    k_percent REAL DEFAULT 0.0 CHECK(k_percent >= 0 AND k_percent <= 100),
    organic_matter_percent REAL DEFAULT 0.0,
    manufacturer TEXT,
    label_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Fertilizer Applications Table (Treatments applied to sections)
CREATE TABLE IF NOT EXISTS fertilizer_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES fertilizer_products(id) ON DELETE SET NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity_kg REAL NOT NULL CHECK(quantity_kg > 0 AND quantity_kg <= 5000),
    application_date DATE NOT NULL,
    application_method TEXT NOT NULL,
    reason TEXT,
    n_supplied_kg REAL DEFAULT 0.0,
    p_supplied_kg REAL DEFAULT 0.0,
    k_supplied_kg REAL DEFAULT 0.0,
    label_image_filename TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Soil Tests Table (pH, EC, texture, and laboratory nutrient levels)
CREATE TABLE IF NOT EXISTS soil_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    test_date DATE NOT NULL,
    sampling_location TEXT NOT NULL,
    ph REAL NOT NULL CHECK(ph >= 3.0 AND ph <= 10.0),
    ec_dsm REAL DEFAULT 0.4 CHECK(ec_dsm >= 0),
    texture TEXT NOT NULL,
    drainage TEXT NOT NULL,
    organic_carbon_pct REAL DEFAULT 0.5 CHECK(organic_carbon_pct >= 0),
    available_n TEXT,
    available_p TEXT,
    available_k TEXT,
    micronutrients_status TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Irrigation Records Table (Root moisture, timing, and depth)
CREATE TABLE IF NOT EXISTS irrigation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    irrigation_date DATE NOT NULL,
    was_irrigated INTEGER NOT NULL DEFAULT 1 CHECK(was_irrigated IN (0, 1)),
    method TEXT NOT NULL,
    moisture_depth_observation TEXT NOT NULL,
    duration_minutes INTEGER DEFAULT 45,
    weather_temp_c REAL,
    humidity_pct REAL,
    rainfall_mm REAL DEFAULT 0.0,
    forecast_rain_mm REAL DEFAULT 0.0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Pruning Records Table (Annual winter and maintenance pruning)
CREATE TABLE IF NOT EXISTS pruning_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    pruning_date DATE NOT NULL,
    pruning_type TEXT NOT NULL,
    height_cut_cm REAL DEFAULT 35.0 CHECK(height_cut_cm > 0),
    defoliation_done INTEGER DEFAULT 0 CHECK(defoliation_done IN (0, 1)),
    foliage_cleared INTEGER DEFAULT 1 CHECK(foliage_cleared IN (0, 1)),
    water_withheld_days INTEGER DEFAULT 10 CHECK(water_withheld_days >= 0),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Image Labels Table (Ground truth dataset staging)
CREATE TABLE IF NOT EXISTS image_labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL UNIQUE,
    filepath TEXT NOT NULL,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    image_type TEXT NOT NULL,
    label_stage TEXT NOT NULL CHECK(label_stage IN ('READY_TO_PLUCK', 'NOT_READY', 'TOO_OPEN', 'DAMAGED_OR_ABNORMAL')),
    labeled_by TEXT DEFAULT 'grower',
    width INTEGER,
    height INTEGER,
    format TEXT,
    filesize_kb REAL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Plant Observations Table (Visible symptoms and damage scouting)
CREATE TABLE IF NOT EXISTS plant_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    observation_date DATE NOT NULL,
    visible_symptoms TEXT NOT NULL,
    affected_part TEXT NOT NULL,
    severity TEXT NOT NULL,
    suspected_causes TEXT,
    confirmed_diagnosis TEXT DEFAULT 'Unconfirmed',
    status TEXT DEFAULT 'Under Investigation',
    image_filename TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Harvest Records Table (Yield quantities and market grades)
CREATE TABLE IF NOT EXISTS harvest_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    harvest_date DATE NOT NULL,
    stage TEXT NOT NULL CHECK(stage IN ('READY_TO_PLUCK', 'NOT_READY', 'TOO_OPEN', 'DAMAGED_OR_ABNORMAL')),
    quantity REAL NOT NULL CHECK(quantity > 0),
    unit TEXT NOT NULL DEFAULT 'buds',
    grade TEXT,
    time_of_day TEXT DEFAULT 'Morning (6:00 - 8:30 AM)',
    image_filename TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Recommendations Table (Actionable guidance with supporting evidence)
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER REFERENCES garden_sections(id) ON DELETE SET NULL,
    recommendation_date DATE NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    observation_basis TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    supporting_evidence TEXT NOT NULL,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance and Query Optimization Indexes
CREATE INDEX IF NOT EXISTS idx_harvest_date ON harvest_records(harvest_date);
CREATE INDEX IF NOT EXISTS idx_harvest_stage ON harvest_records(stage);
CREATE INDEX IF NOT EXISTS idx_fertilizer_date ON fertilizer_applications(application_date);
CREATE INDEX IF NOT EXISTS idx_soil_date ON soil_tests(test_date);
CREATE INDEX IF NOT EXISTS idx_irrigation_date ON irrigation_records(irrigation_date);
CREATE INDEX IF NOT EXISTS idx_observations_date ON plant_observations(observation_date);
CREATE INDEX IF NOT EXISTS idx_image_labels_stage ON image_labels(label_stage);
"""
