# LocalLead Automator/main.py
# main entry point

# """
# Main entry point - run the complete pipeline
# """
# import sys
# from utils import ensure_directories, setup_logging
# import config
# from scraper import run_scraper
# from filter import run_filter
#
# logger = setup_logging(config.LOG_FILE)
#
#
# def main():
#     """Run the complete data collection pipeline"""
#     logger.info("=" * 50)
#     logger.info("DENTAL CLINIC LEAD GENERATOR - STARTING")
#     logger.info("=" * 50)
#
#     try:
#         # Ensure directories exist
#         ensure_directories()
#
#         # Phase 1: Scrape Google Maps
#         logger.info("\n--- PHASE 1: SCRAPING ---")
#         df_raw = run_scraper()
#
#         if df_raw is None or len(df_raw) == 0:
#             logger.error("No data scraped. Exiting.")
#             return
#
#         # Phase 2: Filter and clean
#         logger.info("\n--- PHASE 2: FILTERING ---")
#         df_qualified = run_filter()
#
#         logger.info("\n" + "=" * 50)
#         logger.info("PIPELINE COMPLETE!")
#         logger.info(f"Qualified leads ready: {len(df_qualified)}")
#         logger.info(f"Check: {config.QUALIFIED_DATA_FILE}")
#         logger.info("=" * 50)
#
#     except KeyboardInterrupt:
#         logger.info("\nProcess interrupted by user")
#         sys.exit(0)
#     except Exception as e:
#         logger.error(f"Pipeline failed: {e}")
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     main()


"""
Main entry point - run the complete pipeline
"""
import sys
from utils import ensure_directories, setup_logging
import config
from scraper import run_scraper
from filter import run_filter

logger = setup_logging(config.LOG_FILE)


def main():
    """Run the complete data collection pipeline"""
    logger.info("=" * 50)
    logger.info("DENTAL CLINIC LEAD GENERATOR - STARTING")
    logger.info("=" * 50)

    try:
        # Ensure directories exist
        ensure_directories()

        # Phase 1: Scrape Google Maps
        logger.info("\n--- PHASE 1: SCRAPING ---")
        df_raw = run_scraper()

        if df_raw is None or len(df_raw) == 0:
            logger.error("No data scraped. Exiting.")
            return

        # Phase 2: Filter and clean
        logger.info("\n--- PHASE 2: FILTERING ---")
        df_qualified = run_filter()

        logger.info("\n" + "=" * 50)
        logger.info("PIPELINE COMPLETE!")
        logger.info(f"Qualified leads ready: {len(df_qualified)}")
        logger.info(f"Check: {config.QUALIFIED_DATA_FILE}")
        logger.info("=" * 50)

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

