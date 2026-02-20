import json
import time
import os
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

# اسم ملف المفتاح الخاص بك
JSON_KEY = "anyq-488010-76c7d406dc22.json"
URLS_FILE = "urls.txt"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def run_indexer():
    if not os.path.exists(JSON_KEY):
        print(f"❌ الملف {JSON_KEY} غير موجود!")
        return

    print("🔐 جاري تجهيز المفتاح والمصادقة...")
    
    try:
        # قراءة الملف وتنظيف المفتاح الخاص برمجياً
        with open(JSON_KEY, "r") as f:
            key_data = json.load(f)
            # إصلاح مشكلة الـ JWT Signature عن طريق التأكد من تنسيق السطور
            if 'private_key' in key_data:
                key_data['private_key'] = key_data['private_key'].replace('\\n', '\n')
        
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_data, SCOPES)
        http = credentials.authorize(httplib2.Http())
    except Exception as e:
        print(f"❌ فشل في قراءة المفتاح: {e}")
        return

    if not os.path.exists(URLS_FILE):
        print("❌ ملف urls.txt غير موجود!")
        return

    with open(URLS_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"🚀 البدء بإرسال {len(urls)} رابط لجوجل...")

    for index, url in enumerate(urls):
        if index >= 200: break
        
        data = {"url": url, "type": "URL_UPDATED"}
        try:
            # إرسال الطلب
            response, content = http.request(ENDPOINT, method="POST", body=json.dumps(data))
            
            if response.status == 200:
                print(f"✅ [{index+1}] نجاح -> {url}")
            else:
                # طباعة الخطأ بشكل واضح بعيداً عن الرابط
                error_msg = json.loads(content.decode())
                print(f"⚠️ [{index+1}] فشل! الكود: {response.status}")
                print(f"السبب: {error_msg.get('error', {}).get('message', 'خطأ غير معروف')}")
        except Exception as e:
            print(f"❌ خطأ في الرابط {url}: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    run_indexer()
