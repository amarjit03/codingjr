import streamlit as st
import requests
import os
# from dotenv import load_dotenv

# # Load .env variables
# load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

# Set page config
st.set_page_config(page_title="Groq Chat App", page_icon="🤖")

st.title("🤖 Chat with Groq AI")
st.write("Type a message to talk with the AI model powered by Groq.")
st.write("Created by Diya Khandelwal")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = f"Error: {response.status_code} - {response.text}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
