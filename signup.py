import streamlit as st
from database import create_users_table, add_user
from pathlib import Path
from base64 import b64encode


def run_signup():
    create_users_table()
    st.set_page_config(page_title="SattvikAI", page_icon="🥗", layout="centered")

    # Hide default UI
    st.markdown("""
           <style>
           .stApp { background-color: #FFFFF0; }
           #MainMenu, footer, header {visibility: hidden;}
           .block-container { padding-top:10px; padding-bottom:30px; display:flex; justify-content:center; align-items:center; min-height:90px; }
           </style>
       """, unsafe_allow_html=True)


    # Logo + App Name
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        logo_bytes = logo_path.read_bytes()
        logo_base64 = b64encode(logo_bytes).decode()
        st.markdown(f"""
            <div style="text-align:center; margin-top:600px;">
                <img src="data:image/png;base64,{logo_base64}" width="140"/>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>SattvikAI</h1>", unsafe_allow_html=True)

    # Card CSS + wrapper (same as login)
    st.markdown("""
    <style>
    .login-wrapper {
      position: relative; 
      width: 100%; 
      display: flex; 
      justify-content: center; 
      align-items: flex-start; 
      margin-top: 3px; 
      margin-bottom: 20px;
    }
    .login-card {
      position: absolute; 
      width: 550px; 
      min-height: 900px; 
      background: #ffffff; 
      padding: 60px 50px; 
      border-radius: 20px; 
      box-shadow:0 14px 38px rgba(0,0,0,0.12); 
      top:40px;
    }
    .login-form {
     width:500px; 
     margin-top:40px; 
     margin-bottom:10px;
    }
    div.stButton > button {
     display:block; 
     margin:80px;
     margin-bottom:30px; 
     width:80%; 
     background-color:#123a14; 
     margin-top:30px; 
     color:white; 
     font-weight:500; 
     border:none; 
     border-radius:10px; 
     padding:10px; 
     transition:all 0.3s ease;
    }
    div.stButton > button:hover {
      background-color:#45a049; 
      transform:scale(1.03);
    }
    .login-form p { 
      text-align:center;
    }
    .login-form .stTextInput, 
    .login-form .stSelectbox, 
    .login-form .stNumberInput, 
    .login-form .stButton {
      width:80%;
    }
    @media (max-width:480px) {
    .login-card, 
    .login-form {
      width:90%; 
      padding:35px 25px;
     }
    }
    </style>
    <div class="login-wrapper">
        <div class="login-card"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Sign Up</h1>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.5)
        activity = st.selectbox("Activity Level",
                                ["Select", "Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

        if st.button("Register"):
            if not username or not password or gender == "Select" or activity == "Select":
                st.error("Please fill all required fields.")
            else:
                success, msg = add_user(username, password, name, age, gender, weight, height, activity)
                if success:
                    st.success("Account created successfully! You can now log in.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(msg)
        if st.button("← Login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
