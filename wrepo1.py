import streamlit as st
import requests
import google.genai as genai
import json

# --- API Keys ---
WEATHER_API_KEY = "8f1b2bb4e9921443522d43cc36a8a719"  
GEMINI_API_KEY = "AIzaSyD2k4du2yV_ce2X2_xf8ohXCHPp68S9UD0"  

st.set_page_config(page_title="🌦️ Weather & Safety Assistant", page_icon="☁️")
st.title("🌦️ Weather & Safety Assistant")
st.write("This app shows your **current location's weather** automatically 🌍 and lets you check other cities too!")

# --- Inject JavaScript to Get Browser Location ---
st.write("Fetching your location... please allow access in your browser 👇")

location_html = """
<script>
navigator.geolocation.getCurrentPosition(
    (pos) => {
        const coords = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
        };
        window.parent.postMessage(coords, "*");
    },
    (err) => {
        window.parent.postMessage({error: err.message}, "*");
    }
);
</script>
"""

st.components.v1.html(location_html, height=0)

# --- Get Coordinates from JS (via Streamlit message) ---
location_data = st.experimental_get_query_params()

# Placeholder for coordinates
if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None

# Try to update if Streamlit gets message
st.markdown(
    """
    <script>
    window.addEventListener("message", (event) => {
        const data = event.data;
        if (data.lat && data.lon) {
            const params = new URLSearchParams({
                lat: data.lat,
                lon: data.lon
            });
            window.location.search = params.toString();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

if "lat" in location_data and "lon" in location_data:
    try:
        st.session_state.lat = float(location_data["lat"][0])
        st.session_state.lon = float(location_data["lon"][0])
    except:
        pass

# --- Weather Function ---
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# --- If user location found ---
if st.session_state.lat and st.session_state.lon:
    weather = get_weather(st.session_state.lat, st.session_state.lon)
    if weather and "main" in weather:
        city = weather.get("name", "your area")
        temp_c = round(weather["main"]["temp"] - 273.15, 2)
        desc = weather["weather"][0]["description"].capitalize()
        humidity = weather["main"]["humidity"]

        st.info(f"👋 Hi! You are currently in **{city}** 🌍")
        st.write(f"🌡️ Temperature: {temp_c}°C")
        st.write(f"☁️ Weather: {desc}")
        st.write(f"💧 Humidity: {humidity}%")

        if st.button("💡 Get Precautions for Current City"):
            query = f"The temperature is {temp_c}°C in {city} with {desc} and {humidity}% humidity. Suggest safety precautions."
            client = genai.Client(api_key=GEMINI_API_KEY)
            ai_response = client.models.generate_content(
                model="gemini-2.5-flash", contents=query
            )
            st.subheader("🌤️ Precautionary Advice:")
            st.write(ai_response.text)
    else:
        st.warning("⚠️ Unable to fetch weather data for your location.")
else:
    st.warning("⚠️ Please allow location access in your browser.")

