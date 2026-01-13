# # LocalLead Automator.py/generator.py

# """
# Phase 3: Website Preview Generation
# Generate HTML preview websites from enriched leads (NO scraping here)
# """
#
# import re
# import pandas as pd
# from pathlib import Path
# import config
# from utils import setup_logging
#
# logger = setup_logging(config.LOG_FILE)
#
# # Absolute project paths
# BASE_DIR = Path(__file__).resolve().parent
# TEMPLATES_DIR = BASE_DIR / "templates"
# PREVIEWS_DIR = BASE_DIR / "previews"
#
#
# # -------------------------
# # Helpers
# # -------------------------
# def clean_value(value):
#     """Normalize CSV values: N/A, <null>, NaN → None"""
#     if value is None:
#         return None
#     if isinstance(value, float) and pd.isna(value):
#         return None
#     if isinstance(value, str):
#         v = value.strip()
#         if v.lower() in {"n/a", "<null>", "null", ""}:
#             return None
#         return v
#     return value
#
#
# def safe_int(value, default=0):
#     try:
#         if value is None:
#             return default
#         return int(float(value))
#     except Exception:
#         return default
#
#
# def safe_float(value, default=None):
#     try:
#         if value is None:
#             return default
#         return float(value)
#     except Exception:
#         return default
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
#         self.template_content = self.template_path.read_text(encoding="utf-8")
#         logger.info(f"✓ Template loaded: {self.template_path}")
#
#     def slugify(self, text):
#         text = clean_value(text) or "business"
#         text = text.lower()
#         text = re.sub(r"[^a-z0-9]+", "-", text)
#         return text.strip("-")[:50]
#
#     # -------------------------
#     # Render helpers
#     # -------------------------
#     def render_services(self, services_text):
#         services_text = clean_value(services_text)
#         if not services_text:
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
#             text = clean_value(row.get(f"review_{i}_text"))
#             if not text:
#                 continue
#
#             name = clean_value(row.get(f"review_{i}_name")) or "Anonymous"
#             rating = safe_int(row.get(f"review_{i}_rating"), default=5)
#
#             stars_html = '<i class="fas fa-star text-yellow-400"></i>' * rating
#
#             html += f"""
#             <div class="bg-gray-50 p-6 rounded-xl card-shadow">
#                 <div class="flex gap-1 mb-3">{stars_html}</div>
#                 <p class="italic text-gray-700 mb-4">"{text}"</p>
#                 <p class="font-semibold text-gray-800">- {name}</p>
#             </div>
#             """
#
#         return html
#
#     def render_hours(self, hours_text):
#         hours_text = clean_value(hours_text)
#         if not hours_text:
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
#             business_name = clean_value(row.get("business_name"))
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
#                 "{{category}}": clean_value(row.get("category")) or "",
#                 "{{city}}": clean_value(row.get("city")) or "",
#                 "{{address}}": clean_value(row.get("address")) or "",
#                 "{{phone}}": clean_value(row.get("phone")) or "",
#                 "{{rating}}": safe_float(row.get("rating"), "") or "",
#                 "{{review_count}}": safe_int(row.get("review_count"), 0),
#                 "{{maps_url}}": clean_value(row.get("maps_url")) or "#",
#                 "{{about_business}}": clean_value(row.get("about_business")) or "",
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
#             toggle("rating", replacements["{{rating}}"])
#             toggle("about", replacements["{{about_business}}"])
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
#             toggle("maps_url", replacements["{{maps_url}}"] != "#")
#
#             # Remove unused placeholders
#             html = re.sub(r"{{.*?}}", "", html)
#
#             filepath.write_text(html, encoding="utf-8")
#             logger.info(f"✅ Preview generated: {filepath.name}")
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
#                     "business_name": clean_value(row.get("business_name")) or "",
#                     "category": clean_value(row.get("category")) or "",
#                     "city": clean_value(row.get("city")) or ""
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

###################### UP UNTOUCHED ###########

