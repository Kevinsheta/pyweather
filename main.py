import streamlit as st
import os
from streamlit_cookies_manager import EncryptedCookieManager
import json
from database import *
from weather import *
from visualization import *
from notification import *
from map import *
from news import *
from ui import *

# Set up cookies manager.
cookie_password = os.environ.get("COOKIE_PASSWORD", "default_fallback_password")
cookies= EncryptedCookieManager(prefix='2', password= cookie_password)
if not cookies.ready():
    st.stop() 

# Handle exception when accessing cookies
try:
    cookie_history = json.loads(cookies.get('search_history', '[]'))  # Use get() with default value
except Exception as e:
    st.error(f"Failed to load cookies: {e}")
    cookie_history = []

if 'search_history' not in st.session_state:
    st.session_state['search_history']= cookie_history

# Save the (updated) history back into cookies
def update_cookies(history):
    try:
        cookies['search_history'] = json.dumps(history)
    except Exception as e:
        st.error(f"Error saving cookies: {e}")

def save_history(city):
    # Prevent duplicates
    if city in [entry["City"] for entry in st.session_state['search_history']]:
        return  
    
    # Add valid city to history
    st.session_state['search_history'].insert(0, {"City": city})
    st.session_state['search_history'] = st.session_state['search_history'][:10]  

    update_cookies(st.session_state['search_history']) 

# Clear search history
def clear_history():
    st.session_state['search_history']= []
    update_cookies(st.session_state['search_history'])

    save_history(st.session_state["city_input"])

    st.sidebar.success("Search history cleared.")



def main():
    
    if 'map_click' not in st.session_state:
        st.session_state['map_click']= None

    if "view" not in st.session_state:
        st.session_state["view"] = "Weather Data"

    if "city_input" not in st.session_state:
        st.session_state["city_input"] = ""
        save_history(st.session_state["city_input"])
    
    if "weather_needs_update" not in st.session_state:
        st.session_state["weather_needs_update"] = True  
    

    # Sidebar: Search for another city
    st.sidebar.title("🔍 Search Another City")
    search_city = st.sidebar.text_input("Enter city name:", placeholder="E.g., Tokyo, Berlin")
    
    # Ensure search history exists
    if "search_history" not in st.session_state:
        st.session_state["search_history"] = []

    
    # Handle user input from the sidebar
    if search_city and search_city != st.session_state.get("city_input", ""):      
        st.session_state["city_input"] = search_city
        st.session_state["weather_needs_update"] = True
        save_history(search_city)
        st.sidebar.success(f"✅ Showing weather for: {search_city}")
        
        # Set the active tab to "Weather Data"
        st.session_state["active_tab"] = 0  
        
        st.rerun()

    # Search History Selection
    search_history = [entry["City"] for entry in st.session_state["search_history"] if entry["City"]]
    
    # Search History Selection
    selected_city = st.sidebar.selectbox(
        "Search History",
        search_history,
        index=None,
        key="city_history"
    )
   
    if selected_city and selected_city != st.session_state["city_input"]:
        st.session_state["city_input"] = selected_city
        st.session_state["weather_needs_update"] = True  
        
        st.sidebar.success(f"✅ Showing weather for: {selected_city}")
        
        # Set the active tab to "Weather Data"
        st.session_state["active_tab"] = 0  # Assuming "Weather Data" is the first tab (index 0)
        
    st.sidebar.button("Clear Search History", on_click=clear_history) 

    # Set the default active tab if not already set
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = 0  
        
    tab1, tab2, tab3, tab4, tab5= st.tabs(["🌦 Weather Data", "📊 Weather Data Visualization","🌍 Map ", "📰 Weather News", "📂 Weather Dataset"])
        
    
    with tab1:
        st.write("### 🌦 Weather Data Analysis")   
        st.write("##### 📍 Your Location")
        
        city = st.text_input("Enter your city:", value=st.session_state["city_input"], placeholder="E.g., New York, Paris") 

        # Handle user input from the main page
        if city and city != st.session_state["city_input"]:
            st.session_state["city_input"] = city
            st.session_state["weather_needs_update"] = True
            save_history(city)
            st.rerun()
        
        unit= st.radio('Select Temperature Unit:', ['Celsius (°C)', 'Fahrenheit (°F)'])
        if city and unit:
            unit= unit[0]
            with st.spinner("Just Wait!!"): 
                time.sleep(3)
            
            st.write(f"Fetching weather data for: {city}")

            weather_data= current_weather(city, unit)
            forecast_data= fetch_forecast_data(city)

            if weather_data and forecast_data:
                save_current_weather(city, weather_data)
                save_forecast_weather(city, forecast_data)

            # Fetch coordinates of the city
            lat, lon= fetch_coordinates(city)        

            if lat is not None and lon is not None and weather_data:

                display_weather_data(forecast_data, city, unit, data_type= 'forecast')
                
                st.markdown("### <br>🌡️ 24-Hourly Data", unsafe_allow_html=True)  
                
                hourly_data= fetch_weather_data(city, unit)
                if hourly_data:
                    weather_card(hourly_data)

                    st.markdown("<br>", unsafe_allow_html=True) 

                    st.write('### <br>🚨 Weather Alert Message', unsafe_allow_html= True)
                    display_notification(city, hourly_data)

            else:
                st.error("Could not fetch weather data. Please check the city name or try again later.")
        else:
            st.info('Please enter a city name.')

    with tab2:
        st.write("### 📊 Weather Data Visualization")
        plot_weather_graph(city, unit)
    
    with tab3:
        st.write("### 🌍 Location Map")
        
        # Fetch coordinates again if city is entered
        lat, lon= fetch_coordinates(city) if city else (None, None)

        if city and lat is not None and lon is not None:
            display_map(city, lat, lon, weather_data)
        else:
            st.info("Please enter a city name to display the map.")

    with tab4:
        st.title("🌦 Weather News")
        with st.spinner("Fetching weather news..."):
            articles = fetch_weather_news()
        display_all_news(articles)
    
    with tab5:
        st.write("### 📂 Stored Weather Data")
        display_weather_tables()


    cookies.save()


if __name__ == "__main__":
    main()