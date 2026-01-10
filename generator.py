# # LocalLead Automator.py/generator.py
#
# """
# Phase 3: Website Preview Generation
# Generate beautiful HTML preview websites for each business
# """
# import os
# import re
# import pandas as pd
# from pathlib import Path
# import config
# from utils import setup_logging
#
# logger = setup_logging(config.LOG_FILE)
#
# BASE_DIR = Path(__file__).resolve().parent
#
#
# class PreviewGenerator:
#     def __init__(self):
#         # self.template_path = "templates/dental_preview.html"
#         # self.output_dir = "previews"
#
#         self.template_path = BASE_DIR / "templates" / "dental_preview.html"
#         self.output_dir = BASE_DIR / "previews"
#
#         self.template_content = None
#
#     def load_template(self):
#         """Load the HTML template"""
#         try:
#             with open(self.template_path, 'r', encoding='utf-8') as f:
#                 self.template_content = f.read()
#             logger.info(f"✓ Template loaded: {self.template_path}")
#         except FileNotFoundError:
#             logger.error(f"Template not found: {self.template_path}")
#             raise
#
#     def slugify(self, text):
#         """Convert business name to URL-friendly slug"""
#         text = text.lower()
#         text = re.sub(r'[^a-z0-9]+', '-', text)
#         text = text.strip('-')
#         return text[:50]  # Limit length
#
#     def render_services(self, services_text):
#         """Convert services text to HTML cards"""
#         if not services_text or services_text == "N/A":
#             return ""
#
#         services = services_text.split(';')
#         html = ""
#
#         for service in services:
#             service = service.strip()
#             if service:
#                 html += f'''
#                 <div class="bg-white p-6 rounded-xl card-shadow hover:shadow-xl transition">
#                     <div class="text-purple-600 text-3xl mb-3">
#                         <i class="fas fa-tooth"></i>
#                     </div>
#                     <h3 class="font-semibold text-lg text-gray-800">{service}</h3>
#                 </div>
#                 '''
#
#         return html
#
#     def render_reviews(self, row):
#         """Convert reviews to HTML cards"""
#         html = ""
#
#         for i in range(1, config.MAX_REVIEWS_TO_SCRAPE + 1):
#             review_name = row.get(f'review_{i}_name', 'N/A')
#             review_rating = row.get(f'review_{i}_rating', 'N/A')
#             review_text = row.get(f'review_{i}_text', 'N/A')
#
#             # Skip if no text
#             if not review_text or review_text == 'N/A':
#                 continue
#
#             # Generate star rating HTML
#             try:
#                 rating_num = int(float(review_rating))
#             except:
#                 rating_num = 5
#
#             stars = '<i class="fas fa-star text-yellow-400"></i>' * rating_num
#
#             html += f'''
#             <div class="bg-gray-50 p-6 rounded-xl card-shadow">
#                 <div class="flex items-center gap-2 mb-3">
#                     <div class="flex gap-1">
#                         {stars}
#                     </div>
#                 </div>
#                 <p class="text-gray-700 mb-4 italic">"{review_text}"</p>
#                 <p class="font-semibold text-gray-800">- {review_name if review_name != 'N/A' else 'Anonymous'}</p>
#             </div>
#             '''
#
#         return html
#
#     def render_hours(self, hours_text):
#         """Convert hours text to HTML table"""
#         if not hours_text or hours_text == "N/A":
#             return ""
#
#         hours_list = hours_text.split(';')
#         html = ""
#
#         for hour_entry in hours_list:
#             hour_entry = hour_entry.strip()
#             if ':' in hour_entry:
#                 day, time = hour_entry.split(':', 1)
#                 html += f'''
#                 <div class="flex justify-between py-3 border-b border-gray-200 last:border-0">
#                     <span class="font-semibold text-gray-800">{day.strip()}</span>
#                     <span class="text-gray-600">{time.strip()}</span>
#                 </div>
#                 '''
#
#         return html
#
#     def generate_preview(self, business_row):
#         """Generate HTML preview for a single business"""
#         try:
#             business_name = business_row['business_name']
#             logger.info(f"🎨 Generating preview: {business_name}")
#
#             # Create slug for filename
#             slug = self.slugify(business_name)
#             filename = f"{slug}.html"
#             filepath = os.path.join(self.output_dir, filename)
#
#             # Start with template
#             html = self.template_content
#
#             # Replace basic placeholders
#             replacements = {
#                 '{{business_name}}': business_row.get('business_name', 'Dental Clinic'),
#                 '{{category}}': business_row.get('category', 'Dental Clinic'),
#                 '{{city}}': business_row.get('city', ''),
#                 '{{address}}': business_row.get('address', ''),
#                 '{{phone}}': business_row.get('phone', ''),
#                 '{{rating}}': str(business_row.get('rating', 'N/A')),
#                 '{{review_count}}': str(
#                     int(business_row.get('review_count', 0)) if business_row.get('review_count') != 'N/A' else 0),
#                 '{{maps_url}}': business_row.get('maps_url', '#'),
#             }
#
#             for placeholder, value in replacements.items():
#                 html = html.replace(placeholder, str(value))
#
#             # Conditional sections
#             # Rating section
#             if business_row.get('rating') and business_row.get('rating') != 'N/A':
#                 html = html.replace('{{if_rating}}', '').replace('{{endif_rating}}', '')
#             else:
#                 html = re.sub(r'{{if_rating}}.*?{{endif_rating}}', '', html, flags=re.DOTALL)
#
#             # About section
#             about = business_row.get('about_business', 'N/A')
#             if about and about != 'N/A' and len(about) > 10:
#                 html = html.replace('{{if_about}}', '').replace('{{endif_about}}', '')
#                 html = html.replace('{{about_business}}', about)
#             else:
#                 html = re.sub(r'{{if_about}}.*?{{endif_about}}', '', html, flags=re.DOTALL)
#
#             # Services section
#             services = business_row.get('services', 'N/A')
#             if services and services != 'N/A':
#                 services_html = self.render_services(services)
#                 if services_html:
#                     html = html.replace('{{if_services}}', '').replace('{{endif_services}}', '')
#                     html = html.replace('{{services_list}}', services_html)
#                 else:
#                     html = re.sub(r'{{if_services}}.*?{{endif_services}}', '', html, flags=re.DOTALL)
#             else:
#                 html = re.sub(r'{{if_services}}.*?{{endif_services}}', '', html, flags=re.DOTALL)
#
#             # Reviews section
#             reviews_html = self.render_reviews(business_row)
#             if reviews_html:
#                 html = html.replace('{{if_reviews}}', '').replace('{{endif_reviews}}', '')
#                 html = html.replace('{{reviews_list}}', reviews_html)
#             else:
#                 html = re.sub(r'{{if_reviews}}.*?{{endif_reviews}}', '', html, flags=re.DOTALL)
#
#             # Hours section
#             hours = business_row.get('opening_hours', 'N/A')
#             if hours and hours != 'N/A':
#                 hours_html = self.render_hours(hours)
#                 if hours_html:
#                     html = html.replace('{{if_hours}}', '').replace('{{endif_hours}}', '')
#                     html = html.replace('{{hours_list}}', hours_html)
#                 else:
#                     html = re.sub(r'{{if_hours}}.*?{{endif_hours}}', '', html, flags=re.DOTALL)
#             else:
#                 html = re.sub(r'{{if_hours}}.*?{{endif_hours}}', '', html, flags=re.DOTALL)
#
#             # Maps URL section
#             if business_row.get('maps_url') and business_row.get('maps_url') != 'N/A':
#                 html = html.replace('{{if_maps_url}}', '').replace('{{endif_maps_url}}', '')
#             else:
#                 html = re.sub(r'{{if_maps_url}}.*?{{endif_maps_url}}', '', html, flags=re.DOTALL)
#
#             # Clean up any remaining placeholders
#             html = re.sub(r'{{.*?}}', '', html)
#
#             # Save HTML file
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 f.write(html)
#
#             logger.info(f"✅ Preview generated: {filename}")
#
#             return filename
#
#         except Exception as e:
#             logger.error(f"Error generating preview for {business_row.get('business_name', 'Unknown')}: {e}")
#             return None
#
#     def generate_index(self, previews_data):
#         """Generate index.html listing all previews"""
#         try:
#             html = f'''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Dental Clinic Previews</title>
#     <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-100">
#     <div class="container mx-auto px-6 py-12">
#         <h1 class="text-4xl font-bold mb-8 text-center">Generated Preview Websites</h1>
#         <p class="text-center text-gray-600 mb-12">Total: {len(previews_data)} previews</p>
#
#         <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
# '''
#
#             for preview in previews_data:
#                 html += f'''
#             <a href="{preview['filename']}" class="block bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
#                 <h2 class="text-xl font-bold mb-2 text-purple-600">{preview['business_name']}</h2>
#                 <p class="text-gray-600 mb-2">{preview['category']}</p>
#                 <p class="text-sm text-gray-500">{preview['city']}</p>
#             </a>
# '''
#
#             html += '''
#         </div>
#     </div>
# </body>
# </html>
# '''
#
#             index_path = os.path.join(self.output_dir, 'index.html')
#             with open(index_path, 'w', encoding='utf-8') as f:
#                 f.write(html)
#
#             logger.info(f"✅ Index page generated: {index_path}")
#
#         except Exception as e:
#             logger.error(f"Error generating index: {e}")
#
#     def generate_all(self, input_file, output_file):
#         """Generate preview websites for all enriched businesses"""
#         logger.info(f"Loading enriched leads from {input_file}...")
#
#         try:
#             # Create output directory
#             os.makedirs(self.output_dir, exist_ok=True)
#             os.makedirs('templates', exist_ok=True)
#
#             # Load template
#             self.load_template()
#
#             # Load enriched data
#             df = pd.read_csv(input_file)
#             total = len(df)
#
#             if total == 0:
#                 logger.error("No enriched leads to generate previews for!")
#                 return None
#
#             logger.info(f"Found {total} enriched leads")
#
#             previews_data = []
#             generated_count = 0
#
#             for idx, row in df.iterrows():
#                 logger.info(f"\n--- Generating {idx + 1}/{total} ---")
#
#                 filename = self.generate_preview(row)
#
#                 if filename:
#                     preview_url = f"previews/{filename}"
#                     df.at[idx, 'preview_url'] = preview_url
#
#                     previews_data.append({
#                         'filename': filename,
#                         'business_name': row['business_name'],
#                         'category': row.get('category', ''),
#                         'city': row.get('city', '')
#                     })
#
#                     generated_count += 1
#
#             # Generate index page
#             self.generate_index(previews_data)
#
#             # Save updated CSV with preview URLs
#             df.to_csv(output_file, index=False, encoding='utf-8')
#             logger.info(f"✓ Updated CSV saved: {output_file}")
#
#             logger.info(f"\n{'=' * 60}")
#             logger.info(f"✅ PREVIEW GENERATION COMPLETE!")
#             logger.info(f"{'=' * 60}")
#             logger.info(f"📊 Generated: {generated_count}/{total} preview websites")
#             logger.info(f"📁 Location: {self.output_dir}/")
#             logger.info(f"🌐 Open: {self.output_dir}/index.html to view all previews")
#             logger.info(f"{'=' * 60}")
#
#             return df
#
#         except Exception as e:
#             logger.error(f"Preview generation failed: {e}")
#             raise
#
#
# def run_generator():
#     """Main function to run preview generator"""
#     generator = PreviewGenerator()
#     df = generator.generate_all(config.ENRICHED_DATA_FILE, config.ENRICHED_DATA_FILE)
#     return df

