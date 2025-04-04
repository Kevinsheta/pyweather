import streamlit as st

# Function to inject JavaScript for notifications
def get_notification_script(city, message):
    return f"""
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
        if (Notification.permission !== "granted") {{
          Notification.requestPermission().then(permission => {{
            if (permission === "granted") {{
              showNotification("{message}");
            }}
          }});
        }} else {{
          showNotification("{city} - {message}");
        }}
      }});

      function showNotification(message) {{
        if (Notification.permission === "granted") {{
          new Notification("Weather Alert in {city}", {{
            body: message + "\\nTap to see more.",
            icon: "https://yourwebsite.com/weather_icon.png"
          }});
        }}
      }}
    </script>
    """
    
# Function to display weather notifications
def display_notification(city, forecast_data):
    rain_prob = max(hour.get('rain_probability', 0) for hour in forecast_data)
    snow_prob = max(hour.get('snow_probability', 0) for hour in forecast_data)
    unique_conditions = set(hour.get('conditions', '') for hour in forecast_data)
    
    message = "🌤️ Looks like moderate weather today! Enjoy your day!"  

    if rain_prob >= 1:
        message = f"🌧️ Chance of rain today ({rain_prob}%). Don't forget your umbrella!"
        st.warning(message)
    elif snow_prob >= 1:
        message = f"❄️ Chance of snow today ({snow_prob}%). Dress warmly!"
        st.warning(message)
    elif "Thunderstorm" in unique_conditions:
        message = "⛈️ Thunderstorms expected today. Stay indoors if possible!"
        st.warning(message)
    elif "Fog" in unique_conditions:
        message = "🌫️ Expect foggy conditions today. Drive safely!"
        st.warning(message)
    elif "Clear" in unique_conditions:
        message = "☀️ Clear skies today! Enjoy your day!"
        st.info(message)

    # Inject JavaScript for browser notification
    st.components.v1.html(get_notification_script(city, message))