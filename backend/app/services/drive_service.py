from googleapiclient.discovery import build


class GoogleDriveService:

    def __init__(self, creds):

        self.service = build(
            'drive',
            'v3',
            credentials=creds
        )

    def search_files(self, folder_id, query):

        final_query = f"'{folder_id}' in parents and {query}"

        results = self.service.files().list(
            q=final_query,
            pageSize=10,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()

        return results.get('files', [])