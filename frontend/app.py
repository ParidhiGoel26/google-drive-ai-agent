import streamlit as st
import requests
import time

API_URL = "https://google-drive-ai-agent-47b2.onrender.com/chat"

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
    margin-top: 40px;
    font-size: 14px;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("Drive Assistant")

    st.markdown("---")

    st.markdown("### Supported searches:")

    st.markdown("""
- 📄 PDFs
- 🖼 Images
- 🎥 Videos
- 📊 Excel files
- 📁 Folders
- 📑 Reports
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
# HEADER
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
# DISPLAY OLD CHAT
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "files" in message:

            for file in message["files"]:

                file_name = file.get("name", "Unknown File")

                file_url = file.get(
                    "webViewLink",
                    file.get("url", "#")
                )

                st.markdown(
                    f"- [{file_name}]({file_url})"
                )

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask about your files...")

if prompt:

    st.session_state.history.append(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # =========================
    # ASSISTANT RESPONSE
    # =========================

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching Google Drive..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"message": prompt},
                    timeout=60
                )

                data = response.json()

                files = data.get("files", [])

                if files:

                    st.success(f"Found {len(files)} file(s).")

                    for file in files:

                        file_name = file.get(
                            "name",
                            "Unknown File"
                        )

                        file_url = file.get(
                            "webViewLink",
                            file.get("url", "#")
                        )

                        st.markdown(
                            f"- [{file_name}]({file_url})"
                        )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Found {len(files)} file(s).",
                        "files": files
                    })

                else:

                    st.warning("No matching files found.")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "No matching files found."
                    })

            except Exception as e:

                st.error(f"Error: {str(e)}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": str(e)
                })

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