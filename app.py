import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import time

# -------------------------------
# Improved Training Data
# -------------------------------
questions = [
    "i have a cut", "cut on hand", "my hand is bleeding", "deep cut", "bleeding badly",
    "burn injury", "i got burned", "burned my finger", "hot oil burn",
    "i have fever", "high temperature", "feeling feverish", "body is hot",
    "headache", "i have headache", "my head hurts", "severe headache"
]

answers = [
    "Clean the wound and apply antiseptic.",
    "Apply pressure to stop bleeding.",
    "Apply pressure and clean the wound properly.",
    "Cover with clean cloth and seek medical help if deep.",
    "Apply pressure immediately and stop bleeding.",

    "Cool the burn under running water. Do not apply ice.",
    "Run cool water over burn area for 10 minutes.",
    "Apply aloe vera or soothing cream after cooling.",
    "Do not touch burn, cool it with water immediately.",

    "Take rest and stay hydrated.",
    "Monitor temperature and consult a doctor if needed.",
    "Drink fluids and rest well.",
    "Take proper rest and check temperature regularly.",

    "Take rest and consider mild pain relief.",
    "Relax and avoid stress.",
    "Take rest in a quiet place.",
    "Use mild pain relief if necessary."
]

# -------------------------------
# Train Model (Improved)
# -------------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = MultinomialNB()
model.fit(X, answers)

# -------------------------------
# UI Setup
# -------------------------------
st.set_page_config(page_title="AI First Aid Assistant", page_icon="🩺")

st.title("🩺 AI First Aid Assistant")
st.write("Get quick first aid help (cut, burn, fever, headache)")

# Sidebar
st.sidebar.title("⚙️ Options")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

st.sidebar.write("💡 Try: 'I have a cut', 'burn injury', 'fever'")

# -------------------------------
# Chat History
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat Input
# -------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Process input
    X_test = vectorizer.transform([user_input])
    response = model.predict(X_test)[0]

    # Fallback response (if unsure)
    if response is None or response == "":
        response = "I'm not sure. Please consult a doctor."

    # Typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for char in response:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.02)

    # Save bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })