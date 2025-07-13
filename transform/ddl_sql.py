CREATE_DTP_TABLE_SQL = """
-- Main DTP (Traffic Accident) table
CREATE TABLE IF NOT EXISTS dtp (
    id BIGINT PRIMARY KEY,
    registration_number VARCHAR(20),
    date_time TEXT,
    dtp_type VARCHAR(100),
    district VARCHAR(100),
    vehicle_count INT,
    participant_count INT,
    died INT,
    injured INT,

    -- InfoDTP fields
    coord_l DECIMAL(10,6),
    coord_w DECIMAL(10,6),
    change_org_motion VARCHAR(255),
    road VARCHAR(255),
    road_condition VARCHAR(100),
    road_category VARCHAR(10),
    road_value VARCHAR(255),
    settlement VARCHAR(100),
    street VARCHAR(100),
    street_category VARCHAR(100),
    house VARCHAR(50),
    km_mark VARCHAR(10),
    m_mark VARCHAR(10),
    lighting_condition VARCHAR(255),
    dtp_scheme_number VARCHAR(10)
);
"""
CREATE_ROAD_SQL = """
-- Table for OBJ_DTP (Road objects)
CREATE TABLE IF NOT EXISTS dtp_objects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT,
    object_description VARCHAR(255),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_FACTORS_SQL = """
-- Table for factors
CREATE TABLE IF NOT EXISTS dtp_factors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT,
    factor VARCHAR(255),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_NDU_SQL = """
-- Table for ndu
CREATE TABLE IF NOT EXISTS dtp_ndu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT,
    ndu_value VARCHAR(255),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_WEATHER_CONDITIONS_SQL = """
-- Table for weather conditions
CREATE TABLE IF NOT EXISTS dtp_weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT,
    weather_condition VARCHAR(100),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_ROAD_SECTION_SQL = """
-- Table for road sections
CREATE TABLE IF NOT EXISTS dtp_road_sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT,
    section_description VARCHAR(255),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_DTP_VEHICLES_SQL = """
-- Table for vehicles involved in accidents
CREATE TABLE IF NOT EXISTS dtp_vehicles (
    id TEXT PRIMARY KEY,
    card_id BIGINT,
    color VARCHAR(50),
    ownership_form VARCHAR(100),
    manufacture_year INT,
    trailer VARCHAR(100),
    model VARCHAR(100),
    brand VARCHAR(50),
    owner_type VARCHAR(100),
    drive_type VARCHAR(100),
    technical_faults VARCHAR(255),
    class VARCHAR(100),
    status VARCHAR(100),
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""
CREATE_DTP_VEHICLE_PARTICIPANTS_SQL = """
-- Table for participants in accidents
CREATE TABLE IF NOT EXISTS dtp_vehicle_participants (
    id TEXT PRIMARY KEY ,
    vehicle_id Text,
    role VARCHAR(50),
    sex VARCHAR(20),
    safety_belt VARCHAR(10),
    fled VARCHAR(100),
    injury_status VARCHAR(255),
    age INT,
    alco VARCHAR(50),
    seat_group VARCHAR(50),
    FOREIGN KEY (vehicle_id) REFERENCES dtp_vehicles(id)
);
"""
CREATE_VIOLATIONS_SQL = """
-- Table for NPDD violations
CREATE TABLE IF NOT EXISTS dtp_violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id TEXT,
    violation_code VARCHAR(50),
    FOREIGN KEY (participant_id) REFERENCES dtp_participants(id)
);
"""
CREATE_SOP_VIOLATIONS_SQL = """
-- Table for SOP_NPDD violations
CREATE TABLE IF NOT EXISTS dtp_sop_violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id TEXT,
    violation_code VARCHAR(50),
    FOREIGN KEY (participant_id) REFERENCES dtp_participants(id)
);
"""
CREATE_DTP_PARTICIPANTS_INFO_SQL = """
-- Table for uchInfo (additional participant info)
CREATE TABLE IF NOT EXISTS dtp_participants (
    id Text PRIMARY KEY,
    card_id BIGINT,
    role VARCHAR(50),
    sex VARCHAR(20),
    fled VARCHAR(100),
    injury_status VARCHAR(255),
    age INT,
    alco VARCHAR(50),
    -- Add fields as needed based on actual data
    FOREIGN KEY (card_id) REFERENCES dtp(id)
);
"""


def all_ddl_sql():
    ddl = [
        CREATE_DTP_TABLE_SQL,
        CREATE_ROAD_SQL,
        CREATE_FACTORS_SQL,
        CREATE_NDU_SQL,
        CREATE_WEATHER_CONDITIONS_SQL,
        CREATE_ROAD_SECTION_SQL,
        CREATE_DTP_VEHICLES_SQL,
        CREATE_DTP_VEHICLE_PARTICIPANTS_SQL,
        CREATE_VIOLATIONS_SQL,
        CREATE_SOP_VIOLATIONS_SQL,
        CREATE_DTP_PARTICIPANTS_INFO_SQL,
    ]
    for sql in ddl:
        yield sql
