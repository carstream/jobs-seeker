import streamlit as st
from dotenv import load_dotenv
from backend.app import handle_user_request, init_func
import os
load_dotenv()

# Initialize function when app starts
init_func()

# Password authentication
PASSWORD = os.getenv("APP_PASSWORD")  # Change this to your desired password

st.sidebar.header("Authentication")
password = st.sidebar.text_input("Enter Your Password", type="password")

if password != PASSWORD:
    st.warning("❌ Incorrect Password! Please enter the correct password to access the app.")
    st.stop()  # Stop execution if the password is incorrect

st.title("Job Search with FastAPI Backend")

# Input fields for job details
st.header("Enter Job Details")
title = st.text_input("Job Title")
location = st.text_input("Location")
length = st.text_input("Size")

# Check if all fields are filled
is_enabled = bool(title.strip()) and bool(location.strip()) and bool(length.strip())

# Disable button if fields are empty
submit_button = st.button("Submit", disabled=not is_enabled)

if submit_button:
    bot_response = handle_user_request(title=title, location=location, length=length)
    
    st.subheader("Response")
    st.write(bot_response)
