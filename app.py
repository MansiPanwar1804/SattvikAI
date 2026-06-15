import streamlit as st
import login
import signup
import food_logging

# Initialize session page
if "page" not in st.session_state:
    st.session_state.page = "login"

# Route pages
if st.session_state.page == "login":
    login.run_login()  # call your existing login code
elif st.session_state.page == "signup":
    signup.run_signup()
elif st.session_state.page == "food_logging":
    food_logging.run_food_logging()