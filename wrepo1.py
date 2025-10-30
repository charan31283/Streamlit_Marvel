import requests
import streamlit as st
import google.genai as genai

WEATHER_API_KEY = "8f1b2bb4e9921443522d43cc36a8a719"
GEMINI_API_KEY = "AIzaSyD2k4du2yV_ce2X2_xf8ohXCHPp68S9UD0"

st.set_page_config(page_title="🌦️ Weather & Safety Assistant", page_icon="☁️")
st.title("🌦️ Weather & Safety Assistant")

st.write("This app shows your **current location's weather** automatically 🌍 and lets you check other cities too!")

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            loc = data.get("loc", "0,0").split(",")
            lat, lon = float(loc[0]), float(loc[1])
            return city, lat, lon
    except:
        return None, None, None
    return None, None, None

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_coordinates(city_name):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None


current_city, lat, lon = get_current_location()

if current_city and lat and lon:
    weather_data = get_weather(lat, lon)
    if weather_data and "main" in weather_data:
        tk = weather_data["main"]["temp"]
        tc = round(tk - 273.15, 2)
        desc = weather_data["weather"][0]["description"].capitalize()
        humidity = weather_data["main"]["humidity"]

        st.info(f"👋 Hi! You are currently in **{current_city}** 🌍")
        st.write(f"**Temperature:** {tc}°C")
        st.write(f"**Weather:** {desc}")
        st.write(f"**Humidity:** {humidity}%")

        if st.button("💡 Get Precautions for Current City"):
            query = (
                f"The current temperature is {tc}°C in {current_city} "
                f"with {desc} and {humidity}% humidity. "
                "Give some safety precautions for this weather."
            )
            client = genai.Client(api_key=GEMINI_API_KEY)
            ai_response = client.models.generate_content(
                model="gemini-2.5-flash", contents=query
            )

            st.subheader("🌤️ Precautionary Advice:")
            st.write(ai_response.text)
    else:
        st.warning("⚠️ Could not fetch weather for your current location.")
else:
    st.warning("⚠️ Could not detect your location automatically.")


st.markdown("---")
st.subheader("🔍 Check Another City")

city = st.text_input("🏙️ Enter another City Name to check:")

if st.button("Get Weather & Precautions"):
    if not city:
        st.warning("⚠️ Please enter a valid city name.")
    else:
        lat, lon = get_coordinates(city)
        if lat is None or lon is None:
            st.error("❌ Could not find the city. Please check the name.")
        else:
            data = get_weather(lat, lon)
            if not data or "main" not in data:
                st.error("⚠️ No weather data found.")
            else:
                tk = data["main"]["temp"]
                tc = round(tk - 273.15, 2)
                description = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]
                city_name = data.get("name", city)

                st.success(f"🌍 City: {city_name}")
                st.write(f"🌡️ Temperature: {tc}°C")
                st.write(f"☁️ Weather: {description}")
                st.write(f"💧 Humidity: {humidity}%")

                query = (
                    f"The current temperature is {tc}°C in {city_name} "
                    f"with {description} and {humidity}% humidity. "
                    "Give some safety precautions for this weather."
                )
                client = genai.Client(api_key=GEMINI_API_KEY)
                ai_response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=query
                )

                st.subheader("🌤️ Precautionary Advice:")
                st.write(ai_response.text)

