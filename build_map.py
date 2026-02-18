import os
import subprocess
import urllib.parse
import math
from datetime import datetime

# ==========================================
# Extract site URL (CNAME has priority)
# ==========================================
def get_site_url():
    if os.path.isfile("CNAME"):
        with open("CNAME", "r", encoding="utf-8") as f:
            domain = f.read().strip()
            if domain:
                return f"https://{domain}"

    try:
        remote = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        if remote.startswith("git@"):  # SSH URL
            user, repo = remote.replace("git@github.com:", "").replace(".git", "").split("/")
        else:  # HTTPS URL
            user, repo = remote.replace("https://github.com/", "").replace(".git", "").split("/")
        return f"https://{user}.github.io/{repo}"
    except:
        return "https://example.org"

SITE_URL = get_site_url()

# ==========================================
# Settings
# ==========================================
EXCLUDED_DIRS = {".git", ".github", "assets", "css", "js"}
EXCLUDED_FILES = {"404.html"}
URLS_PER_FILE = 5000

# أسماء ملفات السايت ماب
SITEMAP_FILES = ["map-main.xml", "map-pages.xml", "map-videos.xml", "map-extra.xml"]
NEWS_SITEMAP_NAME = "map-news.xml"

# ==========================================
def last_modified(path):
    try:
        # محاولة الحصول على تاريخ آخر تعديل من جيتهاب
        return subprocess.check_output([
            "git", "log", "-1", "--format=%cd", "--date=short", "--", path
        ]).decode().strip()
    except:
        return datetime.today().strftime("%Y-%m-%d")

# ==========================================
def main():
    urls = []
    today = datetime.today().strftime("%Y-%m-%d")

    # جمع روابط HTML
    for root, dirs, files in os.walk(".", topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]
        for file in files:
            if not file.endswith(".html") or file in EXCLUDED_FILES:
                continue

            path = os.path.join(root, file).replace("\\", "/").lstrip("./")

            # شرط: يجب أن يحتوي path على مسار فرعي واحد على الأقل
            if "/" not in path:
                continue 

            url = f"{SITE_URL}/{urllib.parse.quote(path)}"
            mod_date = last_modified(path)
            urls.append({
                "url": url,
                "mod": mod_date,
                "path": path,
                "name": file.replace(".html", "").replace("-", " ")
            })

    # حذف ملفات السايت ماب القديمة
    for f in os.listdir("."):
        if (f.startswith("map-") or f == "map-news.xml") and f.endswith(".xml"):
            try:
                os.remove(f)
            except:
                pass

    # --- 1. إنشاء خريطة أخبار جوجل (Google News Sitemap) ---
    # تشمل الملفات التي تم تعديلها أو إنشاؤها اليوم فقط (آخر 48 ساعة تقنياً)
    news_urls = [u for u in urls if u["mod"] == today]
    if news_urls:
        news_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
        ]
        for item in news_urls[:1000]: # جوجل نيوز تقبل حتى 1000 رابط
            news_content.append(f"""
  <url>
    <loc>{item['url']}</loc>
    <news:news>
      <news:publication>
        <news:name>{SITE_URL.replace('https://', '')}</news:name>
        <news:language>ar</news:language>
      </news:publication>
      <news:publication_date>{item['mod']}T00:00:00+00:00</news:publication_date>
      <news:title>{item['name']}</news:title>
    </news:news>
  </url>""")
        news_content.append("</urlset>")
        with open(NEWS_SITEMAP_NAME, "w", encoding="utf-8") as f:
            f.write("\n".join(news_content))
        print(f"📰 News Sitemap generated with {len(news_urls)} recent items.")

    # --- 2. إنشاء خرائط الموقع العادية ---
    sitemap_files = []
    if news_urls: sitemap_files.append(NEWS_SITEMAP_NAME)
    
    parts = math.ceil(len(urls) / URLS_PER_FILE)
    for i in range(parts):
        filename = SITEMAP_FILES[i] if i < len(SITEMAP_FILES) else f"map-extra{i}.xml"
        sitemap_files.append(filename)
        content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for item in urls[i*URLS_PER_FILE:(i+1)*URLS_PER_FILE]:
            content.append(f"""
  <url>
    <loc>{item['url']}</loc>
    <lastmod>{item['mod']}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""")
        content.append("</urlset>")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    # --- 3. إنشاء ملف الفهرس الرئيسي (Index) ---
    index = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for sm in sitemap_files:
        index.append(f"""
  <sitemap>
    <loc>{SITE_URL}/{sm}</loc>
    <lastmod>{today}</lastmod>
  </sitemap>""")
    index.append("</sitemapindex>")
    with open("map-root.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(index))

    print(f"✅ Done: {len(urls)} total pages indexed.")
    print(f"🚀 Main Index: {SITE_URL}/map-root.xml")

if __name__ == "__main__":
    main()