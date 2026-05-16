import streamlit as st
import requests

API_URL = "https://google-drive-ai-agent-47b2.onrender.com"

st.set_page_config(
    page_title="Google Drive AI Agent",
    page_icon="📁",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

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

    if st.button("Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# ---------------- CHAT MEMORY ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ---------------- #

st.title("📁 Google Drive AI Agent")

st.markdown("Search files using natural language.")

st.caption("Try: PDFs • invoices • videos • reports • excel sheets")

st.markdown("")

# ---------------- DISPLAY OLD CHAT ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "files" in message:

            for file in message["files"]:

                st.markdown(
                    f"- [{file['name']}]({file['webViewLink']})"
                )

# ---------------- USER INPUT ---------------- #

prompt = st.chat_input("Ask about your files...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching Google Drive..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"message": prompt}
                )

                data = response.json()

                files = data.get("files", [])

                if files:

                    st.success(f"Found {len(files)} file(s).")

                    for file in files:

                        st.markdown(
                            f"- [{file['name']}]({file['webViewLink']})"
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

                st.error(str(e))

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": str(e)
                })

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    "Built with ❤️ using Streamlit, FastAPI, LangChain & Google Drive API"
)
