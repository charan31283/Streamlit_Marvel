import requests
import streamlit as st
from streamlit_js_eval import get_geolocation
import google.genai as genai

WEATHER_API_KEY = "8f1b2bb4e9921443522d43cc36a8a719"
GEMINI_API_KEY = "AIzaSyD2k4du2yV_ce2X2_xf8ohXCHPp68S9UD0"

st.set_page_config(page_title="🌦️ Weather & Safety Assistant", page_icon="☁️")
st.title("🌦️ Weather & Safety Assistant")
st.write("This app shows your **current location's weather and safety tips** automatically 🌍 and lets you check other cities too!")

def get_weather(lat, lon):
    """Fetch weather data from OpenWeather API using coordinates."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_coordinates(city_name):
    """Get latitude and longitude for a given city."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_city_name(lat, lon):
    """Reverse geocode coordinates to get city name."""
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get('name', 'Unknown')
    return "Unknown"

def get_precautions(temp_c, city, desc, humidity):
    """Generate AI-based precautions for the given weather."""
    query = (
        f"The current temperature is {temp_c}°C in {city} "
        f"with {desc} and {humidity}% humidity. "
        "Give some safety precautions for this weather."
    )
    client = genai.Client(api_key=GEMINI_API_KEY)
    ai_response = client.models.generate_content(model="gemini-2.5-flash", contents=query)
    return ai_response.text


st.subheader("📍 Detecting your location...")

loc = get_geolocation()

if loc and "coords" in loc:
    lat = loc["coords"]["latitude"]
    lon = loc["coords"]["longitude"]
    city = get_city_name(lat, lon)

    if city:
        st.success(f"📍 Detected location: **{city}**")
        data = get_weather(lat, lon)
        if data and "main" in data:
            temp_c = round(data["main"]["temp"] - 273.15, 2)
            desc = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]

            st.write(f"🌡️ **Temperature:** {temp_c}°C")
            st.write(f"☁️ **Weather:** {desc}")
            st.write(f"💧 **Humidity:** {humidity}%")

            st.map([{"lat": lat, "lon": lon}], zoom=8)

            if st.button("💡 Get Precautions for Current City"):
                st.subheader("🌤️ Precautionary Advice:")
                st.write(get_precautions(temp_c, city, desc, humidity))
        else:
            st.warning("⚠️ Could not fetch weather data for your location.")
    else:
        st.warning("⚠️ Could not detect your city name.")
else:
    st.warning("⚠️ Could not access browser location (please allow location access in your browser).")

st.markdown("---")
st.subheader("🔍 Check Another City")

city_input = st.text_input("🏙️ Enter another City Name:")

if st.button("Get Weather & Precautions"):
    if not city_input:
        st.warning("⚠️ Please enter a valid city name.")
    else:
        lat, lon = get_coordinates(city_input)
        if lat is None or lon is None:
            st.error("❌ Could not find the city. Please check the name.")
        else:
            data = get_weather(lat, lon)
            if not data or "main" not in data:
                st.error("⚠️ No weather data found.")
            else:
                temp_c = round(data["main"]["temp"] - 273.15, 2)
                desc = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]

                st.success(f"🌍 City: {city_input}")
                st.write(f"🌡️ Temperature: {temp_c}°C")
                st.write(f"☁️ Weather: {desc}")
                st.write(f"💧 Humidity: {humidity}%")

                st.map([{"lat": lat, "lon": lon}], zoom=8)

                st.subheader("🌤️ Precautionary Advice:")
                st.write(get_precautions(temp_c, city_input, desc, humidity))