#
#
# """
# Phase 3: Data Export
# Generate JSON for frontend templates (NO HTML, NO UI)
# """
#
# import json
# import re
# import pandas as pd
# from pathlib import Path
# from datetime import datetime
# import config
# from utils import setup_logging
#
# logger = setup_logging(config.LOG_FILE)
#
# BASE_DIR = Path(__file__).resolve().parent
# OUTPUT_DIR = BASE_DIR / "output"
# OUTPUT_DIR.mkdir(exist_ok=True)
#
#
# # -------------------------
# # Helpers
# # -------------------------
# def clean_value(value):
#     if value is None:
#         return ""
#     if isinstance(value, float) and pd.isna(value):
#         return ""
#     return str(value).strip()
#
#
# def safe_int(value):
#     try:
#         if value is None or pd.isna(value):
#             return 0
#         return int(float(value))
#     except Exception:
#         return 0
#
#
# def safe_float(value):
#     try:
#         if value is None or pd.isna(value):
#             return None
#         return float(value)
#     except Exception:
#         return None
#
#
# def slugify(text):
#     text = clean_value(text).lower()
#     text = re.sub(r"[^a-z0-9]+", "-", text)
#     return text.strip("-")
#
#
# # -------------------------
# # Main generator
# # -------------------------
# def generate_businesses_json(input_csv: Path):
#     df = pd.read_csv(input_csv)
#     businesses = []
#
#     for _, row in df.iterrows():
#         business = {
#             "id": slugify(row.get("business_name")),
#             "name": clean_value(row.get("business_name")),
#             "category": clean_value(row.get("category")),
#             "city": clean_value(row.get("city")),
#             "address": clean_value(row.get("address")),
#             "phone": clean_value(row.get("phone")),
#             "email": clean_value(row.get("email")),
#             "website": clean_value(row.get("website")),
#             "rating": safe_float(row.get("rating")),
#             "review_count": safe_int(row.get("review_count")),
#             "about": clean_value(row.get("about_business")),
#             "services": [],
#             "highlights": [],
#             "opening_hours": {},
#             "location": {
#                 "maps_url": clean_value(row.get("maps_url"))
#             },
#             "reviews": []
#         }
#
#         # Reviews (up to 3)
#         for i in range(1, 4):
#             text = clean_value(row.get(f"review_{i}_text"))
#             if text:
#                 business["reviews"].append({
#                     "author": clean_value(row.get(f"review_{i}_name")) or "Anonymous",
#                     "rating": safe_int(row.get(f"review_{i}_rating")),
#                     "text": text
#                 })
#
#         businesses.append(business)
#
#     output = {
#         "generated_at": datetime.utcnow().isoformat() + "Z",
#         "count": len(businesses),
#         "businesses": businesses
#     }
#
#     out_file = OUTPUT_DIR / "businesses.json"
#     out_file.write_text(
#         json.dumps(output, indent=2, allow_nan=False),
#         encoding="utf-8"
#     )
#
#     logger.info(f"✅ businesses.json generated ({len(businesses)} businesses)")
#     return out_file
#
#
# def generate_meta_json():
#     meta = {
#         "project": "LocalLead Automator",
#         "data_version": "1.0",
#         "generated_at": datetime.utcnow().isoformat() + "Z",
#         "source_file": str(config.ENRICHED_DATA_FILE),
#         "templates": [
#             {
#                 "id": "dental-v1",
#                 "name": "Dental Clinic Template v1",
#                 "status": "active"
#             }
#         ],
#         "routing": {
#             "mode": "slug",
#             "base_path": "/preview"
#         }
#     }
#
#     out_file = OUTPUT_DIR / "meta.json"
#     out_file.write_text(
#         json.dumps(meta, indent=2, allow_nan=False),
#         encoding="utf-8"
#     )
#
#     logger.info("✅ meta.json generated")
#     return out_file
#
#
# def run_generator():
#     generate_businesses_json(Path(config.ENRICHED_DATA_FILE))
#     generate_meta_json()
#
#
#
# if __name__ == "__main__":
#     run_generator()
#
#     # Sync generated data to frontend
#     try:
#         import sync_to_frontend
#     except Exception as e:
#         logger.error(f"❌ Sync to frontend failed: {e}")
#


"""
Phase 3: Data Export
Generate JSON for frontend templates (NO HTML, NO UI)
"""

import json
import re
import pandas as pd
from pathlib import Path
from datetime import datetime

import config
from utils import setup_logging


# -------------------------
# Setup
# -------------------------
logger = setup_logging(config.LOG_FILE)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_BUSINESSES_DIR = (
    BASE_DIR.parent / "Dental Clinic Website Template" / "public" / "data" / "businesses"
)
FRONTEND_BUSINESSES_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------
# Helpers
# -------------------------
def clean_value(value) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def safe_int(value) -> int:
    try:
        if value is None or pd.isna(value):
            return 0
        return int(float(value))
    except Exception:
        return 0


