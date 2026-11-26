import os
import requests
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import pandas as pd

load_dotenv()

st.title("🌤️ AI Weather Assistant")

api_key = os.getenv("WEATHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

city = st.text_input("Enter City Name")

if st.button("Get Weather"):

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    response = requests.get(url)

    if response.status_code != 200:
     st.error("Error: Could not fetch weather data.")
     st.stop()


        
    data = response.json()

    if "error" in data:
     st.error(data["error"]["message"])
     st.stop()


    print(data)

    city_name = data["location"]["name"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    wind = data["current"]["wind_kph"]
    condition = data["current"]["condition"]["text"]

    st.subheader("🌍 Weather Report")

    st.write("City:", city_name)
    st.write("Country:", country)
    st.write("Condition:", condition)
    st.write("Temperature:", temperature, "°C")
    st.write("Humidity:", humidity, "%")
    st.write("Wind Speed:", wind, "km/h")

    prompt = f"""
    You are an AI Weather Assistant.

    City: {city_name}
    Country: {country}
    Weather: {condition}
    Temperature: {temperature} °C
    Humidity: {humidity}%
    Wind Speed: {wind} km/h

    Based on this weather, give:
    1. A short weather summary.
    2. Clothing recommendation.
    3. Outdoor activity suggestion.
    4. Health advice.

    Keep the answer simple and friendly under 120 words.
    """

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_response = chat_completion.choices[0].message.content

    st.subheader(" AI Weather Advice")
    st.write(ai_response)
