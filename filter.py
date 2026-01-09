# LocalLead Automator/filter.py
# filter and clean data

# """
# Filter and clean the scraped data
# """
# import pandas as pd
# import config
# from utils import setup_logging, validate_email
#
# logger = setup_logging(config.LOG_FILE)
#
#
# def filter_leads(input_file, output_file):
#     """Filter leads based on criteria - ONLY businesses with NO website + contact info"""
#     logger.info(f"Loading data from {input_file}...")
#
#     try:
#         df = pd.read_csv(input_file)
#         logger.info(f"Loaded {len(df)} businesses")
#
#         original_count = len(df)
#
#         # Show what we have before filtering
#         logger.info("\n=== BEFORE FILTERING ===")
#         logger.info(f"Businesses with websites: {len(df[df['website'] != 'N/A'])}")
#         logger.info(f"Businesses WITHOUT websites: {len(df[df['website'] == 'N/A'])}")
#         logger.info(f"Businesses with phone: {len(df[df['phone'] != 'N/A'])}")
#         logger.info(f"Businesses with email: {len(df[df['email'] != 'N/A'])}")
#
#         # CRITICAL FILTER 1: Keep ONLY businesses WITHOUT websites
#         before_website = len(df)
#         if config.ONLY_NO_WEBSITE:
#             df = df[df['website'] == 'N/A']
#             logger.info(
#                 f"✓ After NO WEBSITE filter: {len(df)} businesses (removed {before_website - len(df)} with websites)")
#         else:
#             logger.info(f"Website filter disabled - keeping all: {len(df)} businesses")
#
#         # CRITICAL FILTER 2: Must have phone OR email (or both)
#         before_contact = len(df)
#         df = df[(df['phone'] != 'N/A') | (df['email'] != 'N/A')]
#         logger.info(
#             f"✓ After CONTACT filter (phone OR email required): {len(df)} businesses (removed {before_contact - len(df)} without contact)")
#
#         # FILTER 3: Minimum rating (convert to numeric, keep if no rating)
#         before_rating = len(df)
#         df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
#         df = df[(df['rating'] >= config.MIN_RATING) | (df['rating'].isna())]
#         logger.info(
#             f"✓ After RATING filter (>= {config.MIN_RATING}): {len(df)} businesses (removed {before_rating - len(df)} low rated)")
#
#         # FILTER 4: Minimum reviews (optional - set to 0 to skip)
#         if config.MIN_REVIEWS > 0:
#             before_reviews = len(df)
#             df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
#             df = df[(df['review_count'] >= config.MIN_REVIEWS) | (df['review_count'].isna())]
#             logger.info(
#                 f"✓ After REVIEW filter (>= {config.MIN_REVIEWS} reviews): {len(df)} businesses (removed {before_reviews - len(df)})")
#         else:
#             logger.info(f"✓ Review filter skipped (MIN_REVIEWS = 0)")
#
#         # Remove duplicates by phone
#         before_dedup = len(df)
#         df = df.drop_duplicates(subset=['phone'], keep='first')
#         if before_dedup > len(df):
#             logger.info(f"✓ Removed {before_dedup - len(df)} duplicate phone numbers")
#
#         # Add status columns for tracking
#         df['status'] = 'new'
#         df['notes'] = ''
#         df['email_sent_date'] = ''
#         df['preview_url'] = ''
#
#         # Save filtered data
#         df.to_csv(output_file, index=False, encoding='utf-8')
#         logger.info(f"\n✓ Filtered data saved to {output_file}")
#         logger.info(f"📊 SUMMARY: {original_count} scraped -> {len(df)} QUALIFIED LEADS")
#
#         # Show qualified leads
#         if len(df) > 0:
#             logger.info("\n=== ✅ QUALIFIED LEADS (NO WEBSITE + HAS CONTACT) ===")
#             for idx, row in df.iterrows():
#                 contact = f"Phone: {row['phone']}" if row['phone'] != 'N/A' else f"Email: {row['email']}"
#                 logger.info(f"{idx + 1}. {row['business_name']} | {contact} | Rating: {row['rating']}")
#         else:
#             logger.warning("\n⚠️  NO QUALIFIED LEADS FOUND!")
#             logger.warning("Try: Lower MIN_RATING or increase MAX_RESULTS in config.py")
#
#         return df
#
#     except Exception as e:
#         logger.error(f"Filtering failed: {e}")
#         raise
#
#
# def run_filter():
#     """Main function to run filter"""
#     df = filter_leads(config.RAW_DATA_FILE, config.QUALIFIED_DATA_FILE)
#     return df


"""
Filter and clean the scraped data
"""
import pandas as pd
import config
from utils import setup_logging, validate_email
from utils import has_valid_website

logger = setup_logging(config.LOG_FILE)


