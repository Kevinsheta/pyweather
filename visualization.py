import streamlit as st
from datetime import datetime, timedelta
import time
import base64
from ui import convert_to_fahrenheit, plot_graph
from weather import fetch_historical_data, get_forecast_data, process_forecast_data

def plot_weather_graph(city, unit):
    # Initialize session state for weather type if not set
    if "weather_type" not in st.session_state:
        st.session_state["weather_type"] = "Forecast Weather"  # Default value

    tab1, tab2= st.tabs(["Historical Weather", "Forecast Weather"])

    
    with tab1:
        start_date = st.date_input("Select Start Date: ", datetime.now() - timedelta(days=30))
        end_date = st.date_input("Select End Date: ", datetime.now())

        # Convert to datetime objects
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        if start_date > end_date:
            st.error("Start date must be before end date.")
        else:
            data = fetch_historical_data(city, start_date, end_date)

            if data is not None and not data.empty: 
                with st.spinner("Just Wait!!"):
                    time.sleep(3)

                data = data.rename(columns={
                    "time": "datetime",
                    "tavg": f"Average Temperature (°C)",
                    "tmin": f"Minimum Temperature (°C)",
                    "tmax": f"Maximum Temperature (°C)",
                    "prcp": "Precipitation (mm)",
                    "snow": "Snowfall (mm)",
                    "wspd": "Wind Speed (km/h)",
                    "wdir": "Wind Direction (°)",
                    "pres": "Pressure (hPa)",
                    'humidity': 'Relative Humidity (%)',
                    'dew': 'Dew Point (°C)'
                })

                if unit == "F":
                    data["Average Temperature (°F)"] = convert_to_fahrenheit(data["Average Temperature (°C)"])
                    data["Minimum Temperature (°F)"] = convert_to_fahrenheit(data["Minimum Temperature (°C)"])
                    data["Maximum Temperature (°F)"] = convert_to_fahrenheit(data["Maximum Temperature (°C)"])

                    data.drop(columns=["Average Temperature (°C)", "Minimum Temperature (°C)", "Maximum Temperature (°C)"], inplace=True)
                    temp_unit = "(°F)"
                else:
                    temp_unit = "(°C)"

                data = data[["datetime"] + [col for col in data.columns if col != "datetime"]]

                st.write('### Historical Data')
                
                available_columns = [
                    f"Average Temperature {temp_unit}",
                    f"Minimum Temperature {temp_unit}",
                    f"Maximum Temperature {temp_unit}",
                    "Precipitation (mm)",
                    "Snowfall (mm)",
                    "Wind Speed (km/h)",
                    "Wind Direction (°)",   
                    "Pressure (hPa)",
                    "Relative Humidity (%)",
                    "Dew Point (°C)"
                ]

                # Filter related columns dynamically
                column_groups = {
                    f"Average Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                    f"Minimum Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                    f"Maximum Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                    "Precipitation (mm)": ["Precipitation (mm)", "Snowfall (mm)", f"Average Temperature {temp_unit}"],
                    "Snowfall (mm)": ["Precipitation (mm)", "Snowfall (mm)", f"Average Temperature {temp_unit}"],
                    "Wind Speed (km/h)": ["Wind Speed (km/h)", "Wind Direction (°)", "Pressure (hPa)"],
                    "Wind Direction (°)": ["Wind Speed (km/h)", "Wind Direction (°)", "Pressure (hPa)"],
                    "Pressure (hPa)": ["Pressure (hPa)", "Wind Speed (km/h)", "Wind Direction (°)"],
                    "Relative Humidity (%)": ["Relative Humidity (%)", "Dew Point (°C)", "Snowfall (mm)"],
                    "Dew Point (°C)": ["Relative Humidity (%)", "Dew Point (°C)", "Snowfall (mm)"]
                }

                st.success("Historical weather data fetched successfully.")
                # Prompt user to select the primary column
                primary_columns = st.selectbox("Select a primary column to visualize:", available_columns)

                # Dynamically filter available columns based on the primary column
                filter_columns = column_groups.get(primary_columns, [primary_columns])

                # Ensure default values are a subset of filtered columns
                default_columns = [col for col in filter_columns if col in available_columns]

                selected_columns = st.multiselect("Select columns to visualize.", filter_columns, default=default_columns)

                if selected_columns:
                    selected_columns_with_date = ["datetime"] + [col for col in selected_columns if col in data.columns]
                    st.write("### Historical Weather Data")
                    st.dataframe(data[selected_columns_with_date])

                    # Ensure plot_graph() is called
                    if selected_columns_with_date:
                        plot_graph(data, city, temp_unit, start_date, end_date, primary_columns, selected_columns_with_date, 'historical')
                    else:
                        st.warning("No valid columns selected for visualization.")
                        
    with tab2:
        # Fetch and process forecast data
        forecast_data= get_forecast_data(city)

        if forecast_data is not None:
            forecast_data= process_forecast_data(forecast_data)

            # Convert temperatures to Fahrenheit if selected
            if unit == "F":
                if "Average Temperature (°C)" in forecast_data.columns:
                    forecast_data["Average Temperature (°F)"] = convert_to_fahrenheit(forecast_data["Average Temperature (°C)"])
                if "Minimum Temperature (°C)" in forecast_data.columns:
                    forecast_data["Minimum Temperature (°F)"] = convert_to_fahrenheit(forecast_data["Minimum Temperature (°C)"])
                if "Maximum Temperature (°C)" in forecast_data.columns:
                    forecast_data["Maximum Temperature (°F)"] = convert_to_fahrenheit(forecast_data["Maximum Temperature (°C)"])

                # Drop Celsius columns and rename Fahrenheit columns
                forecast_data.drop(columns=["Average Temperature (°C)", "Minimum Temperature (°C)", "Maximum Temperature (°C)"], inplace=True)
                temp_unit = "(°F)"
            else:
                temp_unit = "(°C)"

            st.write('### Forecast Data')

            # Available columns for forecast visualization
            forecast_columns = [
                f"Average Temperature {temp_unit}",
                f"Minimum Temperature {temp_unit}",
                f"Maximum Temperature {temp_unit}",
                "Precipitation (mm)",
                "Snowfall (mm)",
                "Wind Speed (m/s)",
                "Wind Direction (°)",   
                "Pressure (hPa)",
                "Relative Humidity (%)",
                "Dew Point (°C)"
            ]

            # Filter related columns dynamically
            related_columns = {
                f"Average Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                f"Minimum Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                f"Maximum Temperature {temp_unit}": [f"Average Temperature {temp_unit}", f"Minimum Temperature {temp_unit}", f"Maximum Temperature {temp_unit}", "Precipitation (mm)"],
                "Precipitation (mm)": ["Precipitation (mm)", "Snowfall (mm)", f"Average Temperature {temp_unit}"],
                "Snowfall (mm)": ["Precipitation (mm)", "Snowfall (mm)", f"Average Temperature {temp_unit}"],
                "Wind Speed (km/h)": ["Wind Speed (km/h)", "Wind Direction (°)", "Pressure (hPa)"],
                "Wind Direction (°)": ["Wind Speed (km/h)", "Wind Direction (°)", "Pressure (hPa)"],
                "Pressure (hPa)": ["Pressure (hPa)", "Wind Speed (km/h)", "Wind Direction (°)"],
                "Relative Humidity (%)": ["Relative Humidity (%)", "Dew Point (°C)", "Snowfall (mm)"],
                "Dew Point (°C)": ["Relative Humidity (%)", "Dew Point (°C)", "Snowfall (mm)"]
            }
            
            st.success("Forecast weather data fetched successfully.")

            # Allow user to select a primary column
            primary_column = st.selectbox("Select a primary column to visualize:", forecast_columns)
            related_selected_columns= related_columns.get(primary_column, [primary_column])
            related_selected_columns= [col for col in related_selected_columns if col in forecast_columns]
            # Allow user to select multiple columns
            selected_column = st.multiselect("Select columns to visualize:", related_selected_columns, default=related_selected_columns)

            # Display forecast data
            if selected_column:
                st.write("### Forecast Weather Data")
                st.dataframe(forecast_data[selected_column])
                plot_graph(forecast_data, city, temp_unit, datetime.now(), datetime.now() + timedelta(days= 7), primary_column, selected_column, 'forecast')
            else:
                st.warning("No valid columns selected for visualization.")
        else:
            st.info("No forecast data available. Displaying historical weather data instead.")