#
# """
# Phase 3: Website Preview Generation
# Generate HTML preview websites from enriched leads (NO scraping here)
# """
#
# import os
# import re
# import pandas as pd
# from pathlib import Path
# import config
# from utils import setup_logging
#
# logger = setup_logging(config.LOG_FILE)
#
# # Absolute project paths (CRITICAL FIX)
# BASE_DIR = Path(__file__).resolve().parent
# TEMPLATES_DIR = BASE_DIR / "templates"
# PREVIEWS_DIR = BASE_DIR / "previews"
#
#
# class PreviewGenerator:
#     def __init__(self):
#         self.template_path = TEMPLATES_DIR / "dental_preview.html"
#         self.output_dir = PREVIEWS_DIR
#         self.template_content = None
#
#     # -------------------------
#     # Utilities
#     # -------------------------
#     def load_template(self):
#         if not self.template_path.exists():
#             raise FileNotFoundError(f"Template not found: {self.template_path}")
#
#         self.template_content = self.template_path.read_text(encoding="utf-8")
#         logger.info(f"✓ Template loaded: {self.template_path}")
#
#     def slugify(self, text: str) -> str:
#         text = text.lower()
#         text = re.sub(r"[^a-z0-9]+", "-", text)
#         return text.strip("-")[:50]
#
#     # -------------------------
#     # Render helpers
#     # -------------------------
#     # def render_services(self, services_text):
#     #     if not services_text or services_text == "N/A":
#     #         return ""
#     #
#     #     html = ""
#     #     for service in services_text.split(";"):
#     #         service = service.strip()
#     #         if service:
#     #             html += f"""
#     #             <div class="bg-white p-6 rounded-xl card-shadow hover:shadow-xl transition">
#     #                 <div class="text-purple-600 text-3xl mb-3">
#     #                     <i class="fas fa-tooth"></i>
#     #                 </div>
#     #                 <h3 class="font-semibold text-lg text-gray-800">{service}</h3>
#     #             </div>
#     #             """
#     #     return html
#
#     def render_services(self, services_text):
#         if not isinstance(services_text, str):
#             return ""
#
#         html = ""
#         for service in services_text.split(";"):
#             service = service.strip()
#             if service:
#                 html += f"""
#                 <div class="bg-white p-6 rounded-xl card-shadow">
#                     <h3 class="font-semibold text-lg">{service}</h3>
#                 </div>
#                 """
#         return html
#
#     def render_reviews(self, row):
#         html = ""
#
#         for i in range(1, config.MAX_REVIEWS_TO_SCRAPE + 1):
#             text = row.get(f"review_{i}_text")
#             if not text or text == "N/A":
#                 continue
#
#             name = row.get(f"review_{i}_name", "Anonymous")
#             rating = row.get(f"review_{i}_rating", 5)
#
#             try:
#                 stars = int(float(rating))
#             except Exception:
#                 stars = 5
#
#             star_html = '<i class="fas fa-star text-yellow-400"></i>' * stars
#
#             html += f"""
#             <div class="bg-gray-50 p-6 rounded-xl card-shadow">
#                 <div class="flex gap-1 mb-3">{star_html}</div>
#                 <p class="italic text-gray-700 mb-4">"{text}"</p>
#                 <p class="font-semibold text-gray-800">- {name}</p>
#             </div>
#             """
#
#         return html
#
#     # def render_hours(self, hours_text):
#     #     if not hours_text or hours_text == "N/A":
#     #         return ""
#     #
#     #     html = ""
#     #     for entry in hours_text.split(";"):
#     #         entry = entry.strip()
#     #         if ":" in entry:
#     #             day, time = entry.split(":", 1)
#     #             html += f"""
#     #             <div class="flex justify-between py-3 border-b last:border-0">
#     #                 <span class="font-semibold">{day.strip()}</span>
#     #                 <span class="text-gray-600">{time.strip()}</span>
#     #             </div>
#     #             """
#     #     return html
#
#     def render_hours(self, hours_text):
#         if not isinstance(hours_text, str):
#             return ""
#
#         html = ""
#         for entry in hours_text.split(";"):
#             entry = entry.strip()
#             if ":" in entry:
#                 day, time = entry.split(":", 1)
#                 html += f"""
#                 <div class="flex justify-between py-3 border-b last:border-0">
#                     <span class="font-semibold">{day.strip()}</span>
#                     <span class="text-gray-600">{time.strip()}</span>
#                 </div>
#                 """
#         return html
#
#     # -------------------------
#     # Preview generation
#     # -------------------------
#     def generate_preview(self, row):
#         try:
#             business_name = row.get("business_name")
#             if not business_name:
#                 raise ValueError("Missing business_name")
#
#             slug = self.slugify(business_name)
#             filepath = self.output_dir / f"{slug}.html"
#
#             html = self.template_content
#
#             replacements = {
#                 "{{business_name}}": business_name,
#                 "{{category}}": row.get("category", ""),
#                 "{{city}}": row.get("city", ""),
#                 "{{address}}": row.get("address", ""),
#                 "{{phone}}": str(row.get("phone", "")),
#                 "{{rating}}": str(row.get("rating", "")),
#                 "{{review_count}}": str(int(row.get("review_count", 0) or 0)),
#                 "{{maps_url}}": row.get("maps_url", "#"),
#                 "{{about_business}}": row.get("about_business", ""),
#             }
#
#             for key, value in replacements.items():
#                 html = html.replace(key, str(value))
#
#             # Conditional sections
#             def toggle(section, condition):
#                 nonlocal html
#                 if condition:
#                     html = html.replace(f"{{{{if_{section}}}}}", "").replace(
#                         f"{{{{endif_{section}}}}}", ""
#                     )
#                 else:
#                     html = re.sub(
#                         rf"{{{{if_{section}}}}}.*?{{{{endif_{section}}}}}",
#                         "",
#                         html,
#                         flags=re.DOTALL,
#                     )
#
#             toggle("rating", row.get("rating"))
#             toggle("about", row.get("about_business"))
#
#             services_html = self.render_services(row.get("services"))
#             toggle("services", services_html)
#             html = html.replace("{{services_list}}", services_html)
#
#             reviews_html = self.render_reviews(row)
#             toggle("reviews", reviews_html)
#             html = html.replace("{{reviews_list}}", reviews_html)
#
#             hours_html = self.render_hours(row.get("opening_hours"))
#             toggle("hours", hours_html)
#             html = html.replace("{{hours_list}}", hours_html)
#
#             toggle("maps_url", row.get("maps_url"))
#
#             html = re.sub(r"{{.*?}}", "", html)
#
#             filepath.write_text(html, encoding="utf-8")
#             logger.info(f"✅ Preview generated: {filepath.name}")
#
#             return filepath.name
#
#         except Exception as e:
#             logger.error(f"❌ Failed preview for '{row.get('business_name')}': {e}")
#             return None
#
#     # -------------------------
#     # Index page
#     # -------------------------
#     def generate_index(self, previews):
#         index_path = self.output_dir / "index.html"
#
#         html = f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <title>Preview Websites</title>
#   <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-100">
# <div class="container mx-auto px-6 py-12">
# <h1 class="text-4xl font-bold text-center mb-8">Generated Previews</h1>
# <p class="text-center mb-12 text-gray-600">Total: {len(previews)}</p>
#
# <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
# """
#
#         for p in previews:
#             html += f"""
# <a href="{p['filename']}" class="bg-white p-6 rounded-lg shadow hover:shadow-xl transition block">
#   <h2 class="text-xl font-bold text-purple-600">{p['business_name']}</h2>
#   <p class="text-gray-600">{p['category']}</p>
#   <p class="text-sm text-gray-500">{p['city']}</p>
# </a>
# """
#
#         html += """
# </div>
# </div>
# </body>
# </html>
# """
#
#         index_path.write_text(html, encoding="utf-8")
#         logger.info(f"✓ Index generated: {index_path}")
#
#     # -------------------------
#     # Main pipeline
#     # -------------------------
#     def generate_all(self, input_csv, output_csv):
#         self.output_dir.mkdir(exist_ok=True)
#         self.load_template()
#
#         df = pd.read_csv(input_csv)
#         if df.empty:
#             raise RuntimeError("No enriched leads found")
#
#         previews = []
#         generated = 0
#
#         for i, row in df.iterrows():
#             filename = self.generate_preview(row)
#             if filename:
#                 df.at[i, "preview_url"] = f"previews/{filename}"
#                 previews.append({
#                     "filename": filename,
#                     "business_name": row["business_name"],
#                     "category": row.get("category", ""),
#                     "city": row.get("city", "")
#                 })
#                 generated += 1
#
#         if generated == 0:
#             raise RuntimeError("0 previews generated — aborting")
#
#         self.generate_index(previews)
#         df.to_csv(output_csv, index=False, encoding="utf-8")
#
#         logger.info(f"🎉 Generated {generated}/{len(df)} previews")
#         logger.info(f"📂 Location: {self.output_dir}")
#         logger.info(f"🌐 Open: {self.output_dir / 'index.html'}")
#
#         return df
#
#
# def run_generator():
#     generator = PreviewGenerator()
#     return generator.generate_all(
#         config.ENRICHED_DATA_FILE,
#         config.ENRICHED_DATA_FILE,
#     )



