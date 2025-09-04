import streamlit as st
import google.generativeai as genai
import datetime
import re
import pytz

# 🔐 Configure Gemini API securely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(history=[])

# 🧼 Clean text
def clean_text(text):
    return re.sub(r'[^\w\s.,!?\'"]+', '', text)
#timestamp
def timestamp():
    local_tz = pytz.timezone("Africa/Nairobi")
    local_time = datetime.datetime.now(local_tz)
    return local_time.strftime("%H:%M")

# 💬 Callback to handle input and clear it
def process_input():
    user_input = st.session_state.input
    st.session_state.history.append(("You", user_input, timestamp(), None))
    try:
        response = chat.send_message(user_input)
        reply = clean_text(response.text)
        st.session_state.history.append(("Jay", reply, None, timestamp()))
    except Exception as e:
        error_msg = f"⚠️ Gemini error: {e}"
        st.session_state.history.append(("Jay", error_msg, None, timestamp()))
    st.session_state.input = ""  # ✅ Safe reset via callback

# 🧠 Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "input" not in st.session_state:
    st.session_state.input = ""

# 🖼️ Page setup
st.set_page_config(page_title="JayBot – Your Data Science Tutor", layout="wide")

# 🎨 WhatsApp-style purple theme
st.markdown("""
    <style>
    .chat-container {
        background-color: #f3e5f5;
        padding: 20px;
        border-radius: 10px;
        max-height: 80vh;
        overflow-y: auto;
    }
    .jay-header {
        background-color: #6A1B9A;
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
        background-color: #CE93D8;
        text-align: right;
        margin-left: auto;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        color: black;
        position: relative;
    }
    .bubble-jay {
        background-color: #E1BEE7;
        text-align: left;
        margin-right: auto;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        color: black;
        position: relative;
    }
    .timestamp-right {
        font-size: 10px;
        color: #4A148C;
        margin-top: 5px;
        text-align: right;
    }
    .timestamp-left {
        font-size: 10px;
        color: #4A148C;
        margin-top: 5px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# 🧭 Header
st.markdown("""
    <div class="jay-header">
        <img src="https://img.icons8.com/ios-filled/50/ffffff/chat.png"/>
        JayBot – Your Data Science Tutor
    </div>
""", unsafe_allow_html=True)

# 💬 Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, message, sent_time, received_time in st.session_state.history:
    bubble_class = "bubble-you" if speaker == "You" else "bubble-jay"
    timestamp_class = "timestamp-right" if speaker == "You" else "timestamp-left"
    time_label = f"Sent at {sent_time}" if speaker == "You" else f"Received at {received_time}"

    st.markdown(f"""
        <div class="{bubble_class}">
            <strong>{speaker}:</strong><br>{message}
            <div class="{timestamp_class}">{time_label}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📥 Input box with callback
st.text_input(
    "Type your message and press Enter:",
    key="input",
    on_change=process_input
)

