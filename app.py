import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
from googletrans import Translator

# -----------------------------
# Translator
# -----------------------------
translator = Translator()

# -----------------------------
# Voice Output
# -----------------------------
def speak(text):
    tts = gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    st.audio(temp_file.name)

# -----------------------------
# Voice Input
# -----------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return None

# -----------------------------
# Smart Response Engine
# -----------------------------
def get_response(user_input):

    # Translate to English
    try:
        translated = translator.translate(user_input, dest="en").text.lower()
    except:
        translated = user_input.lower()

    # NON-MEDICAL DETECTION
    non_medical_words = [
        "what", "who", "hello", "hi", "about",
        "project", "chatbot", "ai", "how are you"
    ]

    if any(word in translated for word in non_medical_words):
        return "I'm a first aid chatbot. Please describe a health issue like injury, fever, burn, etc."

    # MEDICAL RESPONSES
    if any(word in translated for word in ["cut", "injury", "bleeding", "hurt", "wound"]):
        return "Clean the wound, apply pressure to stop bleeding, and use antiseptic."

    elif any(word in translated for word in ["burn", "fire", "hot"]):
        return "Cool the burn under running water for 10 minutes. Do not apply ice."

    elif any(word in translated for word in ["fever", "temperature"]):
        return "Take rest, drink fluids, and monitor temperature."

    elif any(word in translated for word in ["headache", "migraine"]):
        return "Take rest in a quiet place and stay hydrated."

    elif any(word in translated for word in ["vomit", "vomiting", "nausea"]):
        return "Drink small amounts of water and stay hydrated."

    else:
        return "I couldn't clearly understand the issue. Please describe your symptoms."

# -----------------------------
# UI SETTINGS
# -----------------------------
st.set_page_config(page_title="AI First Aid Chatbot", page_icon="🩺")

st.title("🩺 AI First Aid Chatbot")
st.warning("⚠️ This is not medical advice")

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# VOICE INPUT BUTTON
# -----------------------------
user_input = None

if st.button("🎤 Speak"):
    voice_text = listen()
    if voice_text:
        user_input = voice_text
        st.write("You said:", user_input)
    else:
        st.warning("Could not understand voice. Try again.")

# -----------------------------
# TEXT INPUT
# -----------------------------
typed_input = st.chat_input("Type your problem...")
if typed_input:
    user_input = typed_input

# -----------------------------
# PROCESS INPUT
# -----------------------------
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)

    speak(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
