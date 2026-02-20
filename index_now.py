import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# إعداد الملفات
JSON_KEYFILE = 'anyq-488010-76c7d406dc22.json'
URLS_FILE = 'urls.txt'

def run_indexing():
    # التحميل من ملف المفتاح
    scopes = ["https://www.googleapis.com/auth/indexing"]
    credentials = service_account.Credentials.from_service_account_file(JSON_KEYFILE, scopes=scopes)
    service = build('indexing', 'v3', credentials=credentials)

    # قراءة الروابط من urls.txt
    try:
        with open(URLS_FILE, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("خطأ: ملف urls.txt غير موجود")
        return

    print(f"تم العثور على {len(urls)} رابط. جاري الإرسال...")

    for url in urls:
        body = {
            "url": url,
            "type": "URL_UPDATED"
        }
        try:
            res = service.urlNotifications().publish(body=body).execute()
            print(f"تم بنجاح: {url}")
        except HttpError as e:
            print(f"خطأ في الرابط {url}: {e}")
        
        # تأخير بسيط لتجنب الضغط على السيرفر
        time.sleep(1)

if __name__ == "__main__":
    run_indexing()
