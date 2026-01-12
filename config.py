# # locallead/LocalLead Automator/config.py
# """
# Configuration settings for the scraper
# """
#
# # Search Parameters
# SEARCH_QUERY = "dental clinics"
# SEARCH_LOCATION = "Kampala, Uganda"
# MAX_RESULTS = 10  # How many businesses to scrape per run
#
# # CSV File Paths
# RAW_DATA_FILE = "data/leads_raw.csv"
# QUALIFIED_DATA_FILE = "data/leads_qualified.csv"
# ENRICHED_DATA_FILE = "data/leads_enriched.csv"  # NEW: Phase 2 output
# LOG_FILE = "logs/scraper.log"
#
# # Scraping Settings
# HEADLESS_MODE = False  # Set to True to hide browser window
# SCROLL_PAUSE_TIME = 2  # seconds between scrolls
# PAGE_LOAD_WAIT = 4     # seconds to wait for page load
# ELEMENT_WAIT = 10      # seconds to wait for elements to load
#
# # Phase 2: Enrichment Settings
# ENRICHMENT_DELAY = 3   # seconds to wait on each Maps page
# MAX_REVIEWS_TO_SCRAPE = 3  # number of reviews to collect per business
#
# # Phase 3: Preview Generation Settings
# PREVIEW_OUTPUT_DIR = "previews"
#
# # Filtering Criteria
# MIN_RATING = 2.5       # Minimum Google rating to keep
# MIN_REVIEWS = 0        # Minimum number of reviews (0 = accept all)
# ONLY_NO_WEBSITE = True  # TRUE = Keep ONLY businesses WITHOUT websites


# locallead/LocalLead Automator/config.py
"""
Configuration settings for the scraper
"""
from pathlib import Path

# Base directory (LocalLead Automator/)
BASE_DIR = Path(__file__).resolve().parent

# Search Parameters
SEARCH_QUERY = "dental clinics"
SEARCH_LOCATION = "Kampala, Uganda"
MAX_RESULTS = 10  # How many businesses to scrape per run

# CSV File Paths
RAW_DATA_FILE = BASE_DIR / "data" / "leads_raw.csv"
QUALIFIED_DATA_FILE = BASE_DIR / "data" / "leads_qualified.csv"
ENRICHED_DATA_FILE = BASE_DIR / "data" / "leads_enriched.csv"  # NEW: Phase 2 output
LOG_FILE = BASE_DIR / "logs" / "scraper.log"

# Scraping Settings
HEADLESS_MODE = False  # Set to True to hide browser window
SCROLL_PAUSE_TIME = 2  # seconds between scrolls
PAGE_LOAD_WAIT = 4     # seconds to wait for page load
ELEMENT_WAIT = 10      # seconds to wait for elements to load

# Phase 2: Enrichment Settings
ENRICHMENT_DELAY = 3   # seconds to wait on each Maps page
MAX_REVIEWS_TO_SCRAPE = 3  # number of reviews to collect per business

# Phase 3: Preview Generation Settings
PREVIEW_OUTPUT_DIR = "previews"

# Filtering Criteria
MIN_RATING = 2.5       # Minimum Google rating to keep
MIN_REVIEWS = 0        # Minimum number of reviews (0 = accept all)
ONLY_NO_WEBSITE = True  # TRUE = Keep ONLY businesses WITHOUT websites

