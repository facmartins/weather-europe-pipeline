-- -------------------------
-- ANALYSIS QUERIES
-- European Weather Pipeline
-- -------------------------

-- Hottest city
SELECT c.name, c.country, ROUND(AVG(w.temperature), 2) AS avg_temperature
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY avg_temperature DESC

-- Windiest city
SELECT c.name, c.country, ROUND(AVG(w.wind_speed), 2) AS avg_wind
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY avg_wind DESC

-- Most rainy city
SELECT c.name, c.country, ROUND(SUM(w.precipitation), 2) AS total_precipitation
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY total_precipitation DESC