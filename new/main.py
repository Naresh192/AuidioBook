import streamlit as st
import asyncio
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription
import subprocess

# Function to start the server script
def start_server():
    subprocess.Popen(["python", "server.py"])

# Check if the server is already running
if 'server_started' not in st.session_state:
    st.session_state['server_started'] = False

if not st.session_state['server_started']:
    start_server()
    st.session_state['server_started'] = True


st.title("Multi-User Audio Chat App")

# User Authentication (simple example)
if 'username' not in st.session_state:
    st.session_state.username = st.text_input("Enter your username")

if st.session_state.username:
    st.write(f"Hello, {st.session_state.username}!")

    # WebSocket connection
    async def connect():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            st.session_state.websocket = websocket
            while True:
                message = await websocket.recv()
                st.write(f"Message received: {message}")

    asyncio.run(connect())

    # WebRTC setup
    pc = RTCPeerConnection()

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        await st.session_state.websocket.send(candidate.to_json())

    @pc.on("track")
    def on_track(track):
        st.audio(track)

    # User Interface
    online_users = ["User1", "User2", "User3"]  # Example list of online users
    selected_user = st.selectbox("Select a user to talk to:", online_users)

    if st.button("Start Chat"):
        st.write(f"Starting chat with {selected_user}")
        # WebRTC signaling and connection setup
        offer = pc.createOffer()
        asyncio.run(pc.setLocalDescription(offer))
        asyncio.run(st.session_state.websocket.send(offer.sdp))

        answer = asyncio.run(st.session_state.websocket.recv())
        pc.setRemoteDescription(RTCSessionDescription(answer, "answer"))
