
import streamlit as st
from backend.app import handle_user_request,init_func

# Initialize function when app starts
init_func()


st.title("Job Search with FastAPI Backend")

# Input fields for car details
st.header("Enter Job Details")
title = st.text_input("Job Title")
location = st.text_input("Location")
length = st.text_input("Size")



if st.button("Submit"):

    bot_response = handle_user_request(title=title, location=location, length=length)


    st.subheader("Response")
    st.write(bot_response)