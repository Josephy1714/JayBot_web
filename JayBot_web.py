import streamlit as st
import google.generativeai as genai
import datetime
import re

# 🔑 Insert your Gemini API key here
genai.configure(api_key="AIzaSyDQYGU3j8pR_y50Igdt-mDGjk3fdHDnnTQ")

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(history=[])

# 🧼 Clean text output
def clean_text(text):
    return re.sub(r'[^\w\s.,!?\'"]+', '', text)

# 🕒 Timestamp
def timestamp():
    return datetime.datetime.now().strftime("%H:%M")

# 💬 Handle input
def handle_input(user_input):
    st.session_state.history.append(("You", user_input, timestamp(), None))
    try:
        response = chat.send_message(user_input)
        jay_reply = clean_text(response.text)
    except Exception as e:
        jay_reply = f"⚠️ Error: {e}"
        print(f"Gemini error: {e}")
    st.session_state.history.append(("Jay", jay_reply, None, timestamp()))

# 🖼️ Page config
st.set_page_config(page_title="JayBot – Your Data Science Tutor", layout="wide")

# 🎨 Custom CSS for WhatsApp-style layout
st.markdown("""
    <style>
    .chat-container {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        max-height: 80vh;
        overflow-y: auto;
    }
    .jay-header {
        background-color: #075E54;
        color: white;
        padding: 10px 20px;
        font-size: 20px;
        font-weight: bold;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        display: flex;
        align-items: center;
    }
    .jay-header img {
        height: 30px;
        margin-right: 10px;
    }
    .bubble-you {
        background-color: #DCF8C6;
        text-align: right;
        margin-left: auto;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
    }
    .bubble-jay {
        background-color: #E6E6E6;
        text-align: left;
        margin-right: auto;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
    }
    .timestamp {
        font-size: 10px;
        color: gray;
        margin-top: 5px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# 🧭 Header
st.markdown("""
    <div class="jay-header">
        <img src="https://img.icons8.com/ios-filled/50/ffffff/chat.png"/>
        JayBot – Your Data Science Tutor
    </div>
""", unsafe_allow_html=True)

# 💬 Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, message, sent_time, received_time in st.session_state.history:
    bubble_class = "bubble-you" if speaker == "You" else "bubble-jay"
    time_label = f"Sent at {sent_time}" if speaker == "You" else f"Received at {received_time}"

    st.markdown(f"""
        <div class="{bubble_class}">
            <strong>{speaker}:</strong><br>{message}
            <div class="timestamp">{time_label}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📥 Input box
user_input = st.text_input("Type your message and press Enter:", key="input")

if user_input:
    handle_input(user_input)
    st.session_state.input = ""  # Clear the textbox after sending
