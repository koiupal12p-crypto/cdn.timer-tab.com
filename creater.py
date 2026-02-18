import os
import random
import string
import re
from datetime import datetime, timedelta

# ==============================================================================
# GENERATOR PRO - VIDEO PLATFORM & CINEMA EDITION (2026)
# ==============================================================================
# - Hybrid Content: Keywords driven content generation
# - Visual Mesh Linking: Grid-style suggested videos
# - SpamBrain Bypass: Contextual Camouflage
# - SEO Safe: Chain + Cluster Linking
# ==============================================================================

class ContinuousGenerator:
    def __init__(self):
        self.templates = {}
        self.template_names = ["test.html", "test1.html", "test2.html"]
        self.keywords_ar = []
        self.keywords_en = []
        self.max_files_per_folder = 500
        self.emojis = ["🔥", "🎥", "🎬", "📺", "✅", "🌟", "✨", "💎", "⚡", "🍿"]
        
        # مصفوفة فارغة بناءً على طلبك لإزالة أي جمل نقدية جاهزة
        self.review_hooks_ar = []

        self.load_all_templates()
        self.load_keywords()
        self.domain = self.load_domain()

    def load_all_templates(self):
        for t_name in self.template_names:
            if os.path.exists(t_name):
                with open(t_name, "r", encoding="utf-8") as f:
                    self.templates[t_name] = f.read()
                print(f"[*] Template {t_name} loaded.")
            else:
                print(f"[!] {t_name} not found. Ensure templates exist.")

    def load_keywords(self):
        # تحميل الكلمات من الملفات الخارجية لضمان النظافة التامة
        if os.path.exists("keywords_ar.txt"):
            with open("keywords_ar.txt", "r", encoding="utf-8") as f:
                self.keywords_ar = [l.strip() for l in f if l.strip()]
        if os.path.exists("keywords_en.txt"):
            with open("keywords_en.txt", "r", encoding="utf-8") as f:
                self.keywords_en = [l.strip() for l in f if l.strip()]

    def load_domain(self):
        if os.path.exists("CNAME"):
            with open("CNAME", "r", encoding="utf-8") as f:
                domain = f.read().strip()
                return domain.replace("https://", "").replace("http://", "")
        return "example.org"

    def build_hybrid_content(self, min_words, max_words, mode="ar"):
        """
        توليد محتوى يعتمد كلياً وبشكل حصري على ملفات الكلمات المرفقة
        """
        target_length = random.randint(min_words, max_words)
        source = self.keywords_ar if mode == "ar" else self.keywords_en
        
        if not source:
            return "Content update in progress."

        content_parts = []
        
        # تعبئة المحتوى بالكلمات المفتاحية فقط حتى الوصول للطول المطلوب
        while len(" ".join(content_parts).split()) < target_length:
            content_parts.append(random.choice(source))
                
        return " ".join(content_parts)

    def get_target_path(self, total_count):
        paths = []
        files_remaining = total_count
        while files_remaining > 0:
            # تسميات مسارات المجلدات
            d1 = random.choice(["media", "vault", "production", "library", "archive"])
            d2 = ''.join(random.choices(string.ascii_lowercase, k=3))
            full_path = os.path.join(d1, d2)
            os.makedirs(full_path, exist_ok=True)
            paths.append(full_path)
            files_remaining -= self.max_files_per_folder
        return paths

    def build_internal_links(self, current_index, generated_files):
        """
        بناء شبكة الربط الداخلي المتوافق مع تصميم Grid الفيديوهات
        """
        current_file = generated_files[current_index]
        current_folder = current_file["folder"]
        selected_links = []
        
        # الربط التسلسلي (Chain)
        if current_index > 0:
            selected_links.append(generated_files[current_index - 1])
        if current_index < len(generated_files) - 1:
            selected_links.append(generated_files[current_index + 1])

        # ربط العناقيد (Cluster)
        same_folder = [f for idx, f in enumerate(generated_files) 
                       if f["folder"] == current_folder and idx != current_index]
        random.shuffle(same_folder)
        selected_links.extend(same_folder[:4])

        # تنويع الروابط (Deep Links)
        other_folders = [f for f in generated_files if f["folder"] != current_folder]
        random.shuffle(other_folders)
        selected_links.extend(other_folders[:2])

        links_html = ""
        seen_urls = set()
        
        for link in selected_links:
            url = f"https://{self.domain}/{link['folder'].replace(os.sep, '/')}/{link['filename']}"
            if url not in seen_urls:
                links_html += f"""
                <a href='{url}' class='related-item'>
                    <div class='thumb-mock'>VIDEO PREVIEW</div>
                    <div class='related-info'>{link['display_title']}</div>
                </a>"""
                seen_urls.add(url)

        return links_html

    def run_single_cycle(self, count=150):
        folder_paths = self.get_target_path(count)
        base_time = datetime.utcnow()
        files_to_create = []

        # تجهيز البيانات بناءً على الكلمات المحملة فقط
        for folder in folder_paths:
            num_in_folder = min(count, self.max_files_per_folder)
            for _ in range(num_in_folder):
                if not self.keywords_ar:
                    print("[!] No keywords found. Skipping generation.")
                    return

                # استخلاص عنوان من الكلمات المتاحة مباشرة
                raw_title = random.choice(self.keywords_ar)
                prefix = random.choice(["شاهد:", "حصرياً:", "فيديو:", "HD:", "جديد:"])
                display_title = f"{random.choice(self.emojis)} {prefix} {raw_title}"
                
                clean_name = re.sub(r'[^\w\s-]', '', raw_title.lower())
                slug = re.sub(r'[-\s]+', '-', clean_name).strip('-')[:80]
                if not slug: slug = ''.join(random.choices(string.ascii_lowercase, k=10))

                files_to_create.append({
                    "display_title": display_title,
                    "filename": f"{slug}.html",
                    "desc": self.build_hybrid_content(120, 200),
                    "folder": folder,
                    "date_iso": (base_time - timedelta(minutes=random.randint(1, 1440))).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "template": random.choice(self.template_names)
                })

        # عملية حقن البيانات في القوالب
        for i, file_data in enumerate(files_to_create):
            template_content = self.templates.get(file_data['template'], "")
            if not template_content: continue
            
            canonical_url = f"https://{self.domain}/{file_data['folder'].replace(os.sep, '/')}/{file_data['filename']}"
            internal_links = self.build_internal_links(i, files_to_create)

            content = template_content
            content = content.replace("{{TITLE}}", file_data['display_title'])
            content = content.replace("{{DESCRIPTION}}", file_data['desc'])
            content = content.replace("{{CANONICAL_URL}}", canonical_url)
            content = content.replace("{{INTERNAL_LINKS}}", internal_links)
            content = content.replace("{{DOMAIN_NAME}}", self.domain)
            content = content.replace("{{DATE}}", file_data['date_iso'])

            target_file = os.path.join(file_data['folder'], file_data['filename'])
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✅ Generated {len(files_to_create)} clean, keywords-only pages.")

if __name__ == "__main__":
    generator = ContinuousGenerator()
    generator.run_single_cycle(count=150)