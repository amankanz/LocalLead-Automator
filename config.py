# LocalLead Automator/config.py
# settings, search parameters

"""
Configuration settings for the scraper
"""

# Search Parameters
SEARCH_QUERY = "dental clinics"
SEARCH_LOCATION = "KAMPALA, Uganda"  # Change this for different cities
MAX_RESULTS = 10  # How many businesses to scrape per run

# CSV File Paths
RAW_DATA_FILE = "data/leads_raw.csv"
QUALIFIED_DATA_FILE = "data/leads_qualified.csv"
LOG_FILE = "logs/scraper.log"

# Scraping Settings
# HEADLESS_MODE = True  # Set to False to see browser window
HEADLESS_MODE = False  # Set to True to hide browser window
SCROLL_PAUSE_TIME = 2  # seconds between scrolls
# PAGE_LOAD_WAIT = 3     # seconds to wait for page load
PAGE_LOAD_WAIT = 4     # seconds to wait for page load
ELEMENT_WAIT = 10      # seconds to wait for elements to load

# Filtering Criteria
# MIN_RATING = 3.0       # Minimum Google rating to keep
MIN_RATING = 2.5       # Minimum Google rating to keep (lowered)
# MIN_REVIEWS = 5        # Minimum number of reviews
MIN_REVIEWS = 1        # Minimum number of reviews (lowered)
# EXCLUDE_WEBSITES = True  # Only keep businesses without websites
EXCLUDE_WEBSITES = True  # Set to True to ONLY keep businesses without websites
