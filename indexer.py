import json
import time
import os
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

# إعدادات الأرشفة - إعدادات ثابتة لعام 2026
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
JSON_KEY = "service_account.json"
URLS_FILE = "urls.txt"

def run_indexer():
    # التأكد من وجود الملفات
    if not os.path.exists(JSON_KEY):
        print(f"❌ خطأ: ملف {JSON_KEY} غير موجود!")
        return
    if not os.path.exists(URLS_FILE):
        print(f"❌ خطأ: ملف {URLS_FILE} غير موجود! أنشئ الملف وضع الروابط بداخله.")
        return

    # المصادقة مع جوجل
    print("🔐 جاري الاتصال بخوادم جوجل...")
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, SCOPES)
        http = credentials.authorize(httplib2.Http())
    except Exception as e:
        print(f"❌ فشل في المصادقة: {e}")
        return

    # قراءة الروابط
    with open(URLS_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("ℹ️ ملف الروابط فارغ.")
        return

    print(f"🚀 تم العثور على {len(urls)} رابط. جاري البدء...")

    # إرسال الروابط
    for index, url in enumerate(urls):
        # جوجل تسمح بـ 200 طلب كحد أقصى يومياً للحساب الواحد
        if index >= 200:
            print("🛑 توقف! تم الوصول للحد اليومي (200 رابط).")
            break

        data = {"url": url, "type": "URL_UPDATED"}
        try:
            response, content = http.request(ENDPOINT, method="POST", body=json.dumps(data))
            
            if response.status == 200:
                print(f"✅ [{index+1}] تم الإرسال بنجاح: {url}")
            else:
                print(f"⚠️ [{index+1}] خطأ {response.status} في الرابط: {url}")
                print(f"السبب: {content.decode()}")
        except Exception as e:
            print(f"❌ خطأ تقني في الرابط {url}: {e}")
        
        # تأخير بسيط لتجنب ضغط الشبكة
        time.sleep(1)

    print("\n✨ انتهت المهمة. تفقد Google Search Console غداً لمتابعة النتائج.")

if __name__ == "__main__":
    run_indexer()
