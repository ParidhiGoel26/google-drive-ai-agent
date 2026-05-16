from typing import TypedDict
import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from app.services.auth import authenticate_google
from app.services.drive_service import GoogleDriveService

load_dotenv()

FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")


class AgentState(TypedDict):

    user_input: str
    search_query: str
    results: list
    response: str


def generate_query(state):

    user_input = state["user_input"].lower()

    # PDFs
    if "pdf" in user_input:
        query = "mimeType='application/pdf'"

    # Videos
    elif "video" in user_input:
        query = "mimeType contains 'video/'"

    # Images
    elif "image" in user_input or "photo" in user_input:
        query = "mimeType contains 'image/'"

    # Excel files
    elif "excel" in user_input or "sheet" in user_input:
        query = (
            "mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
        )

    # Folders
    elif "folder" in user_input:
        query = "mimeType='application/vnd.google-apps.folder'"

    # Reports
    elif "report" in user_input:
        query = "name contains 'Report'"

    # Default search
    else:
        query = "trashed=false"

    return {
        "search_query": query
    }


def execute_search(state):

    creds = authenticate_google()

    drive_service = GoogleDriveService(creds)

    results = drive_service.search_files(
        FOLDER_ID,
        state["search_query"]
    )

    return {
        "results": results
    }


def generate_response(state):

    files = state["results"]

    if not files:
        return {
            "response": "No matching files found."
        }

    response_text = "## I found these files:\n\n"

    for file in files:

        mime = file.get("mimeType", "")

        icon = "📄"

        if "image" in mime:
            icon = "🖼️"

        elif "video" in mime:
            icon = "🎥"

        elif "spreadsheet" in mime:
            icon = "📊"

        elif "folder" in mime:
            icon = "📁"

        elif "pdf" in mime:
            icon = "📄"

        response_text += (
            f"{icon} "
            f"[{file['name']}]({file['webViewLink']})\n\n"
        )

    return {
        "response": response_text
    }


workflow = StateGraph(AgentState)

workflow.add_node(
    "generate_query",
    generate_query
)

workflow.add_node(
    "execute_search",
    execute_search
)

workflow.add_node(
    "generate_response",
    generate_response
)

workflow.set_entry_point("generate_query")

workflow.add_edge(
    "generate_query",
    "execute_search"
)

workflow.add_edge(
    "execute_search",
    "generate_response"
)

workflow.add_edge(
    "generate_response",
    END
)

agent = workflow.compile()