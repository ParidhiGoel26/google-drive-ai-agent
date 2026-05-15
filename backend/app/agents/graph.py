from typing import TypedDict
import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from app.services.llm_service import llm
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

    prompt = f"""
    You are a Google Drive API query generator.

    Convert the user request into ONLY a valid Google Drive API q query.

    Rules:
    - Use name contains
    - Use mimeType
    - Use fullText contains
    - Use modifiedTime
    - Return ONLY query text

    Examples:

    User: Find PDFs
    Output:
    mimeType='application/pdf'

    User: Find reports
    Output:
    name contains 'report'

    User: Find invoice documents
    Output:
    fullText contains 'invoice'

    User: Show images
    Output:
    mimeType contains 'image/'

    User: Show videos
    Output:
    mimeType contains 'video/'

    User: Show excel files
    Output:
    mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    User: Show folders
    Output:
    mimeType='application/vnd.google-apps.folder'

    User Request:
    {state['user_input']}
    """

    response = llm.invoke(prompt)

    return {
        "search_query": response.content.strip()
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