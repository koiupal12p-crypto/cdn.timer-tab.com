import requests
import json
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import time

SITEMAP_URL = "https://cdn.timer-tab.com/map-root.xml"
JSON_KEY_FILE = "anyq-488010-76c7d406dc22.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_urls(url):
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # إذا كانت الخريطة تحتوي على خرائط أخرى (Sitemap Index)
        sitemaps = root.findall(".//ns:sitemap/ns:loc", ns)
        if sitemaps:
            all_links = []
            for sm in sitemaps:
                all_links.extend(get_urls(sm.text))
            return all_links
        
        # إذا كانت خريطة روابط مباشرة
        return [node.text for node in root.findall(".//ns:url/ns:loc", ns)]
    except Exception as e:
        print(f"❌ خطأ في قراءة الخريطة: {e}")
        return []

def run():
    print("🔍 سحب الروابط بعمق...")
    all_urls = list(set(get_urls(SITEMAP_URL))) # حذف المتكرر
    print(f"✅ تم العثور على {len(all_urls)} رابط إجمالي.")

    if not all_urls: return

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, SCOPES)
        http_auth = credentials.authorize(httplib2.Http())
        
        # أخذ أول 200 رابط لم يتم أرشفتهم (أو أول 200 فقط حالياً)
        to_index = all_urls[:200] 

        for i, url in enumerate(to_index):
            endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
            data = json.dumps({"url": url, "type": "URL_UPDATED"})
            response, content = http_auth.request(endpoint, method="POST", body=data)
            print(f"[{i+1}] Status {response.status} - {url}")
            time.sleep(0.5)
            
    except Exception as e:
        print(f"💥 خطأ تقني في المفتاح أو الاتصال: {e}")

if name == "main":
    run()
