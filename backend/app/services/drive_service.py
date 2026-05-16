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

        drive_query = (
            f"'{folder_id}' in parents and trashed=false"
        )

        # PDFs
        if "pdf" in query:

            drive_query += (
                " and mimeType='application/pdf'"
            )

        # Videos
        elif "video" in query:

            drive_query += (
                " and mimeType contains 'video/'"
            )

        # Images
        elif "image" in query:

            drive_query += (
                " and mimeType contains 'image/'"
            )

        # Excel
        elif "excel" in query or "sheet" in query:

            drive_query += (
                " and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
            )

        # Folders
        elif "folder" in query:

            drive_query += (
                " and mimeType='application/vnd.google-apps.folder'"
            )

        results = self.service.files().list(
            q=drive_query,
            pageSize=20,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()

        return results.get('files', [])