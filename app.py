import streamlit as st
import requests

# Set up the look of the website
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 My Resume AI Chatbot")
st.markdown("---")

# Sidebar for security and settings
with st.sidebar:
    st.header("Settings")
    api_token = st.text_input("Hugging Face Token", type="password", help="Enter your token from huggingface.co")
    st.info("This bot uses the Mistral-7B model.")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type your message here..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call the AI "Chef" (The API)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    with st.chat_message("assistant"):
        if not api_token:
            st.warning("Please enter your Hugging Face Token in the sidebar to start!")
        else:
            with st.spinner("AI is thinking..."):
                try:
                    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
                    data = response.json()
                    
                    # Extract the reply text
                    full_response = data[0]['generated_text']
                    # Remove the prompt from the answer
                    bot_reply = full_response.split(prompt)[-1].strip()
                    
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error("The AI is still waking up. Please wait 15 seconds and try again!")