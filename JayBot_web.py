import streamlit as st
import google.generativeai as genai
import datetime
import re

# 🔑 Insert your Gemini API key below
genai.configure(api_key="AIzaSyDQYGU3j8pR_y50Igdt-mDGjk3fdHDnnTQ")

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(history=[])

# 🧼 Clean up text output
def clean_text(text):
    return re.sub(r'[^\w\s.,!?\'"]+', '', text)

# 🕒 Timestamp for chat history
def timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# 💬 Handle user input and generate reply
def handle_input(user_input):
    st.session_state.history.append((timestamp(), "You", user_input))

    if user_input.lower() == "exit":
        farewell = "Goodbye! Keep exploring data! 📊"
        st.session_state.history.append((timestamp(), "Jay", farewell))
        return

    try:
        response = chat.send_message(user_input)
        jay_reply = response.text
    except Exception as e:
        jay_reply = f"⚠ Error: {e}"
        print(f"Gemini error: {e}")

    st.session_state.history.append((timestamp(), "Jay", clean_text(jay_reply)))
    print(f"JayBot reply: {jay_reply}")

# 🖼 Streamlit UI
st.set_page_config(page_title="JayBot – Your Data Science Tutor", layout="wide")
st.title("🤖 JayBot – Your Data Science Tutor")
st.markdown("Type your question below and press Enter. Jay will reply and help you learn data science.")

# 🧠 Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# 📥 Input box
user_input = st.text_input("Your question:")

if user_input:
    handle_input(user_input)

# 📜 Display chat history
for time, speaker, message in st.session_state.history:
    st.markdown(f"{time} {speaker}:** {message}")
