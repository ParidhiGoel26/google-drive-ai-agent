from googleapiclient.discovery import build


class GoogleDriveService:

    def __init__(self, creds):

        self.service = build(
            'drive',
            'v3',
            credentials=creds
        )

    def search_files(self, folder_id, query):

        query = query.lower()

        mime_query = "trashed=false"

        # PDFs
        if "pdf" in query:
            mime_query += " and mimeType='application/pdf'"

        # Videos
        elif "video" in query:
            mime_query += " and mimeType contains 'video/'"

        # Images
        elif "image" in query:
            mime_query += " and mimeType contains 'image/'"

        # Excel files
        elif "excel" in query or "sheet" in query:
            mime_query += (
                " and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
            )

        # Folders
        elif "folder" in query:
            mime_query += (
                " and mimeType='application/vnd.google-apps.folder'"
            )

        final_query = f"'{folder_id}' in parents and {mime_query}"

        results = self.service.files().list(
            q=final_query,
            pageSize=20,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()

        files = results.get('files', [])

        formatted_files = []

        for file in files:

            formatted_files.append({
    "name": file.get("name", "Unknown File"),
    "url": file.get(
        "webViewLink",
        f"https://drive.google.com/file/d/{file.get('id')}/view"
    )
})

        return formatted_files
