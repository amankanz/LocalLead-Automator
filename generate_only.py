# # LocalLead Automator/generate_only.py
#
# from generator import run_generator
# from utils import setup_logging
# import config
#
# logger = setup_logging(config.LOG_FILE)
#
# if __name__ == "__main__":
#     logger.info("Generating preview websites...")
#     run_generator()
#     logger.info("Done! Open previews/index.html")


# LocalLead Automator/generate_only.py

# from generator import run_generator
# from utils import setup_logging
# import config
#
# logger = setup_logging(config.LOG_FILE)
#
# if __name__ == "__main__":
#     logger.info("Generating preview websites...")
#     run_generator()
#     logger.info("Done! Open previews/index.html")

"""
Phase 4 only: Generate preview websites from existing enriched data.
NO scraping. NO enrichment.
"""

from generator import run_generator
from utils import setup_logging
import config

logger = setup_logging(config.LOG_FILE)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("PHASE 4 ONLY: GENERATING PREVIEW WEBSITES")
    logger.info("=" * 60)

    run_generator()

    logger.info("✅ Done!")
    logger.info("🌐 Open previews/index.html")

