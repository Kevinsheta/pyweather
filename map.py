import folium
import streamlit as st
from streamlit_folium import st_folium

def display_map(city, lat, lon, weather_data):
    if not city:
        st.error("Please enter a city name.")
        return  
    
    if lat is None or lon is None:
        st.error(f"Could not fetch coordinates for {city}.")
        return  
    
    # Check if weather_data is None
    if weather_data is None:
        st.error("Weather data is not available.")
        return  

    # Initialize the map at the city's location
    weather_map = folium.Map(location=[lat, lon], zoom_start=10)

    # Add a marker with weather details
    popup_content = f"""
    <b>City:</b> {city}<br>
    <b>Temperature:</b> {weather_data.get('Temperature (°C)', 'N/A')} (°C)<br>
    <b>Humidity:</b> {weather_data.get('Humidity (%)', 'N/A')}%<br>
    <b>Conditions:</b> {weather_data.get('Conditions', 'N/A')}<br>
    """
    
    folium.Marker(
        location=[lat, lon],
        tooltip=popup_content,
        icon=folium.Icon(color='blue', icon='cloud'),
    ).add_to(weather_map)

    # Handle map interaction using st_folium
    map_data = st_folium(weather_map, height=500, width=800, returned_objects=["last_clicked"])

    # Update session state with clicked location if it exists
    if map_data and map_data.get("last_clicked"):
        st.session_state['map_click'] = map_data["last_clicked"]['lat'], map_data["last_clicked"]['lng']