import streamlit as st
import requests

st.set_page_config(
    page_title="Google Drive AI Agent",
    page_icon="📁",
    layout="centered"
)

st.title("📁 Google Drive AI Agent")

st.markdown(
    "Search files using natural language."
)

# SIDEBAR

st.sidebar.title("Drive Assistant")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Supported searches:

    • PDFs  
    • Images  
    • Videos  
    • Excel files  
    • Folders  
    • Reports  
    """
)

if st.sidebar.button("Clear Chat"):

    st.session_state.messages = []

    st.rerun()

# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY OLD MESSAGES

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# USER INPUT

user_input = st.chat_input(
    "Ask about your files..."
)

# NEW MESSAGE

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):

        st.markdown(user_input)

    with st.spinner("Searching Google Drive..."):

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "message": user_input
            }
        )

        data = response.json()

        assistant_response = data.get(
            "response",
            "No response"
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })

    with st.chat_message("assistant"):

        st.markdown(
            assistant_response,
            unsafe_allow_html=True
        )