from googleapiclient.discovery import build


class GoogleDriveService:

    def __init__(self, creds):

        self.service = build(
            'drive',
            'v3',
            credentials=creds
        )

    def search_files(self, folder_id, query):

        drive_query = f"{query} and trashed=false"

        results = self.service.files().list(
            q=drive_query,
            pageSize=20,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()

        return results.get('files', [])