"""
Phase 3: Website Preview Generation
Generate HTML preview websites from enriched leads (NO scraping here)
"""

import re
import pandas as pd
from pathlib import Path
import config
from utils import setup_logging

logger = setup_logging(config.LOG_FILE)

# Absolute project paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
PREVIEWS_DIR = BASE_DIR / "previews"


# -------------------------
# Helpers
# -------------------------
def clean_value(value):
    """Normalize CSV values: N/A, <null>, NaN → None"""
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    if isinstance(value, str):
        v = value.strip()
        if v.lower() in {"n/a", "<null>", "null", ""}:
            return None
        return v
    return value


def safe_int(value, default=0):
    try:
        if value is None:
            return default
        return int(float(value))
    except Exception:
        return default


def safe_float(value, default=None):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


class PreviewGenerator:
    def __init__(self):
        self.template_path = TEMPLATES_DIR / "dental_preview.html"
        self.output_dir = PREVIEWS_DIR
        self.template_content = None

    # -------------------------
    # Utilities
    # -------------------------
    def load_template(self):
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        self.template_content = self.template_path.read_text(encoding="utf-8")
        logger.info(f"✓ Template loaded: {self.template_path}")

    def slugify(self, text):
        text = clean_value(text) or "business"
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")[:50]

    # -------------------------
    # Render helpers
    # -------------------------
    def render_services(self, services_text):
        services_text = clean_value(services_text)
        if not services_text:
            return ""

        html = ""
        for service in services_text.split(";"):
            service = service.strip()
            if service:
                html += f"""
                <div class="bg-white p-6 rounded-xl card-shadow">
                    <h3 class="font-semibold text-lg">{service}</h3>
                </div>
                """
        return html

    def render_reviews(self, row):
        html = ""

        for i in range(1, config.MAX_REVIEWS_TO_SCRAPE + 1):
            text = clean_value(row.get(f"review_{i}_text"))
            if not text:
                continue

            name = clean_value(row.get(f"review_{i}_name")) or "Anonymous"
            rating = safe_int(row.get(f"review_{i}_rating"), default=5)

            stars_html = '<i class="fas fa-star text-yellow-400"></i>' * rating

            html += f"""
            <div class="bg-gray-50 p-6 rounded-xl card-shadow">
                <div class="flex gap-1 mb-3">{stars_html}</div>
                <p class="italic text-gray-700 mb-4">"{text}"</p>
                <p class="font-semibold text-gray-800">- {name}</p>
            </div>
            """

        return html

    def render_hours(self, hours_text):
        hours_text = clean_value(hours_text)
        if not hours_text:
            return ""

        html = ""
        for entry in hours_text.split(";"):
            entry = entry.strip()
            if ":" in entry:
                day, time = entry.split(":", 1)
                html += f"""
                <div class="flex justify-between py-3 border-b last:border-0">
                    <span class="font-semibold">{day.strip()}</span>
                    <span class="text-gray-600">{time.strip()}</span>
                </div>
                """
        return html

    # -------------------------
    # Preview generation
    # -------------------------
    def generate_preview(self, row):
        try:
            business_name = clean_value(row.get("business_name"))
            if not business_name:
                raise ValueError("Missing business_name")

            slug = self.slugify(business_name)
            filepath = self.output_dir / f"{slug}.html"

            html = self.template_content

            replacements = {
                "{{business_name}}": business_name,
                "{{category}}": clean_value(row.get("category")) or "",
                "{{city}}": clean_value(row.get("city")) or "",
                "{{address}}": clean_value(row.get("address")) or "",
                "{{phone}}": clean_value(row.get("phone")) or "",
                "{{rating}}": safe_float(row.get("rating"), "") or "",
                "{{review_count}}": safe_int(row.get("review_count"), 0),
                "{{maps_url}}": clean_value(row.get("maps_url")) or "#",
                "{{about_business}}": clean_value(row.get("about_business")) or "",
            }

            for key, value in replacements.items():
                html = html.replace(key, str(value))

            # Conditional sections
            def toggle(section, condition):
                nonlocal html
                if condition:
                    html = html.replace(f"{{{{if_{section}}}}}", "").replace(
                        f"{{{{endif_{section}}}}}", ""
                    )
                else:
                    html = re.sub(
                        rf"{{{{if_{section}}}}}.*?{{{{endif_{section}}}}}",
                        "",
                        html,
                        flags=re.DOTALL,
                    )

            toggle("rating", replacements["{{rating}}"])
            toggle("about", replacements["{{about_business}}"])

            services_html = self.render_services(row.get("services"))
            toggle("services", services_html)
            html = html.replace("{{services_list}}", services_html)

            reviews_html = self.render_reviews(row)
            toggle("reviews", reviews_html)
            html = html.replace("{{reviews_list}}", reviews_html)

            hours_html = self.render_hours(row.get("opening_hours"))
            toggle("hours", hours_html)
            html = html.replace("{{hours_list}}", hours_html)

            toggle("maps_url", replacements["{{maps_url}}"] != "#")

            # Remove unused placeholders
            html = re.sub(r"{{.*?}}", "", html)

            filepath.write_text(html, encoding="utf-8")
            logger.info(f"✅ Preview generated: {filepath.name}")
            return filepath.name

        except Exception as e:
            logger.error(f"❌ Failed preview for '{row.get('business_name')}': {e}")
            return None

    # -------------------------
    # Index page
    # -------------------------
    def generate_index(self, previews):
        index_path = self.output_dir / "index.html"

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Preview Websites</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
<div class="container mx-auto px-6 py-12">
<h1 class="text-4xl font-bold text-center mb-8">Generated Previews</h1>
<p class="text-center mb-12 text-gray-600">Total: {len(previews)}</p>

