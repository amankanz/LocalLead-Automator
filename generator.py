# locallead/LocalLead Automator/generator.py

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
