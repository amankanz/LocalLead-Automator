# # locallead/LocalLead Automator/main.py
#
# """
# Main entry point - run the complete pipeline
# Phase 1: Scrape → Phase 2: Filter → Phase 3: Enrich → Phase 4: Generate Previews
# """
# import sys
# from utils import ensure_directories, setup_logging
# import config
# from scraper import run_scraper
# from filter import run_filter
# from enricher import run_enricher
# from generator import run_generator
#
# logger = setup_logging(config.LOG_FILE)
#
#
# def main():
#     """Run the complete data collection pipeline"""
#     logger.info("=" * 60)
#     logger.info("DENTAL CLINIC LEAD GENERATOR - STARTING")
#     logger.info("=" * 60)
#
#     try:
#         ensure_directories()
#
#         # Phase 1: Scrape Google Maps
#         logger.info("\n" + "=" * 60)
#         logger.info("PHASE 1: SCRAPING GOOGLE MAPS")
#         logger.info("=" * 60)
#         df_raw = run_scraper()
#
#         if df_raw is None or len(df_raw) == 0:
#             logger.error("No data scraped. Exiting.")
#             return
#
#         # Phase 2: Filter and clean
#         logger.info("\n" + "=" * 60)
#         logger.info("PHASE 2: FILTERING QUALIFIED LEADS")
#         logger.info("=" * 60)
#         df_qualified = run_filter()
#
#         if df_qualified is None or len(df_qualified) == 0:
#             logger.error("No qualified leads. Exiting.")
#             return
#
#         # Phase 3: Enrich with Maps data
#         logger.info("\n" + "=" * 60)
#         logger.info("PHASE 3: ENRICHING LEADS WITH MAPS DATA")
#         logger.info("=" * 60)
#         df_enriched = run_enricher()
#
#         if df_enriched is None or len(df_enriched) == 0:
#             logger.error("No enriched leads. Exiting.")
#             return
#
#         # Phase 4: Generate Preview Websites
#         logger.info("\n" + "=" * 60)
#         logger.info("PHASE 4: GENERATING PREVIEW WEBSITES")
#         logger.info("=" * 60)
#         df_final = run_generator()
#
#         logger.info("\n" + "=" * 60)
#         logger.info("✅ COMPLETE PIPELINE FINISHED!")
#         logger.info("=" * 60)
#         logger.info(f"📊 Results:")
#         logger.info(f"   - Scraped: {len(df_raw)} businesses")
#         logger.info(f"   - Qualified: {len(df_qualified)} businesses")
#         logger.info(f"   - Enriched: {len(df_enriched)} businesses")
#         logger.info(f"   - Previews: {len(df_final)} websites")
#         logger.info(f"\n📁 Files:")
#         logger.info(f"   - Raw data: {config.RAW_DATA_FILE}")
#         logger.info(f"   - Qualified: {config.QUALIFIED_DATA_FILE}")
#         logger.info(f"   - Enriched: {config.ENRICHED_DATA_FILE}")
#         logger.info(f"   - Previews: previews/index.html")
#         logger.info("=" * 60)
#         logger.info("\n🌐 Open 'previews/index.html' in your browser to see all preview websites!")
#
#     except KeyboardInterrupt:
#         logger.info("\nProcess interrupted by user")
#         sys.exit(0)
#     except Exception as e:
#         logger.error(f"Pipeline failed: {e}")
#         import traceback
#         traceback.print_exc()
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     main()
#


# locallead/LocalLead Automator/main.py

"""
Main entry point - run the complete pipeline
Phase 1: Scrape → Phase 2: Filter → Phase 3: Enrich → Phase 4: Generate Previews
"""
import sys
from utils import ensure_directories, setup_logging
import config
from scraper import run_scraper
from filter import run_filter
from enricher import run_enricher
from generator import run_generator
from config import set_runtime_config
import time

logger = setup_logging(config.LOG_FILE)


