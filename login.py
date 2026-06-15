import streamlit as st
from database import create_users_table, validate_user
from pathlib import Path
from base64 import b64encode

def run_login():
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
            <div style="text-align:center; margin-top:200px;margin-bottom:-10px;">
                <img src="data:image/png;base64,{logo_base64}" width="140"/>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>SattvikAI</h1>", unsafe_allow_html=True)

    # Card CSS + wrapper
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
      min-height: 460px; 
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
      margin-bottom:50px;
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
    .login-form .stCheckbox, 
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



    # Widgets inside card
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Login</h1>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username")
        show_password = st.checkbox("Show password", value=False)
        password = st.text_input("Password", type="default" if show_password else "password", placeholder="Enter your password")
        if st.button("Login"):
            if not username or not password:
                st.error("Enter username and password.")
            else:
                if validate_user(username, password):
                    st.success(f"Welcome, {username}!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state.page = "food_logging"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please contact admin if you don't have an account.")

        # Wrap the button in a div with class 'signup-button'
        if st.button("Sign up", key="signup"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('<div class="signup-button"></div>', unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center; color:#FF5722; margin: -50px 0 5px 0;'>Don't have an Account? No worries! Sign Up from here :)</p>",
            unsafe_allow_html=True
        )