def display_weather_data(weather_data, city, unit='C', data_type='forecast'):
    if weather_data:
        # Set header title based on data type.
        if data_type.lower() == 'forecast':
            st.markdown(f'### <br>🌤 1 Week Extended Forecast in {city}', unsafe_allow_html= True)
            today_date = datetime.now().date()
        else:
            st.markdown(f'### Weather Data in {city}')
            today_date = None

        # Create header row with columns for each metric.
        header_day, header_condition, header_temp, header_feels, header_wind, header_winddir = st.columns(6)
        with header_day:
            st.markdown('**Day**')
        with header_condition:
            st.markdown('**Condition**')
        with header_temp:
            st.markdown('**Temperature**')
        with header_feels:
            st.markdown('**Feels Like**')
        with header_wind:
            st.markdown('**Wind**')
        with header_winddir:
            st.markdown('**Wind Direction**')

        # Mapping wind direction abbreviations to arrows.
        wind_arrow = {
            'N': '↑', 'NE': '↗', 'E': '→', 'SE': '↘', 
            'S': '↓', 'SW': '↙', 'W': '←', 'NW': '↖'
        }

        for day in weather_data:
            # Convert the date string to a date object.
            date_str = day.get('Date', 'N/A')
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except Exception:
                date_obj = None

            # Determine the day name: if forecast and date is today, label as "Today".
            if data_type.lower() == 'forecast' and today_date and date_obj == today_date:
                day_name = 'Today'
            elif date_obj:
                day_name = date_obj.strftime('%A')
            else:
                day_name = 'N/A'

            # Retrieve the icon and attempt to read the corresponding image file.
            icon = day.get('icon', 'default')
            icon_path = f'Icon/{icon}.png'
            try:
                with open(icon_path, 'rb') as img_file:
                    icon_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            except FileNotFoundError:
                icon_base64 = ''

            # Process wind direction.
            wind_direction = day.get('Wind Direction', 'N/A')
            if wind_direction != 'N/A':
                try:
                    wind_dir_degrees = int(float(wind_direction))
                    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                    index = round(wind_dir_degrees / 45) % 8
                    wind_dir_text = directions[index]
                    wind_arrow_symbol = wind_arrow.get(wind_dir_text, '❓')
                except Exception:
                    wind_arrow_symbol = '❓'
                    wind_dir_text = 'Unknown'
            else:
                wind_arrow_symbol = '❓'
                wind_dir_text = 'Unknown'

            # Handle temperature conversion if needed.
            if unit == 'F':
                Tempmax = int(convert_to_fahrenheit(day.get('Tempmax', 0)))
                Tempmin = int(convert_to_fahrenheit(day.get('Tempmin', 0)))
            else:
                Tempmax = day.get('Tempmax', 'N/A')
                Tempmin = day.get('Tempmin', 'N/A')

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.markdown(f'**{day_name}**')
            with col2:
                if icon_base64:
                    st.markdown(
                        f'<img src="data:image/png;base64,{icon_base64}" alt="{day.get("Conditions", "N/A")}" style="width: 30px; height: 30px; vertical-align: middle;"> {day.get("Conditions", "N/A")}',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f'{day.get("Conditions", "N/A")}')
            with col3:
                st.markdown(f'{Tempmin}°{unit} / {Tempmax}°{unit}')
            with col4:
                st.markdown(f'{day.get("Feelslike", "N/A")}°C')
            with col5:
                st.markdown(f'{day.get("Wind", "N/A")} km/h')
            with col6:
                st.markdown(f'{wind_arrow_symbol} {wind_dir_text} ({wind_direction}°)')
    else:
        st.info('No weather data available.')