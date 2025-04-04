import requests
import base64
import streamlit as st
from datetime import datetime
import numpy as np
from meteostat import Point, Daily
import pandas as pd
import pytz
from config import API_key
from ui import convert_to_fahrenheit

def current_weather(city, unit= 'C'):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_key}&unitGroup=metric"
    try:
        response = requests.get(url)
        data = response.json()
        weather = data.get('currentConditions', {})
        if weather:
            temperature = weather.get('temp', 'N/A')
            humidity = weather.get('humidity', 'N/A')
            dew_point = weather.get('dew', 'N/A')
            precipitation = weather.get('precip', '0')
            wind_speed = weather.get('windspeed', 'N/A')
            conditions = weather.get('conditions', 'N/A')
            icon = weather.get('icon', 'default')  
            
            # Fetch the timezone and convert time
            timezone= data.get('timezone', 'UTC')  # Get timezone from API
            city_time= datetime.now(pytz.utc).astimezone(pytz.timezone(timezone)) # Convert UTC to local time
            
            if unit == 'F':
                temperature= convert_to_fahrenheit(temperature)

            def encode_image_to_base64(file_path):
                try:
                    with open(file_path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode("utf-8")
                except FileNotFoundError:
                    return None

            # Generate dynamic image
            if icon != 'N/A':
                icon_url = f"Icon/{icon}.png"
                base64_image = encode_image_to_base64(icon_url)
                if base64_image:
                    image_html = f'<img src="data:image/png;base64,{base64_image}" alt="Weather Icon" class="weather-icon1">'
                else:
                    image_html = '<p>No Icon Available</p>'
            else:
                image_html = '<p>No Icon Available</p>'


            # HTML for layout
            st.markdown(
                f"""    
                🏠 Results for: {data.get('resolvedAddress', 'N/A')} | Local Time: {city_time.strftime('%Y-%m-%d %I:%M:%S %p')}\n
                **Sunrise:** {datetime.strptime(data['days'][0].get('sunrise', 'N/A'), "%H:%M:%S").strftime("%I:%M %p") if data['days'][0].get('sunrise') else 'N/A'} | 
                **Sunset:** {datetime.strptime(data['days'][0].get('sunset', 'N/A'), "%H:%M:%S").strftime("%I:%M %p") if data['days'][0].get('sunset') else 'N/A'}
                
                <style>
                    .weather-container1 {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: black;
                        color: white;
                        padding: 20px;
                        border-radius: 10px;
                        font-family: Arial, sans-serif;
                        max-width: 900px;
                        margin: 20px auto;
                        gap: 15px;
                    }}
                    .icon-temperature-container {{
                        display: flex;
                        justify-content: center;  /* Center items on mobile */
                        align-items: center;
                    }}
                    .weather-icon1 {{
                        width: 80px;
                        height: auto;
                        margin-right: 8px;
                    }}
                    .temperature {{
                        font-size: 35px !important;
                        font-weight: bold;
                    }}
                    .details-container {{
                        flex: 20px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        font-size: 13px;
                    }}
                    .details {{
                        font-size: 16px;
                        color: #ccc;
                        margin: 5px 0;
                    }}
                    .right-section {{
                        text-align: center;
                        margin-top: 15px;
                        flex: 1;
                    }}
                    .right-section p {{
                        margin: 5px 0;
                        font-size: 16px;
                    }}
                    
                    /* Responsive design for mobile devices */
                    @media screen and (max-width: 600px) {{
                    .weather-container1 {{
                        padding: 10px;
                        max-width: 100%;  /* Allow the container to take full width on mobile */
                    }}

                    .icon-temperature-container {{
                        flex-direction: column;  /* Stack icon and temperature vertically */
                    }}

                    .temperature {{
                        font-size: 28px;
                    }}

                    .details-container {{
                        font-size: 12px;
                    }}
                }}
                </style>
                <div class="weather-container1">
                    <!-- Icon and Temperature Container -->
                    <div class="icon-temperature-container">
                        {image_html}
                        <p class="temperature">{temperature}°{unit}</p>
                    </div>
                    <!-- Details Container -->
                    <div class="details-container">
                        <p class="details"><b>Precipitation:</b> {precipitation}%</p>
                        <p class="details"><b>Humidity:</b> {humidity}%</p>
                        <p class="details"><b>Wind Speed:</b> {wind_speed} km/h</p>
                        <p class="details"><b>Dew Point:</b> {dew_point}°C</p>
                    </div>
                    <!-- Right Section -->
                    <div class="right-section">
                        <p>{city_time.strftime('%A, %I:%M %p')}</p>
                        <p>Weather: {icon}</p>
                        <p>{conditions}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Save current weather data to history
            weather_data = {
                "Temperature (°C)": temperature,
                "Humidity (%)": humidity,
                "Dew Point (°C)": dew_point,
                "Precipitation (mm)": precipitation,
                "Wind Speed (km/h)": wind_speed,
                "Conditions": conditions,
            }

            return weather_data
        else:
            st.error("Weather data unavailable. Check the city name and API key.")
    except Exception as e:
        st.error(f"Error: {e}")
        
def fetch_forecast_data(city):
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_key}"
        try: 
            response= requests.get(url)
            data= response.json()
            forecast_data= data.get('days', [])

            if not forecast_data:
                st.error('Forecast data unavailable.')
                return []
            
            processed_forecast= []
            for day in forecast_data[:7]:  
                processed_forecast.append({
                    'Date': day.get('datetime', 'N/A'),
                    'Tempmax': day.get('tempmax', 'N/A'),
                    'Tempmin': day.get('tempmin', 'N/A'),
                    'Humidity': day.get('humidity', 'N/A'),
                    'Conditions': day.get('conditions', 'N/A'),
                    'Feelslike': day.get('feelslike', 'N/A'),
                    'Wind': day.get('windspeed', 'N/A'),
                    'Wind Direction': day.get('winddir', 'N/A'),
                    'icon': day.get('icon', 'defualt')
                })

            return processed_forecast

        except Exception as e:
            st.error(f'Error fetching forecast data: {e}')
            return []

def fetch_coordinates(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_key}"
    try:
        response = requests.get(url).json()
        if 'latitude' in response and 'longitude' in response:
            return response['latitude'], response['longitude']
        else:
            st.error(f"Error: Could not find coordinates for '{city}'. Please check the city name.")
            return None, None
    except Exception:
        st.info("Please enter a city name.")
        return None, None

def estimate_relative_humidity(tavg, tmin, tmax):
    if tmax != tmin:
        rh = 100 * (tavg - tmin) / (tmax - tmin)
        return max(0, min(rh, 100))  # Clamp RH between 0 and 100%
    else:
        return np.nan

def calculate_dew_point(tavg, rh):
    if pd.notnull(rh) and pd.notnull(tavg):
        a = 17.27
        b = 237.7
        gamma = np.log(rh / 100) + (a * tavg) / (b + tavg)
        dew_point = (b * gamma) / (a - gamma)
        return round(dew_point, 2)
    else:
        return np.nan

def fetch_historical_data(city, start_date, end_date):
    lat, lon = fetch_coordinates(city)
    if lat is None or lon is None:
        return None

    location = Point(lat, lon)
    data = Daily(location, start_date, end_date)
    data = data.fetch()

    if data.empty:
        st.error("No historical data available for the selected date range.")
        return None

    # Reset index to have 'time' as a column
    data = data.reset_index()

    # Calculate Relative Humidity
    data['Relative Humidity (%)'] = data.apply(
        lambda row: estimate_relative_humidity(row['tavg'], row['tmin'], row['tmax'])
        if pd.notnull(row['tavg']) and pd.notnull(row['tmin']) and pd.notnull(row['tmax'])
        else np.nan,
        axis=1
    )

    # Calculate Dew Point
    data['Dew Point (°C)'] = data.apply(
        lambda row: calculate_dew_point(row['tavg'], row['Relative Humidity (%)']),
        axis=1
    )

    return data

# Function to fetch weather data
def fetch_weather_data(city, unit= 'C'):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_key}&unitGroup=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'timezone' not in data:
            return []

        timezone= data['timezone']

        # Get the hour
        city_time= datetime.now(pytz.timezone(timezone)) 
        current_hour= city_time.hour 
        
        # Extract hourly forecast data
        hourly_data = data['days'][0].get('hours', [])

        # Filter the data to start from the current hour
        hourly_data= [hour for hour in hourly_data if int(hour['datetime'].split(':')[0]) >= current_hour]

        # If there are fewer than 24 hours left in today, add missing hours from tomorrow
        if len(hourly_data) < 24:
            next_day_hour= data['days'][1].get('hours', []) # Get next day's hourly data
            remaining_hour= 24 - len(hourly_data)
            hourly_data.extend(next_day_hour[:remaining_hour])
        
        # Convert to required format
        weather_data = []
        for hour in hourly_data:
            time = datetime.strptime(hour['datetime'], "%H:%M:%S").strftime("%I %p")
            temperature = hour.get('temp', 'N/A')
            humidity = hour.get('humidity', 'N/A')
            precipitation = hour.get('precip', 'N/A')
            rain_prob = hour.get('precipprob', 0)
            snow_prob = hour.get('snowprob', 0)
            fog_prob = hour.get('fog', 0)
            conditions = hour.get('conditions', 'N/A')
            icon = hour.get('icon', 'clear-day') 

            if unit == 'F':
                temperature= convert_to_fahrenheit(temperature)
            
            # Assume icon_path is base64-encoded icon; replace with correct method for real icons
            icon_file_path = f"Icon/{icon}.png"
            try:
                with open(icon_file_path, "rb") as img_file:
                    icon_base64 = base64.b64encode(img_file.read()).decode("utf-8")
            except FileNotFoundError:
                icon_base64 = ""  
            
            weather_data.append({
            "time": time,   
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "conditions": conditions,
            "rain_probability": rain_prob,
            "snow_probability": snow_prob,
            "fog_probability": fog_prob,
            "icon_path": icon_base64
        })

        return weather_data

    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return []

def get_forecast_data(city):
    if not city:
        st.error("Please enter a city name.")
        return None

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_key}"
    
    try:
        response = requests.get(url)

        # Check if response is valid
        if response.status_code != 200:
            st.info(f"Error fetching weather data: {response.status_code} - {response.reason}")
            return None
        
        # Try parsing JSON
        data = response.json()

        if 'days' in data:
            forecast_data = pd.DataFrame(data['days'])
            return forecast_data
        else:
            st.info("No forecast data found for this city.")
            return None

    except requests.exceptions.RequestException as e:
        st.info(f"Network error: {e}")
        return None
    except ValueError:
        st.info("Invalid response from the server. Please check the city name and try again.")
        return None
    
def process_forecast_data(forecast_data):
    forecast_data['date'] = pd.to_datetime(forecast_data['datetime'])
    forecast_data.set_index('date', inplace=True)
    forecast_data.rename(columns={
        'temp': 'Average Temperature (°C)',
        'tempmin': 'Minimum Temperature (°C)',
        'tempmax': 'Maximum Temperature (°C)',
        'precip': 'Precipitation (mm)',
        'snow': 'Snowfall (mm)',
        'windspeed': 'Wind Speed (m/s)',
        "wdir": "Wind Direction (°)",
        "pres": "Pressure (hPa)",
        'humidity': 'Relative Humidity (%)',
        'dew': 'Dew Point (°C)'
    }, inplace=True)
    return forecast_data