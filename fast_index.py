import requests
import json
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import time

# --- الإعدادات ---
SITEMAP_URL = "https://cdn.timer-tab.com/map-root.xml"
JSON_KEY_FILE = "anyq-488010-76c7d406dc22.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_urls(url):
    urls = []
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        # التعامل مع الـ Namespace الخاص بجوجل في ملفات الـ XML
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # البحث عن خرائط فرعية (في حال كانت خريطة فهرس)
        sitemaps = root.findall(".//ns:sitemap/ns:loc", ns)
        if sitemaps:
            for sm in sitemaps:
                urls.extend(get_urls(sm.text))
        
        # البحث عن روابط مباشرة
        pages = root.findall(".//ns:url/ns:loc", ns)
        for pg in pages:
            urls.append(pg.text)
            
    except Exception as e:
        print(f"⚠️ تنبيه: تعذر قراءة الخريطة {url} بسبب {e}")
    return list(set(urls)) # حذف الروابط المكررة

def run_indexing():
    print("🔍 جاري فحص الروابط بعمق من الخرائط الفرعية...")
    all_urls = get_urls(SITEMAP_URL)
    print(f"✅ مذهل! تم اكتشاف {len(all_urls)} رابط إجمالي.")

    if not all_urls:
        print("❌ لم يتم العثور على روابط. تأكد من صحة رابط الـ Sitemap.")
        return

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, SCOPES)
        http_auth = credentials.authorize(httplib2.Http())
        
        # إرسال أول 200 رابط (الحصة اليومية)
        to_index = all_urls[:200]
        print(f"🚀 بدء إرسال أول {len(to_index)} رابط للأرشفة القسرية...")

        for i, url in enumerate(to_index):
            endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
            data = json.dumps({"url": url, "type": "URL_UPDATED"})
            response, content = http_auth.request(endpoint, method="POST", body=data)
            
            # طباعة النتيجة: 200 تعني نجاح، 403 تعني مشكلة صلاحيات
            print(f"[{i+1}] Status: {response.status} | URL: {url}")
            time.sleep(1) # فاصل زمني بسيط لتجنب الضغط على الـ API

    except Exception as e:
        print(f"💥 خطأ فادح: {e}")

if name == "main":
    run_indexing()
