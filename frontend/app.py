import streamlit as st
import requests
import time

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Google Drive AI Agent",
    page_icon="📁",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0E1117;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Main title */
.main-title {
    font-size: 54px;
    font-weight: 700;
    color: white;
    margin-bottom: 0;
}

/* Subtitle */
.subtitle {
    font-size: 22px;
    color: #B0B3B8;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* Search examples */
.search-examples {
    color: #8B949E;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Chat box */
.chat-box {
    background-color: #161B22;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 20px;
    border: 1px solid #30363D;
}

/* User message */
.user-msg {
    font-size: 18px;
    font-weight: 600;
    color: white;
}

/* Bot message */
.bot-msg {
    font-size: 20px;
    font-weight: 700;
    color: white;
    margin-bottom: 15px;
}

/* File links */
.file-link {
    font-size: 18px;
    margin-bottom: 14px;
    line-height: 1.8;
}

/* Footer */
.footer {
    text-align: center;
    color: #8B949E;
    padding-top: 40px;
    padding-bottom: 10px;
    font-size: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Spinner */
.stSpinner > div > div {
    border-top-color: #4F8BF9 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:

    st.title("Drive Assistant")

    st.divider()

    st.markdown("""
    ### Supported searches:
    
    - 📄 PDFs  
    - 🖼 Images  
    - 🎥 Videos  
    - 📊 Excel files  
    - 📁 Folders  
    - 📑 Reports  
    """)

    st.divider()

    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("### Recent Searches")

    for item in st.session_state.history[-5:]:
        st.write(f"🔎 {item}")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =========================================
# SESSION STATE
# =========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="main-title">
📁 Google Drive AI Agent
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Search files using natural language.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="search-examples">
Try: PDFs • invoices • videos • reports • excel sheets
</div>
""", unsafe_allow_html=True)

# =========================================
# DISPLAY CHAT HISTORY
# =========================================
for message in st.session_state.messages:

    # USER MESSAGE
    if message["role"] == "user":

        st.markdown(f"""
        <div class="chat-box">
            <div class="user-msg">🔴 {message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ASSISTANT MESSAGE
    else:

        st.markdown("""
        <div class="chat-box">
            <div class="bot-msg">🤖 I found these files:</div>
        """, unsafe_allow_html=True)

        for file in message["files"]:

            icon = "📄"

            if file["name"].lower().endswith(".mp4"):
                icon = "🎥"

            elif file["name"].lower().endswith(".xlsx"):
                icon = "📊"

            elif file["name"].lower().endswith(".png"):
                icon = "🖼"

            st.markdown(
                f"""
                <div class="file-link">
                    {icon} <a href="{file['url']}" target="_blank">{file['name']}</a>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# CHAT INPUT
# =========================================
query = st.chat_input("Ask about your files...")

# =========================================
# API CALL
# =========================================
if query:

    # Save search history
    st.session_state.history.append(query)

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Display user message instantly
    st.markdown(f"""
    <div class="chat-box">
        <div class="user-msg">🔴 {query}</div>
    </div>
    """, unsafe_allow_html=True)

    # LOADING SPINNER
    with st.spinner("Searching Google Drive..."):

        time.sleep(1)

        try:

            # YOUR RENDER BACKEND URL
            API_URL = "https://google-drive-ai-agent-47b2.onrender.com/search"

            response = requests.post(
                API_URL,
                json={"query": query},
                timeout=60
            )

            data = response.json()

            files = data.get("files", [])

            if files:

                st.session_state.messages.append({
                    "role": "assistant",
                    "files": files
                })

                st.markdown("""
                <div class="chat-box">
                    <div class="bot-msg">🤖 I found these files:</div>
                """, unsafe_allow_html=True)

                for file in files:

                    icon = "📄"

                    if file["name"].lower().endswith(".mp4"):
                        icon = "🎥"

                    elif file["name"].lower().endswith(".xlsx"):
                        icon = "📊"

                    elif file["name"].lower().endswith(".png"):
                        icon = "🖼"

                    st.markdown(
                        f"""
                        <div class="file-link">
                            {icon} 
                            <a href="{file['url']}" target="_blank">
                                {file['name']}
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)

            else:

                st.markdown("""
                <div class="chat-box">
                    ❌ No matching files found.
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:

            st.markdown(f"""
            <div class="chat-box">
                ⚠️ Unable to connect to backend server.<br><br>
                Error: {str(e)}
            </div>
            """, unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div class="footer">
Built with ❤️ using Streamlit, FastAPI, LangChain & Google Drive API
</div>
""", unsafe_allow_html=True)