def filter_leads(input_file, output_file):
    """Filter leads based on criteria - ONLY businesses with NO website + contact info"""
    logger.info(f"Loading data from {input_file}...")

    try:
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} businesses")

        # Normalize website column (IMPORTANT)
        # df['website'] = df['website'].fillna('N/A').astype(str).str.strip()
        def normalize_website_column(df):
            df['website'] = df['website'].fillna('N/A').astype(str).str.strip()
            return df

        original_count = len(df)

        # Show what we have before filtering
        logger.info("\n=== BEFORE FILTERING ===")
        logger.info(f"Total businesses: {len(df)}")
        with_website = df['website'].apply(has_valid_website).sum()
        without_website = len(df) - with_website

        logger.info(f"Businesses WITH websites: {with_website}")
        logger.info(f"Businesses WITHOUT websites: {without_website}")
        # logger.info(f"Businesses WITH websites: {len(df[df['website'] != 'N/A'])}")
        # logger.info(f"Businesses WITHOUT websites: {len(df[df['website'] == 'N/A'])}")
        logger.info(f"Businesses with phone: {len(df[df['phone'] != 'N/A'])}")
        logger.info(f"Businesses with email: {len(df[df['email'] != 'N/A'])}")

        # Show the ones without websites in detail
        no_website = df[df['website'] == 'N/A']
        if len(no_website) > 0:
            logger.info(f"\n📋 Businesses WITHOUT websites ({len(no_website)} found):")
            for idx, row in no_website.iterrows():
                logger.info(f"  - {row['business_name']} | Phone: {row['phone']} | Rating: {row['rating']}")

        # CRITICAL FILTER 1: Keep ONLY businesses WITHOUT websites
        before_website = len(df)
        if config.ONLY_NO_WEBSITE:
            # df = df[df['website'] == 'N/A']
            df = df[~df['website'].apply(has_valid_website)]
            logger.info(
                f"\n✓ After NO WEBSITE filter: {len(df)} businesses (removed {before_website - len(df)} with websites)")
        else:
            logger.info(f"\nWebsite filter disabled - keeping all: {len(df)} businesses")

        # Show what's left after website filter
        if len(df) == 0:
            logger.error("❌ NO BUSINESSES LEFT after website filter! All had websites.")
            df.to_csv(output_file, index=False, encoding='utf-8')
            return df

        # CRITICAL FILTER 2: Must have phone OR email (or both)
        before_contact = len(df)
        logger.info(f"\n📞 Checking contact info...")
        logger.info(f"  Businesses with phone: {len(df[df['phone'] != 'N/A'])}")
        logger.info(f"  Businesses with email: {len(df[df['email'] != 'N/A'])}")

        df = df[(df['phone'] != 'N/A') | (df['email'] != 'N/A')]
        logger.info(
            f"✓ After CONTACT filter: {len(df)} businesses (removed {before_contact - len(df)} without contact)")

        if len(df) == 0:
            logger.error("❌ NO BUSINESSES LEFT after contact filter! None had phone or email.")
            df.to_csv(output_file, index=False, encoding='utf-8')
            return df

        # FILTER 3: Minimum rating (convert to numeric, keep if no rating)
        before_rating = len(df)
        logger.info(f"\n⭐ Checking ratings (minimum: {config.MIN_RATING})...")
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # Show ratings before filtering
        for idx, row in df.iterrows():
            logger.info(f"  - {row['business_name']} | Rating: {row['rating']}")

        df = df[(df['rating'] >= config.MIN_RATING) | (df['rating'].isna())]
        logger.info(f"✓ After RATING filter: {len(df)} businesses (removed {before_rating - len(df)} with low ratings)")

        if len(df) == 0:
            logger.error(f"❌ NO BUSINESSES LEFT after rating filter! All had ratings below {config.MIN_RATING}")
            logger.warning(f"💡 TIP: Lower MIN_RATING in config.py (current: {config.MIN_RATING})")
            df.to_csv(output_file, index=False, encoding='utf-8')
            return df

        # FILTER 4: Minimum reviews (optional - set to 0 to skip)
        if config.MIN_REVIEWS > 0:
            before_reviews = len(df)
            df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
            df = df[(df['review_count'] >= config.MIN_REVIEWS) | (df['review_count'].isna())]
            logger.info(f"✓ After REVIEW filter: {len(df)} businesses (removed {before_reviews - len(df)})")
        else:
            logger.info(f"✓ Review filter skipped (MIN_REVIEWS = 0)")

        # Remove duplicates by phone
        before_dedup = len(df)
        df = df.drop_duplicates(subset=['phone'], keep='first')
        if before_dedup > len(df):
            logger.info(f"✓ Removed {before_dedup - len(df)} duplicate phone numbers")

        # Add status columns for tracking
        df['status'] = 'new'
        df['notes'] = ''
        df['email_sent_date'] = ''
        df['preview_url'] = ''

        # Save filtered data
        df.to_csv(output_file, index=False, encoding='utf-8')
        logger.info(f"\n✓ Filtered data saved to {output_file}")
        logger.info(f"📊 SUMMARY: {original_count} scraped -> {len(df)} QUALIFIED LEADS")

        # Show qualified leads
        if len(df) > 0:
            logger.info("\n=== ✅ QUALIFIED LEADS (NO WEBSITE + HAS CONTACT) ===")
            for idx, row in df.iterrows():
                contact = f"Phone: {row['phone']}" if row['phone'] != 'N/A' else f"Email: {row['email']}"
                logger.info(f"{idx + 1}. {row['business_name']} | {contact} | Rating: {row['rating']}")
        else:
            logger.warning("\n⚠️  NO QUALIFIED LEADS FOUND!")
            logger.warning("💡 SUGGESTIONS:")
            logger.warning(f"   - Lower MIN_RATING in config.py (current: {config.MIN_RATING})")
            logger.warning(f"   - Increase MAX_RESULTS to scrape more businesses")
            logger.warning(f"   - Try a different city/location")

        return df

    except Exception as e:
        logger.error(f"Filtering failed: {e}")
        raise


def run_filter():
    """Main function to run filter"""
    df = filter_leads(config.RAW_DATA_FILE, config.QUALIFIED_DATA_FILE)
    return df

