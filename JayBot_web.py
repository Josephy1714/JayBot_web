import streamlit as st
import google.generativeai as genai
import datetime
import pyttsx3
import re

# 🔑 Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyDQYGU3j8pR_y50Igdt-mDGjk3fdHDnnTQ")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")
chat = model.start_chat(history=[])
engine = pyttsx3.init()

def clean_text(text):
    return re.sub(r'[^\w\s.,!?\'"]+', '', text)

def timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def handle_input(user_input):
    st.session_state.history.append((timestamp(), "You", user_input))
    if user_input.lower() == "exit":
        farewell = "Goodbye! Keep exploring data! 📊"
        st.session_state.history.append((timestamp(), "Jay", farewell))
        engine.say(clean_text(farewell))
        engine.runAndWait()
    else:
        try:
            response = chat.send_message(user_input)
            jay_reply = response.text
            st.session_state.history.append((timestamp(), "Jay", jay_reply))
            engine.say(clean_text(jay_reply))
            engine.runAndWait()
        except Exception as e:
            error_msg = f"⚠️ Error: {e}"
            st.session_state.history.append((timestamp(), "Jay", error_msg))

# 🖼️ Streamlit UI
st.set_page_config(page_title="JayBot – Your Data Science Tutor", layout="wide")
st.title("🤖 JayBot – Your Data Science Tutor")
st.markdown("Type your question below and press Enter. Jay will reply and speak the answer.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Your question:")

if user_input:
    handle_input(user_input)

# 💬 Display chat history
for time, speaker, message in st.session_state.history:
    st.markdown(f"**{time} {speaker}:** {message}")
