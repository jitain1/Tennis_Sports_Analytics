CREATE TABLE IF NOT EXISTS competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    country_code CHAR(3),
    abbreviation VARCHAR(10)
) ENGINE=InnoDB;

INSERT INTO categories (category_id, category_name) VALUES
('cat_atp', 'ATP'),
('cat_wta', 'WTA'),
('cat_itf', 'ITF')
ON DUPLICATE KEY UPDATE category_name=VALUES(category_name);

INSERT INTO competitions
(competition_id, competition_name, parent_id, type, gender, category_id) VALUES
('comp_atp_1000', 'ATP Masters 1000', NULL, 'singles', 'men', 'cat_atp'),
('comp_atp_500', 'ATP 500', NULL, 'singles', 'men', 'cat_atp'),
('comp_wta_1000', 'WTA 1000', NULL, 'singles', 'women', 'cat_wta'),
('comp_itf_men', 'ITF Men', NULL, 'singles', 'men', 'cat_itf'),
('comp_itf_women', 'ITF Women', NULL, 'singles', 'women', 'cat_itf')
ON DUPLICATE KEY UPDATE competition_name=VALUES(competition_name);

INSERT INTO complexes (complex_id, complex_name) VALUES
('cx_001', 'National Tennis Complex'),
('cx_002', 'City Sports Complex'),
('cx_003', 'International Tennis Centre')
ON DUPLICATE KEY UPDATE complex_name=VALUES(complex_name);

INSERT INTO venues
(venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id) VALUES
('v_001', 'Central Court', 'London', 'United Kingdom', 'GBR', 'Europe/London', 'cx_001'),
('v_002', 'Court 2', 'London', 'United Kingdom', 'GBR', 'Europe/London', 'cx_001'),
('v_003', 'Main Stadium', 'New York', 'United States', 'USA', 'America/New_York', 'cx_002'),
('v_004', 'Arena Court', 'Melbourne', 'Australia', 'AUS', 'Australia/Melbourne', 'cx_003'),
('v_005', 'Central Arena', 'Paris', 'France', 'FRA', 'Europe/Paris', 'cx_003')
ON DUPLICATE KEY UPDATE venue_name=VALUES(venue_name);

INSERT INTO competitors
(competitor_id, name, country, country_code, abbreviation) VALUES
('sample_001', 'Alex Morgan / Ben Carter', 'United States', 'USA', 'MOR/CAR'),
('sample_002', 'Daniel Smith / Ryan Wilson', 'United Kingdom', 'GBR', 'SMI/WIL'),
('sample_003', 'Lucas Martin / Hugo Bernard', 'France', 'FRA', 'MAR/BER'),
('sample_004', 'Marco Rossi / Luca Bianchi', 'Italy', 'ITA', 'ROS/BIA'),
('sample_005', 'Mateo Garcia / Pablo Lopez', 'Spain', 'ESP', 'GAR/LOP'),
('sample_006', 'Oliver Brown / Jack Taylor', 'Australia', 'AUS', 'BRO/TAY'),
('sample_007', 'Ivan Petrov / Nikolai Ivanov', 'Croatia', 'CRO', 'PET/IVA'),
('sample_008', 'Noah Johnson / Liam Davis', 'Canada', 'CAN', 'JOH/DAV'),
('sample_009', 'Arjun Mehta / Rohan Sharma', 'India', 'IND', 'MEH/SHA'),
('sample_010', 'Kenji Sato / Yuki Tanaka', 'Japan', 'JPN', 'SAT/TAN')
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO competitor_rankings
(competitor_id, competitor_name, country, country_code, `rank`, movement, points, competitions_played, ranking_date)
SELECT c.competitor_id, c.name, c.country, c.country_code,
       d.ranking, d.movement, d.points, d.played, '2026-11-23'
FROM competitors c
JOIN (
    SELECT 'sample_001' id, 1 ranking, 0 movement, 9500 points, 18 played UNION ALL
    SELECT 'sample_002', 2, 1, 8700, 20 UNION ALL
    SELECT 'sample_003', 3, -1, 8100, 17 UNION ALL
    SELECT 'sample_004', 4, 2, 7600, 19 UNION ALL
    SELECT 'sample_005', 5, 0, 7100, 16 UNION ALL
    SELECT 'sample_006', 6, -2, 6500, 21 UNION ALL
    SELECT 'sample_007', 7, 1, 5900, 15 UNION ALL
    SELECT 'sample_008', 8, 0, 5300, 18 UNION ALL
    SELECT 'sample_009', 9, 3, 4700, 14 UNION ALL
    SELECT 'sample_010', 10, -1, 4200, 13
) d ON c.competitor_id=d.id
WHERE NOT EXISTS (
    SELECT 1 FROM competitor_rankings r
    WHERE r.competitor_id=c.competitor_id
);