def safe_float(value):
    try:
        if value is None or pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def slugify(text: str) -> str:
    text = clean_value(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


# -------------------------
# Main generator
# -------------------------
# def generate_businesses_json(input_csv: Path):
#     logger.info(f"Reading enriched CSV: {input_csv}")
#
#     df = pd.read_csv(input_csv)
#
#     businesses_index = []
#     per_business_files = []
#
#     for _, row in df.iterrows():
#         slug = slugify(row.get("business_name"))
#
#         business = {
#             "id": slug,
#             "slug": slug,
#             "name": clean_value(row.get("business_name")),
#             "category": clean_value(row.get("category")),
#             "city": clean_value(row.get("city")),
#             "address": clean_value(row.get("address")),
#             "phone": clean_value(row.get("phone")),
#             "email": clean_value(row.get("email")),
#             "website": clean_value(row.get("website")),
#             "rating": safe_float(row.get("rating")),
#             "review_count": safe_int(row.get("review_count")),
#             "about": clean_value(row.get("about_business")),
#             "preview": f"Trusted {clean_value(row.get('category'))} in {clean_value(row.get('city'))}",
#             "cta": {
#                 "type": "whatsapp",
#                 "label": "Contact Business"
#             },
#             "location": {
#                 "maps_url": clean_value(row.get("maps_url"))
#             },
#             "reviews": []
#         }
#
#         # Reviews (up to 3)
#         for i in range(1, 4):
#             text = clean_value(row.get(f"review_{i}_text"))
#             if text:
#                 business["reviews"].append({
#                     "author": clean_value(row.get(f"review_{i}_name")) or "Anonymous",
#                     "rating": safe_int(row.get(f"review_{i}_rating")),
#                     "text": text
#                 })
#
#         # -------------------------
#         # Write per-business JSON
#         # -------------------------
#         business_file = FRONTEND_BUSINESSES_DIR / f"{slug}.json"
#         business_file.write_text(
#             json.dumps(business, indent=2, allow_nan=False),
#             encoding="utf-8"
#         )
#
#         businesses_index.append(business)
#         per_business_files.append(business_file.name)
#
#     # -------------------------
#     # Master index JSON
#     # -------------------------
#     index_output = {
#         "generated_at": datetime.utcnow().isoformat() + "Z",
#         "count": len(businesses_index),
#         "businesses": businesses_index
#     }
#
#     index_file = OUTPUT_DIR / "businesses.json"
#     index_file.write_text(
#         json.dumps(index_output, indent=2, allow_nan=False),
#         encoding="utf-8"
#     )
#
#     logger.info(f"✅ businesses.json generated ({len(businesses_index)} businesses)")
#     logger.info(f"✅ {len(per_business_files)} per-business JSON files created")
#
#     return index_file

def generate_businesses_json(input_csv: Path):
    logger.info(f"Reading enriched CSV: {input_csv}")

    df = pd.read_csv(input_csv)

    # This will become public/data/businesses/index.json
    dashboard_index = []

    for _, row in df.iterrows():
        slug = slugify(row.get("business_name"))

        business = {
            "id": slug,
            "slug": slug,
            "name": clean_value(row.get("business_name")),
            "category": clean_value(row.get("category")),
            "city": clean_value(row.get("city")),
            "address": clean_value(row.get("address")),
            "phone": clean_value(row.get("phone")),
            "email": clean_value(row.get("email")),
            "website": clean_value(row.get("website")),
            "rating": safe_float(row.get("rating")),
            "review_count": safe_int(row.get("review_count")),
            "about": clean_value(row.get("about_business")),
            "preview": f"Trusted {clean_value(row.get('category'))} in {clean_value(row.get('city'))}",
            "cta": {
                "type": "whatsapp",
                "label": "Contact Business"
            },
            "location": {
                "maps_url": clean_value(row.get("maps_url"))
            },
            "reviews": []
        }

        # -------------------------
        # Reviews (up to 3)
        # -------------------------
        for i in range(1, 4):
            text = clean_value(row.get(f"review_{i}_text"))
            if text:
                business["reviews"].append({
                    "author": clean_value(row.get(f"review_{i}_name")) or "Anonymous",
                    "rating": safe_int(row.get(f"review_{i}_rating")),
                    "text": text
                })

        # -------------------------
        # Write per-business JSON
        # -------------------------
        business_file = FRONTEND_BUSINESSES_DIR / f"{slug}.json"
        business_file.write_text(
            json.dumps(business, indent=2, allow_nan=False),
            encoding="utf-8"
        )

        # -------------------------
        # Add lightweight entry to dashboard index
        # -------------------------
        dashboard_index.append({
            "slug": business["slug"],
            "name": business["name"],
            "category": business["category"],
            "city": business["city"],
            "rating": business["rating"],
            "review_count": business["review_count"],
            "preview": business["preview"]
        })

    # -------------------------
    # Write FRONTEND index.json
    # -------------------------
    index_output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(dashboard_index),
        "businesses": dashboard_index
    }

    index_file = FRONTEND_BUSINESSES_DIR / "index.json"
    index_file.write_text(
        json.dumps(index_output, indent=2, allow_nan=False),
        encoding="utf-8"
    )

    logger.info(f"✅ {len(dashboard_index)} businesses generated")
    logger.info("✅ public/data/businesses/index.json created")

    return index_file



def generate_meta_json():
    meta = {
        "project": "LocalLead Automator",
        "data_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_file": str(config.ENRICHED_DATA_FILE),
        "routing": {
            "mode": "slug",
            "base_path": "/preview"
        }
    }

    out_file = OUTPUT_DIR / "meta.json"
    out_file.write_text(
        json.dumps(meta, indent=2, allow_nan=False),
        encoding="utf-8"
    )

    logger.info("✅ meta.json generated")
    return out_file


def run_generator():
    generate_businesses_json(Path(config.ENRICHED_DATA_FILE))
    generate_meta_json()


if __name__ == "__main__":
    run_generator()
