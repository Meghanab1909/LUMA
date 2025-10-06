import streamlit as st
from streamlit_option_menu import option_menu
import base64
import requests
from datetime import datetime
import pandas as pd

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "login_username" not in st.session_state:
    st.session_state["login_username"] = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "ticket_page" not in st.session_state:
    st.session_state.ticket_page = False 

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

def show_login():
    image_base64 = get_base64("logo-removebg-preview.png")

    st.markdown(f"""
        <div style="text-align: center">
            <img src="data:image/png;base64,{image_base64}" style="width:100px; border-radius:5%; margin-top: -60px; position: relative;">
        </div>
    """, unsafe_allow_html=True)

    login_username = st.text_input("Username or Email")
    login_password = st.text_input("Password", type="password")
    
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
                        st.session_state.logged_in = True
                        st.session_state["login_username"] = login_username
                        st.rerun()
                    elif "detail" in data:
                        st.error(f"❌ {data['detail']}")
                    else:
                        st.info(f"ℹ️ {data}")
                except ValueError:
                    st.error(f"❌ Server returned non-JSON response: {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection or request error: {e}")

def show_register():
    image_base64 = get_base64("logo-removebg-preview.png")

    st.markdown(f"""
        <div style="text-align: center">
            <img src="data:image/png;base64,{image_base64}" style="width:100px; border-radius:5%; margin-top: -60px; position: relative;">
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password")
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
                        st.rerun()
                    elif "detail" in data:
                        st.error(f"❌ {data['detail']}")
                    else:
                        st.info(f"ℹ️ {data}")
                except ValueError:
                    st.error(f"❌ Server returned non-JSON response: {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection or request error: {e}")

def raise_ticket():
    st.markdown("""
    <style>
    .main {
        top: 0;
        position: absolute;
    }
    </style>
    <h2>BUG TICKET TEMPLATE</h2>
    """, unsafe_allow_html = True)

    st.markdown("<div class = 'main'>", unsafe_allow_html = True)
    with st.form("ticket_form", clear_on_submit = True):
        title = st.text_input("Title")
        description = st.text_area("Enter project description (if you have a github link please include that as well)")
        priority = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW", "CRITICAL"])
        specialization = st.multiselect("Specialization", ["Frontend Developer", "Backend Developer", "Full-Stack Developer",
                                                        "Mobile App Developer", "Game Developer", "DevOps Engineer",
                                                        "Cloud Engineer", "Data Engineer", "Data Scientist", "Data Analyst",
                                                        "Machine Learning Engineer", "AI Researcher", "QA Engineer",
                                                        "Automation Tester", "Security Tester", "UI Designer", "UX Designer",
                                                        "Project Manager", "Business Analyst", "Technical Writer"
                                                        ]) or []
        
        submit = st.form_submit_button("Submit")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        created_by = st.session_state.get("login_username")

        status = "OPEN"

        if submit:
            if not title or not description:
                st.warning("Please fill all required fields")
            else:
                payload = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "created_by": created_by,
                    "assigned_to": None,
                    "specialization": specialization,
                    "created_at": current_time,
                    "status": status,
                    "updated_at": None
                }

                try:
                    response = requests.post("http://127.0.0.1:8000/tickets", json=payload)
                    response.raise_for_status()

                    data = response.json()
                    
                    if "message" in data:
                        st.success(f"✅ {data['message']}")
                    else:
                        st.info(f"ℹ️ {data}")
                
                except requests.exceptions.HTTPError as e:
                    st.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def accept_ticket(ticket_id, username):
    payload = {"ticket_id": ticket_id,
                "username": username}
    
    try:
        response = requests.post("http://127.0.0.1:8000/accept-tickets", json = payload)
        response.raise_for_status()

        data = response.json()

        if "message" in data:
            st.success(f"✅ Ticket {ticket_id} is accepted by {username}")
            st.info("📋 Tip: Once you accept a ticket, it won’t appear here anymore. Refresh to see updated tickets.")
        else:
            st.info(f"ℹ️ {data}")

    except Exception as e:
        st.error(f"❌ Failed to accept ticket: {e}")

def show_tickets():
    try:
        response = requests.get("http://127.0.0.1:8000/tickets")
        response.raise_for_status()
        data = response.json()

        if "tickets" in data and len(data["tickets"]) > 0:
            for ticket in data["tickets"]:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="padding:15px; margin-bottom:15px; border-radius:10px; 
                        background-color:#f9f9f9; box-shadow:0px 2px 5px rgba(0,0,0,0.1)">
                            <h4>🎫 {ticket['TITLE']}</h4>
                            <p><b>Status:</b> {ticket['status']} | <b>Priority:</b> {ticket['priority']}</p>
                            <p><b>Created By:</b> {ticket['created_by']}</p>
                            <p><b>Specialization:</b> {ticket['specialisation']}</p>
                            <details>
                                <summary><b>Description</b></summary>
                                <p>{ticket['description']}</p>
                            </details>
                            <p style="font-size:12px; color:gray;">Created at: {ticket['created_at']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns([1,1])  # adjust ratios
                    with col2:
                        accept_btn = st.button("✅ Accept Ticket", key=f"accept_{ticket['bugtkt_id']}")
                        
                        if accept_btn:
                            username = st.session_state["login_username"]
                            accept_ticket(ticket['bugtkt_id'], username)
        else:
            st.markdown(
            """
            <div style="text-align: center; padding: 40px; font-family: 'Arial', sans-serif;">
                <h1 style="color:#4DB6AC; font-size:48px; margin-bottom:10px;">💡 LUMA</h1>
                <h3 style="color:#555555; font-weight:400; margin-bottom:30px;">
                    Your lightweight bug & task tracking system
                </h3>
                <p style="color:#777777; font-size:18px; max-width:600px; margin:auto;">
                    Keep track of bugs, assign tasks, and collaborate effortlessly.
                    Streamline your workflow and stay on top of your projects with ease.
                </p>
                <p style="color:#999999; font-size:16px; margin-top:20px;">
                    Available tickets will be displayed here for quick access and action.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"❌ Failed to fetch tickets: {e}")

def show_mainpage():
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
            background-color: #E6E6FA;
        }
        div[data-testid="stButton"] button:hover {
            background-color: lightgray;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    set_background('main.png')
    username = st.session_state["login_username"]
    st.sidebar.markdown(f"<h1 style = 'margin-left: 40px'>👤 User: {username}</h1><br>", unsafe_allow_html = True)

    if st.sidebar.button("📝 Raise a Ticket", key = "raise-ticket"):
        st.session_state.ticket_page = True

    if st.sidebar.button("📩 Comments", key = "show-ticket"):
        st.session_state.ticket_page = False 

    if st.sidebar.button("⭕ Logout", key = "logout"):
        st.session_state.logged_in = False
        st.session_state.login_username = None
        st.rerun()
    
    if st.session_state.ticket_page:
        raise_ticket()
    else:
        show_tickets()

col1, col2 = st.columns([1, 1])  # ratio 1:1 → each half

if not st.session_state.logged_in:
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
            show_register()
        else:
            show_login()
else:
    show_mainpage()