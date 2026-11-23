USE tennis_analytics;

-- 01. Top 10 Competitors
SELECT competitor_name, country, `rank`, points
FROM competitor_rankings
ORDER BY `rank` ASC
LIMIT 10;

-- 02. Complete Player Rankings
SELECT *
FROM competitor_rankings
ORDER BY `rank` ASC;

-- 03. Country-wise Competitor Count
SELECT country, COUNT(*) AS total_competitors
FROM competitors
GROUP BY country
ORDER BY total_competitors DESC;

-- 04. Country-wise Average Ranking Points
SELECT country, ROUND(AVG(points), 2) AS avg_points
FROM competitor_rankings
GROUP BY country
ORDER BY avg_points DESC;

-- 05. Country-wise Total Ranking Points
SELECT country, SUM(points) AS total_points
FROM competitor_rankings
GROUP BY country
ORDER BY total_points DESC;

-- 06. Best Ranking by Country
SELECT country, MIN(`rank`) AS best_rank
FROM competitor_rankings
GROUP BY country
ORDER BY best_rank ASC;

-- 07. Ranking Movement Analysis
SELECT movement, COUNT(*) AS competitor_count,
       ROUND(AVG(points), 2) AS avg_points
FROM competitor_rankings
GROUP BY movement
ORDER BY movement DESC;

-- 08. Ranking Distribution
SELECT
    CASE
        WHEN `rank` BETWEEN 1 AND 10 THEN 'Top 10'
        WHEN `rank` BETWEEN 11 AND 50 THEN '11-50'
        WHEN `rank` BETWEEN 51 AND 100 THEN '51-100'
        ELSE 'Above 100'
    END AS ranking_group,
    COUNT(*) AS total_players
FROM competitor_rankings
GROUP BY ranking_group
ORDER BY MIN(`rank`);

-- 09. Competitor Country Details
SELECT country, country_code,
       COUNT(*) AS total_competitors
FROM competitors
GROUP BY country, country_code
ORDER BY total_competitors DESC;

-- 10. Competitions by Category
SELECT cat.category_name,
       COUNT(c.competition_id) AS total_competitions
FROM categories cat
LEFT JOIN competitions c
ON cat.category_id = c.category_id
GROUP BY cat.category_id, cat.category_name
ORDER BY total_competitions DESC;

-- 11. Competitions by Gender
SELECT gender, COUNT(*) AS total_competitions
FROM competitions
GROUP BY gender;

-- 12. Competitions by Event Type
SELECT type, COUNT(*) AS total_competitions
FROM competitions
GROUP BY type;

-- 13. Complete Competition Details
SELECT c.competition_id, c.competition_name,
       c.type, c.gender, cat.category_name
FROM competitions c
LEFT JOIN categories cat
ON c.category_id = cat.category_id
ORDER BY cat.category_name, c.competition_name;

-- 14. Venues by Country
SELECT country_name, country_code,
       COUNT(*) AS total_venues
FROM venues
GROUP BY country_name, country_code
ORDER BY total_venues DESC;

-- 15. Venues by City
SELECT city_name, country_name,
       COUNT(*) AS total_venues
FROM venues
GROUP BY city_name, country_name
ORDER BY total_venues DESC;

-- 16. Venues by Complex
SELECT cx.complex_name,
       COUNT(v.venue_id) AS total_venues
FROM complexes cx
LEFT JOIN venues v
ON cx.complex_id = v.complex_id
GROUP BY cx.complex_id, cx.complex_name
ORDER BY total_venues DESC;

-- 17. Complexes Without Venues
SELECT cx.complex_id, cx.complex_name
FROM complexes cx
LEFT JOIN venues v
ON cx.complex_id = v.complex_id
WHERE v.venue_id IS NULL;

-- 18. Rankings by Ranking Date
SELECT ranking_date,
       COUNT(*) AS total_players,
       AVG(points) AS average_points
FROM competitor_rankings
GROUP BY ranking_date
ORDER BY ranking_date DESC;

-- 19. Top 3 Competitors Per Country
SELECT country, competitor_name, `rank`, points
FROM (
    SELECT country, competitor_name, `rank`, points,
           ROW_NUMBER() OVER (
               PARTITION BY country
               ORDER BY `rank` ASC
           ) AS row_num
    FROM competitor_rankings
) ranked
WHERE row_num <= 3
ORDER BY country, `rank`;

-- 20. Competitors Without Ranking Records
SELECT c.competitor_id, c.name, c.country
FROM competitors c
LEFT JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
WHERE r.competitor_id IS NULL;

-- 21. Ranking Records Without Competitor Master Record
SELECT r.competitor_id, r.competitor_name, r.country
FROM competitor_rankings r
LEFT JOIN competitors c
ON r.competitor_id = c.competitor_id
WHERE c.competitor_id IS NULL;

-- 22. Overall Database KPI Summary
SELECT
    (SELECT COUNT(*) FROM competitors) AS total_competitors,
    (SELECT COUNT(*) FROM competitor_rankings) AS total_rankings,
    (SELECT COUNT(*) FROM categories) AS total_categories,
    (SELECT COUNT(*) FROM competitions) AS total_competitions,
    (SELECT COUNT(*) FROM venues) AS total_venues,
    (SELECT COUNT(*) FROM complexes) AS total_complexes;