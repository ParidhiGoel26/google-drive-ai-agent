import os

from dotenv import load_dotenv

from app.services.auth import authenticate_google
from app.services.drive_service import GoogleDriveService

load_dotenv()

FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

creds = authenticate_google()

drive_service = GoogleDriveService(creds)

results = drive_service.search_files(
    FOLDER_ID,
    "name contains 'report'"
)

print(results)