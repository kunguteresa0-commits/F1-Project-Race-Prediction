-- 1. Drivers Table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(50) PRIMARY KEY,
    driver_number INT,
    full_name VARCHAR(100),
    nationality VARCHAR(50)
);

-- 2. Results Table
DROP TABLE IF EXISTS results; 
CREATE TABLE results (
    result_id SERIAL PRIMARY KEY,
    race_id INT,
    season INT,
    round INT,
    circuit_id VARCHAR(100),
    driver_id VARCHAR(50) REFERENCES drivers(driver_id),
    grid INT,
    position INT,
    is_podium BOOLEAN,
    points FLOAT,
    UNIQUE(race_id, driver_id)
);

-- 3. Features Table (Added grid column)
DROP TABLE IF EXISTS features;
CREATE TABLE features (
    feature_id SERIAL PRIMARY KEY,
    driver_id VARCHAR(50) REFERENCES drivers(driver_id),
    race_id INT,
    grid INT,           -- Added this to store the starting position
    driver_form FLOAT,
    career_races INT,
    is_podium BOOLEAN,
    UNIQUE(race_id, driver_id)
);