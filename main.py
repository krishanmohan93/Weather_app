import streamlit as st
import requests
import sqlite3

# Function to fetch weather data
def fetch_weather(city, api_key):
    base_url = 'http://api.weatherapi.com/v1/current.json'
    params = {'q': city, 'key': api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Database setup
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)''')
conn.commit()

# Authentication check
def authenticate(email, password):
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    return c.fetchone() is not None

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Sign Up", "Login", "Weather App"])

if page == "Sign Up":
    st.title("Sign-Up Page")
    name = st.text_input("Enter your full name:")
    email = st.text_input("Enter your email:")
    password = st.text_input("Create a password:", type="password")

    if st.button("Sign Up"):
        if name and email and password:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            st.success("Sign-up successful! Please proceed to the Login page.")
        else:
            st.warning("Please fill out all fields.")

elif page == "Login":
    st.title("Login Page")
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        if authenticate(email, password):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.success("Login successful! You can now access the Weather App.")
        else:
            st.error("Invalid email or password. Please try again.")

elif page == "Weather App":
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("You must log in first to access the Weather App.")
        st.stop()

    st.title("Weather Application")
    st.write("Get real-time weather updates for any city around the world.")

    # Input for user name and city name
    name = st.text_input("Enter Your Name:", "")
    city = st.text_input("Enter the city name:", "")

    # API key for WeatherAPI
    api_key = 'b95127aa9c5141639e9150810242907'

    # Submit button
    if st.button("Submit"):
        if city and name:
            weather_data = fetch_weather(city, api_key)
            if weather_data:
                city_name = weather_data['location']['name']
                country = weather_data['location']['country']
                temperature = weather_data['current']['temp_c']
                weather_desc = weather_data['current']['condition']['text']

                st.markdown(
                    f"<h2 style='color: green;'>Dear {name}, here are the weather details for your city {city_name}:</h2>",
                    unsafe_allow_html=True
                )
                st.write(f"**Country:** {country}")
                st.metric("Temperature", f"{temperature} °C")
                st.write(f"**Weather Description:** {weather_desc}")
            else:
                st.error("Error fetching weather data. Please check the city name and try again.")
        else:
            st.warning("Please enter both your name and the city name.")
