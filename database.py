import streamlit as st
import pandas as pd
import sqlite3

# Database setup
db_file = "weather_data.db"
conn = sqlite3.connect(db_file, check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''
    CREATE TABLE IF NOT EXISTS current_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        temperature REAL,
        humidity REAL,
        dew_point REAL,
        precipitation REAL,
        wind_speed REAL,
        conditions TEXT,
        UNIQUE(city, date)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS forecast_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        temp_max REAL,
        temp_min REAL,
        humidity REAL,
        conditions TEXT,
        feels_like REAL,
        wind REAL,
        wind_direction TEXT,
        icon TEXT,
        UNIQUE(city, date)
    )
''')

conn.commit()

def save_current_weather(city, weather_data):
    today_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    c.execute('''
        INSERT INTO current_weather (city, date, temperature, humidity, dew_point, precipitation, wind_speed, conditions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(city, date) DO UPDATE SET 
            temperature = excluded.temperature,
            humidity = excluded.humidity,
            dew_point = excluded.dew_point,
            precipitation = excluded.precipitation,
            wind_speed = excluded.wind_speed,
            conditions = excluded.conditions
    ''', (city, today_date, weather_data['Temperature (°C)'], weather_data['Humidity (%)'], 
        weather_data['Dew Point (°C)'], weather_data['Precipitation (mm)'], 
        weather_data['Wind Speed (km/h)'], weather_data['Conditions']))
    conn.commit()


def save_forecast_weather(city, forecast_data):
    for day in forecast_data:
        c.execute('''INSERT OR IGNORE INTO forecast_weather (city, date, temp_max, temp_min, humidity, conditions, feels_like, wind, wind_direction, icon)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (city, day['Date'], day['Tempmax'], day['Tempmin'], day['Humidity'], day['Conditions'], day['Feelslike'], day['Wind'],
                   day['Wind Direction'], day['icon']))
    conn.commit()

def get_weather_data():
    current_df = pd.read_sql_query("SELECT date, city, temperature, humidity, dew_point, precipitation, wind_speed, conditions FROM current_weather", conn)
    forecast_df = pd.read_sql_query("SELECT date, city, temp_max, temp_min, humidity, feels_like, wind, wind_direction, conditions FROM forecast_weather", conn)
    return current_df, forecast_df

def download_csv(df, filename):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=f"Download {filename}", data=csv, file_name=filename, mime='text/csv')

def display_weather_tables():
    current_df, forecast_df = get_weather_data()
    
    with st.expander("📌 Current Weather Data"):
        st.dataframe(current_df)
        download_csv(current_df, "current_weather.csv")
    
    with st.expander("📅 7-Day Forecast Data"):
        st.dataframe(forecast_df)
        download_csv(forecast_df, "forecast_weather.csv")