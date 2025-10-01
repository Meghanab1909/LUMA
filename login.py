import streamlit as st
from streamlit_option_menu import option_menu
import base64
import requests
import random

if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_register" not in st.session_state:
    st.session_state.show_register = False

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_path):
    encoded_image = get_base64(image_path)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main {{
        background-color: transparent;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call this with your image file
set_background("bg.png")

st.markdown(
    """
    <style>
    div[data-testid="stButton"] button {
        height: 50px;
        width: 300px;
        background-color: white;
        border-radius: 10px;
        font-size: 20px;
        border: none;
        cursor: pointer;
    }
    div[data-testid="stButton"] button:hover {
        background-color: lightgray;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([1, 1])  # ratio 1:1 → each half

# Treat the first column as your "sidebar"
with col1:
    st.markdown("""
        <h1 style = 'margin-top: 105px; color: white; align-text: center'>💡 LUMA</h1>
        """, unsafe_allow_html=True)

    login = st.button("LOGIN", key="login")
    register = st.button("REGISTER", key="register")

    if login:
        st.session_state.show_login = True
        st.session_state.show_register = False

    if register:
        st.session_state.show_register = True
        st.session_state.show_login = False
        
    
# Main content in the second column
with col2:
    st.markdown(
        """
        <style>
        div.stButton > button {
            display: block;
            margin-left: 65px;   
            width: 200px;        
            height: 50px;
            border-radius: 10px;
            font-size: 18px;
            background-color: #ffffff;
            cursor: pointer;
            transition: 0.3s;
        }

        label[data-testid="stWidgetLabel"] > div {
        font-size: 17px 
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.session_state.get("show_register", True):
        image_base64 = get_base64("logo-removebg-preview.png")

        st.markdown(f"""
            <div style="text-align: center">
                <img src="data:image/png;base64,{image_base64}" style="width:100px; border-radius:5%; margin-top: -60px; position: relative;">
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", key="username")
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        roles = st.multiselect("Role(s)", ["Developer", "Tester"])

        if st.button("Sign Up", key = "signup"):
            if not username or not password or not roles:
                st.warning("Please fill all the required fields and select at least one role")

            else:    
                payload = {"username": username,
                        "email": email or None,
                        "password": password,
                        "roles": list(roles)}
            
                try:
                    response = requests.post("http://127.0.0.1:8000/register", json = payload)
                    response.raise_for_status()

                    try:
                        data = response.json()

                        if "message" in data:
                            st.success(f"✅ {data['message']}")
                            st.session_state.show_register = False
                            st.session_state.show_login = True
                        elif "detail" in data:
                            st.error(f"❌ {data['detail']}")
                        else:
                            st.info(f"ℹ️ {data}")
                    except ValueError:
                        st.error(f"❌ Server returned non-JSON response: {response.text}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection or request error: {e}")
    else:
        image_base64 = get_base64("logo-removebg-preview.png")

        st.markdown(f"""
            <div style="text-align: center">
                <img src="data:image/png;base64,{image_base64}" style="width:100px; border-radius:5%; margin-top: -60px; position: relative;">
            </div>
        """, unsafe_allow_html=True)

        login_username = st.text_input("Username or Email", key="login-username")
        login_password = st.text_input("Password", type="password", key="login-password")
        
        if st.button("Sign In", key = "signin"):
            if not login_username or not login_password:
                st.warning("Please fill all the fields")
            else:
                payload = {"username": login_username,
                        "password": login_password}
                
                try:
                    response = requests.post("http://127.0.0.1:8000/login", json = payload)
                    response.raise_for_status()

                    try:
                        data = response.json()

                        if "message" in data:
                            st.success(f"✅ {data['message']}")
                            #Direct to next page

                        elif "detail" in data:
                            st.error(f"❌ {data['detail']}")
                        else:
                            st.info(f"ℹ️ {data}")
                    except ValueError:
                        st.error(f"❌ Server returned non-JSON response: {response.text}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection or request error: {e}")