def main():
    """Run the complete data collection pipeline"""
    logger.info("=" * 60)
    logger.info("DENTAL CLINIC LEAD GENERATOR - STARTING")
    logger.info("=" * 60)

    try:
        ensure_directories()

        # Phase 1: Scrape Google Maps
        logger.info("\n" + "=" * 60)
        logger.info("PHASE 1: SCRAPING GOOGLE MAPS")
        logger.info("=" * 60)
        df_raw = run_scraper()

        if df_raw is None or len(df_raw) == 0:
            logger.error("No data scraped. Exiting.")
            return

        # Phase 2: Filter and clean
        logger.info("\n" + "=" * 60)
        logger.info("PHASE 2: FILTERING QUALIFIED LEADS")
        logger.info("=" * 60)
        df_qualified = run_filter()

        if df_qualified is None or len(df_qualified) == 0:
            logger.error("No qualified leads. Exiting.")
            return

        # Phase 3: Enrich with Maps data
        logger.info("\n" + "=" * 60)
        logger.info("PHASE 3: ENRICHING LEADS WITH MAPS DATA")
        logger.info("=" * 60)
        df_enriched = run_enricher()

        if df_enriched is None or len(df_enriched) == 0:
            logger.error("No enriched leads. Exiting.")
            return

        # Phase 4: Generate Preview Websites
        logger.info("\n" + "=" * 60)
        logger.info("PHASE 4: GENERATING PREVIEW WEBSITES")
        logger.info("=" * 60)
        df_final = run_generator()

        logger.info("\n" + "=" * 60)
        logger.info("✅ COMPLETE PIPELINE FINISHED!")
        logger.info("=" * 60)
        logger.info(f"📊 Results:")
        logger.info(f"   - Scraped: {len(df_raw)} businesses")
        logger.info(f"   - Qualified: {len(df_qualified)} businesses")
        logger.info(f"   - Enriched: {len(df_enriched)} businesses")
        logger.info(f"   - Previews: {len(df_final)} websites")
        logger.info(f"\n📁 Files:")
        logger.info(f"   - Raw data: {config.RAW_DATA_FILE}")
        logger.info(f"   - Qualified: {config.QUALIFIED_DATA_FILE}")
        logger.info(f"   - Enriched: {config.ENRICHED_DATA_FILE}")
        logger.info(f"   - Previews: previews/index.html")
        logger.info("=" * 60)
        logger.info("\n🌐 Open 'previews/index.html' in your browser to see all preview websites!")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# def run_pipeline(query, location, max_results, progress_cb=None):
#     set_runtime_config(query, location, max_results)
#
#     def update(status):
#         if progress_cb:
#             progress_cb(status)
#
#     update("SCRAPING")
#     df_raw = run_scraper()
#
#     update("FILTERING")
#     df_qualified = run_filter()
#
#     update("ENRICHING")
#     df_enriched = run_enricher()
#
#     update("GENERATING")
#     df_final = run_generator()
#
#     update("DONE")
#
#     return {
#         "scraped": len(df_raw),
#         "qualified": len(df_qualified),
#         "enriched": len(df_enriched),
#         "previews": len(df_final),
#     }

def run_pipeline(query, location, max_results, progress_cb=None):
    set_runtime_config(query, location, max_results)

    def update(status):
        if progress_cb:
            progress_cb(status)

    update("SCRAPING")
    df_raw = run_scraper()

    update("FILTERING")
    df_qualified = run_filter()

    update("ENRICHING")
    df_enriched = run_enricher()

    update("GENERATING")
    df_final = run_generator()

    update("DONE")

    # ---- SAFE COUNTS ----
    scraped = len(df_raw) if df_raw is not None else 0
    qualified = len(df_qualified) if df_qualified is not None else 0
    enriched = len(df_enriched) if df_enriched is not None else 0

    # Preview count from disk (authoritative)
    previews = 0
    try:
        import json
        from pathlib import Path

        index_path = Path("public/data/businesses/index.json")
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                previews = len(json.load(f))
    except Exception:
        previews = 0

    return {
        "scraped": scraped,
        "qualified": qualified,
        "enriched": enriched,
        "previews": previews,
    }


if __name__ == "__main__":
    main()




