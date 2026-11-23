
USE tennis_analytics;

-- 1. Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- 2. Competitions Table
CREATE TABLE IF NOT EXISTS competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50) NULL,
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),
    CONSTRAINT fk_competition_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

-- 3. Complexes Table
CREATE TABLE IF NOT EXISTS complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

-- 4. Venues Table
CREATE TABLE IF NOT EXISTS venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    CONSTRAINT fk_venue_complex
        FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)
);

-- 5. Competitor Rankings Table
CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    competitor_id VARCHAR(50) NOT NULL,
    competitor_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    country_code CHAR(3),
    `rank` INT NOT NULL,
    movement INT NOT NULL DEFAULT 0,
    points INT NOT NULL DEFAULT 0,
    competitions_played INT NOT NULL DEFAULT 0,
    ranking_date DATE
);

-- Indexes
CREATE INDEX idx_competitions_category
ON competitions(category_id);

CREATE INDEX idx_competitions_parent
ON competitions(parent_id);

CREATE INDEX idx_venues_complex
ON venues(complex_id);

CREATE INDEX idx_rankings_rank
ON competitor_rankings(`rank`);