<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
"""

        for p in previews:
            html += f"""
<a href="{p['filename']}" class="bg-white p-6 rounded-lg shadow hover:shadow-xl transition block">
  <h2 class="text-xl font-bold text-purple-600">{p['business_name']}</h2>
  <p class="text-gray-600">{p['category']}</p>
  <p class="text-sm text-gray-500">{p['city']}</p>
</a>
"""

        html += """
</div>
</div>
</body>
</html>
"""

        index_path.write_text(html, encoding="utf-8")
        logger.info(f"✓ Index generated: {index_path}")

    # -------------------------
    # Main pipeline
    # -------------------------
    def generate_all(self, input_csv, output_csv):
        self.output_dir.mkdir(exist_ok=True)
        self.load_template()

        df = pd.read_csv(input_csv)
        if df.empty:
            raise RuntimeError("No enriched leads found")

        previews = []
        generated = 0

        for i, row in df.iterrows():
            filename = self.generate_preview(row)
            if filename:
                df.at[i, "preview_url"] = f"previews/{filename}"
                previews.append({
                    "filename": filename,
                    "business_name": clean_value(row.get("business_name")) or "",
                    "category": clean_value(row.get("category")) or "",
                    "city": clean_value(row.get("city")) or ""
                })
                generated += 1

        if generated == 0:
            raise RuntimeError("0 previews generated — aborting")

        self.generate_index(previews)
        df.to_csv(output_csv, index=False, encoding="utf-8")

        logger.info(f"🎉 Generated {generated}/{len(df)} previews")
        logger.info(f"📂 Location: {self.output_dir}")
        logger.info(f"🌐 Open: {self.output_dir / 'index.html'}")

        return df


def run_generator():
    generator = PreviewGenerator()
    return generator.generate_all(
        config.ENRICHED_DATA_FILE,
        config.ENRICHED_DATA_FILE,
    )
