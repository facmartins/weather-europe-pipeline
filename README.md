# 🌤️ European Weather Data Pipeline

An ETL data engineering project that extracts 7-day weather forecast data
for 8 European cities from the Open-Meteo API, transforms it using Python
and Pandas, and loads it into SQL Server for analysis.

---

## 🛠️ Technologies
- Python 3.14
- Pandas
- Requests
- PyODBC
- SQL Server
- Open-Meteo API (free, no API key required)

---

## 🏗️ Pipeline Architecture
Open-Meteo API → Extract → Transform → Load → SQL Server

---

## 🌍 Cities Covered
Portugal: Lisbon, Porto
Spain: Madrid
France: Paris
United Kingdom: London
Germany: Berlin
Italy: Rome
Netherlands: Amsterdam

---

## 📋 Requirements Specification

### Objective
Build an ETL pipeline that extracts 7-day weather forecast data from the
Open-Meteo API for 8 European cities, transforms and cleans it, and loads
it into SQL Server for analysis.

### Data Source
- API: Open-Meteo
- Endpoint: /v1/forecast
- Format: JSON
- Frequency: Manual
- API Key: Not required

### Functional Requirements
- Extract weather data for 8 European cities
- Remove duplicate and missing data
- Convert dates to correct format
- Round values to 2 decimal places
- Load data into SQL Server
- Enable analysis via SQL queries

### Business Rules
- Remove records with missing temperature, wind or precipitation
- Precipitation and wind rounded to 2 decimal places
- Temperature rounded to 2 decimal places

---

## 📁 Project Structure
├── pipeline.py           # ETL pipeline
├── config.py             # Cities and server config (not included)
├── create_tables.sql     # SQL Server table creation
├── analysis_queries.sql  # SQL analysis queries
└── README.md             # Project documentation
---

## 📊 SQL Analysis

### Hottest City
SELECT c.name, c.country, ROUND(AVG(w.temperature), 2) AS avg_temperature
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY avg_temperature DESC

### Windiest City
SELECT c.name, c.country, ROUND(AVG(w.wind_speed), 2) AS avg_wind
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY avg_wind DESC

### Most Rainy City
SELECT c.name, c.country, ROUND(SUM(w.precipitation), 2) AS total_precipitation
FROM Weather w
JOIN City c ON w.city_id = c.id
GROUP BY c.name, c.country
ORDER BY total_precipitation DESC

---

## ⚙️ How to Run
1. Clone the repository
2. Install dependencies:
pip install pandas requests pyodbc

3. Create a config.py file:
CITIES = [...]
SERVER = "your_server"
DATABASE = "WeatherEurope"

4. Create the database and tables using create_tables.sql
5. Run the pipeline:
python pipeline.py



## 👩‍💻 Author
Flávia de Castro | Data Engineering Student
Portugal 🇵🇹
LinkedIn: https://www.linkedin.com/in/flaviadecastroprojects