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
    font-size: 52px;
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
    margin-bottom: 18px;
    border: 1px solid #30363D;
}

/* User message */
.user-msg {
    font-size: 18px;
    font-weight: 600;
    color: white;
}

/* Assistant message */
.assistant-msg {
    font-size: 18px;
    color: #E6EDF3;
    line-height: 1.7;
    word-wrap: break-word;
}

/* Footer */
.footer {
    text-align: center;
    color: #8B949E;
    padding-top: 40px;
    padding-bottom: 10px;
    font-size: 14px;
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
        st.session_state.history = []
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

    if message["role"] == "user":

        st.markdown(f"""
        <div class="chat-box">
            <div class="user-msg">
                🔴 {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif message["role"] == "assistant":

        st.markdown(f"""
        <div class="chat-box">
            <div class="assistant-msg">
                🤖 {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# CHAT INPUT
# =========================================
query = st.chat_input("Ask about your files...")

# =========================================
# API CALL
# =========================================
if query:

    st.session_state.history.append(query)

    # Save user msg
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Show user msg immediately
    st.markdown(f"""
    <div class="chat-box">
        <div class="user-msg">
            🔴 {query}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Searching Google Drive..."):

        time.sleep(1)

        try:

            API_URL = "https://google-drive-ai-agent-47b2.onrender.com/chat"

            response = requests.post(
                API_URL,
                json={"message": query},
                timeout=60
            )

            if response.status_code != 200:

                assistant_response = (
                    f"❌ Backend Error: {response.status_code}"
                )

            else:

                data = response.json()

                # SAFE RESPONSE PARSING
                assistant_response = ""

                if isinstance(data, dict):

                    if "response" in data:
                        assistant_response = str(data["response"])

                    elif "result" in data:
                        assistant_response = str(data["result"])

                    elif "output" in data:
                        assistant_response = str(data["output"])

                    elif "error" in data:
                        assistant_response = f"❌ {data['error']}"

                    else:
                        assistant_response = str(data)

                else:
                    assistant_response = str(data)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })

            # Display assistant response
            st.markdown(f"""
            <div class="chat-box">
                <div class="assistant-msg">
                    🤖 {assistant_response}
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:

            error_message = f"""
            ⚠️ Unable to connect to backend server.

            Error:
            {str(e)}
            """

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })

            st.markdown(f"""
            <div class="chat-box">
                <div class="assistant-msg">
                    {error_message}
                </div>
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
