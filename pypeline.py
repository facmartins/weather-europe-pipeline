# IMPORT LIBRARIES
import requests
import pandas as pd
import pyodbc
from config import CITIES, SERVER, DATABASE

# EXTRACT
all_data = []

for city in CITIES:
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={city['latitude']}&longitude={city['longitude']}"
        f"&daily=temperature_2m_max,windspeed_10m_max,precipitation_sum"
        f"&timezone=auto&forecast_days=7"
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        daily = data["daily"]

        for i in range(len(daily["time"])):
            all_data.append({
                "name": city["name"],
                "country": city["country"],
                "date": daily["time"][i],
                "temperature": daily["temperature_2m_max"][i],
                "wind": daily["windspeed_10m_max"][i],
                "precipitation": daily["precipitation_sum"][i]
            })
        print(f"✅ {city['name']} — data extracted!")
    else:
        print(f"❌ Error {city['name']}: {response.status_code}")

print(f"\n✅ Total records extracted: {len(all_data)}")

# TRANSFORM
df = pd.DataFrame(all_data)
df = df.drop_duplicates()
df = df.dropna(subset=["temperature", "wind", "precipitation"])
df["date"] = pd.to_datetime(df["date"])
df["temperature"] = df["temperature"].round(2)
df["wind"] = df["wind"].round(2)
df["precipitation"] = df["precipitation"].round(2)

print("\n📊 Transformed data:")
print(df.head(10))
print(f"\n✅ Total records after transform: {len(df)}")

# LOAD
print("🔄 Starting Load...")

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Insert cities
for city in CITIES:
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM City WHERE name = ?)
        INSERT INTO City (name, country, latitude, longitude)
        VALUES (?, ?, ?, ?)
    """, city["name"], city["name"], city["country"], city["latitude"], city["longitude"])

conn.commit()

# Get city IDs
city_ids = {}
cursor.execute("SELECT id, name FROM City")
for row in cursor.fetchall():
    city_ids[row.name] = row.id

# Insert weather data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Weather (city_id, date, temperature, precipitation, wind_speed)
        VALUES (?, ?, ?, ?, ?)
    """, city_ids[row["name"]], row["date"], row["temperature"], row["precipitation"], row["wind"])

conn.commit()
cursor.close()
conn.close()

print("\n✅ Data loaded into SQL Server successfully!")