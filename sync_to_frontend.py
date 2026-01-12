# locallead/LocalLead-Automator/sync_to_frontend.py

from pathlib import Path
import shutil

# Resolve project root (locallead/)
ROOT_DIR = Path(__file__).resolve().parents[1]

BACKEND_FILE = (
    ROOT_DIR
    / "LocalLead Automator"
    / "output"
    / "businesses.json"
)

FRONTEND_FILE = (
    ROOT_DIR
    / "Dental Clinic Website Template"
    / "public"
    / "data"
    / "businesses.json"
)

# Ensure target directory exists
FRONTEND_FILE.parent.mkdir(parents=True, exist_ok=True)

if not BACKEND_FILE.exists():
    raise FileNotFoundError(
        f"Backend file not found: {BACKEND_FILE}"
    )

shutil.copyfile(BACKEND_FILE, FRONTEND_FILE)

print("✅ businesses.json copied to frontend successfully")
