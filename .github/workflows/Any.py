import requests
import json
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import time

# الإعدادات
SITEMAP_URL = "https://cdn.timer-tab.com/map-root.xml"
JSON_KEY_FILE = "anyq-488010-76c7d406dc22.json" # تأكد أن هذا هو نفس اسم الملف في الصورة
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_urls_from_sitemap(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    # فك تشفير روابط خريطة الموقع (namespace)
    urls = [node.text for node in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    return urls

def send_to_google(url, http_auth):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    content = json.dumps({"url": url, "type": "URL_UPDATED"})
    response, content_body = http_auth.request(endpoint, method="POST", body=content)
    return response.status

# بدء العمل
print("🔍 سحب الروابط من خريطة الموقع...")
all_urls = get_urls_from_sitemap(SITEMAP_URL)
print(f"✅ تم العثور على {len(all_urls)} رابط.")

# حصة جوجل هي 200 رابط يومياً لكل حساب خدمة
to_index = all_urls[:200] 

credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, SCOPES)
http_auth = credentials.authorize(httplib2.Http())

print("🚀 إرسال أول 200 رابط للأرشفة القسرية...")
for i, url in enumerate(to_index):
    status = send_to_google(url, http_auth)
    print(f"[{i+1}/200] Status {status} - {url}")
    time.sleep(0.5) # حماية من الحظر

print("🎉 انتهت الدفعة الأولى! كرر العملية غداً للـ 200 التالية.")
