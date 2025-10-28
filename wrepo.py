
import requests as r
import streamlit as st
import google.genai as genai


st.set_page_config(page_title="Weather & Safety Assistant")

st.title("☁️ Weather & Safety Assistant")
st.write("Enter your **Latitude** and **Longitude** to get live weather info and precautions!")

lat = st.user_input("Enter Latitude: ")
lon = st.user_input("Enter Longitude: ")

weather_api_key = "8f1b2bb4e9921443522d43cc36a8a719"
gemini_api_key = "AIzaSyD2k4du2yV_ce2X2_xf8ohXCHPp68S9UD0"

if st.button("Get Weather & Advice"):
    if lat == 0 and lon == 0:
        st.warning("⚠️ Please enter valid coordinates.")
    else:
        
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
            response = r.get(url)
            data = response.json()

            if response.status_code != 200 or "main" not in data:
                st.error("❌ Could not fetch weather details. Check coordinates.")
            else:
                tk = data["main"]["temp"]
                tc = round(tk - 273.15, 2)
                city = data.get("name", "your location")

                st.success(f"The current temperature is {tc}°C in {data['name']} with {data['weather'][0]['main']} and humidity of {data['main']['humidity']}% .Tell me some precatuions")

                query = f"The current temperature is {tc}°C in {city}. Suggest some precautions."
                client = genai.Client(api_key=gemini_api_key)
                ai_response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=query
                )

                st.subheader("🌤️ Precautionary Advice:")
                st.write(ai_response.text)

        



