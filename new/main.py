import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings

# Initialize session state for online users
if 'online_users' not in st.session_state:
    st.session_state['online_users'] = ["User1", "User2", "User3"]

# Function to add a new user to the online users list
def add_user(user_name):
    if user_name not in st.session_state['online_users']:
        st.session_state['online_users'].append(user_name)

# Function to remove a user from the online users list
def remove_user(user_name):
    if user_name in st.session_state['online_users']:
        st.session_state['online_users'].remove(user_name)

# User login
user_name = st.text_input("Enter your name")
if st.button("Join Chat"):
    add_user(user_name)
    st.write(f"Welcome, {user_name}!")

# Display online users
selected_user = st.selectbox("Select a user to call", st.session_state['online_users'])
st.write(f"You selected: {selected_user}")

# WebRTC configuration
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Initiate voice call
if st.button("Call"):
    st.write(f"Calling {selected_user}...")
    webrtc_streamer(key=f"call_{selected_user}", mode=WebRtcMode.SENDRECV, client_settings=WEBRTC_CLIENT_SETTINGS)

# User logout
if st.button("Leave Chat"):
    remove_user(user_name)
    st.write(f"Goodbye, {user_name}!")
