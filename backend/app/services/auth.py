from google.oauth2 import service_account
import json
import os

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def authenticate_google():

    service_account_info = json.loads(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    )

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    return creds