import requests
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/indexing"]
SERVICE_ACCOUNT_FILE = "credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
credentials.refresh(Request())

access_token = credentials.token

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    data = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response = requests.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers=headers,
        data=json.dumps(data),
    )
    print(response.status_code, response.text)
