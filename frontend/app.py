import streamlit as st
import requests
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Google Drive AI Agent",
    page_icon="📁",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.stTextInput>div>div>input {
    background-color: #262730;
    color: white;
}

.big-title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #BBBBBB;
    font-size: 18px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("Drive Assistant")

    st.markdown("---")

    st.info("""
### Supported searches:

• PDFs  
• Images  
• Videos  
• Excel files  
• Folders  
• Reports  
""")

    st.markdown("---")

    st.subheader("Recent Searches")

    if "history" not in st.session_state:
        st.session_state.history = []

    for item in st.session_state.history[-5:][::-1]:
        st.write(f"🔎 {item}")

    st.markdown("---")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# =========================
# TITLE
# =========================
st.markdown(
    '<div class="big-title">📁 Google Drive AI Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Search files using natural language.</div>',
    unsafe_allow_html=True
)

st.caption(
    "Try: PDFs • invoices • videos • reports • excel sheets"
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT HISTORY
# =========================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================
user_input = st.chat_input(
    "Ask about your files..."
)

# =========================
# CHAT LOGIC
# =========================
if user_input and user_input.strip():

    # Save search history
    st.session_state.history.append(user_input)

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # =========================
    # BACKEND REQUEST
    # =========================

    BACKEND_URL = "https://google-drive-ai-agent-47b2.onrender.com/chat"

    with st.spinner("🔍 Searching files..."):

        try:

            response = requests.post(
                BACKEND_URL,
                json={
                    "message": user_input
                },
                timeout=60
            )

            data = response.json()

            assistant_response = data.get(
                "response",
                "No response received from server."
            )

        except Exception:

            assistant_response = (
                "⚠️ Unable to connect to backend server. "
                "Please try again later."
            )

    # Better no-results message
    if assistant_response.strip().lower() in [
        "no matching files found.",
        "no files found."
    ]:

        assistant_response = (
            "❌ No matching files found.\n\n"
            "Try searching by:\n"
            "- file type\n"
            "- file name\n"
            "- keywords\n"
            "- reports\n"
            "- videos\n"
            "- PDFs"
        )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })

    # =========================
    # TYPING ANIMATION
    # =========================
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        for chunk in assistant_response.split():

            full_response += chunk + " "

            message_placeholder.markdown(
                full_response + "▌"
            )

            time.sleep(0.02)

        message_placeholder.markdown(full_response)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <div class="footer">
    Built with ❤️ using Streamlit, FastAPI, LangChain & Google Drive API
    </div>
    """,
    unsafe_allow_html=True
)
