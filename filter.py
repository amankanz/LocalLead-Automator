# LocalLead Automator/filter.py
# filter and clean data
"""
Filter and clean the scraped data
"""
# import pandas as pd
# import config
# from utils import setup_logging, validate_email
#
# logger = setup_logging(config.LOG_FILE)
#
#
# def filter_leads(input_file, output_file):
#     """Filter leads based on criteria"""
#     logger.info(f"Loading data from {input_file}...")
#
#     try:
#         df = pd.read_csv(input_file)
#         logger.info(f"Loaded {len(df)} businesses")
#
#         original_count = len(df)
#
#         # Filter 1: Remove businesses WITH professional websites (we want those WITHOUT)
#         if config.EXCLUDE_WEBSITES:
#             df = df[df['website'] == 'N/A']
#             logger.info(f"After website filter: {len(df)} businesses (removed {original_count - len(df)})")
#
#         # Filter 2: Must have phone or email
#         df = df[(df['phone'] != 'N/A') | (df['email'] != 'N/A')]
#         logger.info(f"After contact filter: {len(df)} businesses")
#
#         # Filter 3: Minimum rating
#         df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
#         df = df[(df['rating'] >= config.MIN_RATING) | (df['rating'].isna())]
#         logger.info(f"After rating filter: {len(df)} businesses")
#
#         # Filter 4: Minimum reviews
#         df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
#         df = df[(df['review_count'] >= config.MIN_REVIEWS) | (df['review_count'].isna())]
#         logger.info(f"After review filter: {len(df)} businesses")
#
#         # Remove duplicates by phone
#         df = df.drop_duplicates(subset=['phone'], keep='first')
#         logger.info(f"After duplicate removal: {len(df)} businesses")
#
#         # Add status column
#         df['status'] = 'new'
#         df['notes'] = ''
#
#         # Save filtered data
#         df.to_csv(output_file, index=False)
#         logger.info(f"Filtered data saved to {output_file}")
#         logger.info(f"SUMMARY: {original_count} scraped → {len(df)} qualified leads")
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

logger = setup_logging(config.LOG_FILE)


def filter_leads(input_file, output_file):
    """Filter leads based on criteria"""
    logger.info(f"Loading data from {input_file}...")

    try:
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} businesses")

        original_count = len(df)

        # Show what we have before filtering
        logger.info("\n=== BEFORE FILTERING ===")
        logger.info(f"Businesses with websites: {len(df[df['website'] != 'N/A'])}")
        logger.info(f"Businesses without websites: {len(df[df['website'] == 'N/A'])}")
        logger.info(f"Businesses with phone: {len(df[df['phone'] != 'N/A'])}")
        logger.info(f"Businesses with email: {len(df[df['email'] != 'N/A'])}")

        # Filter 1: Website filter (FIXED LOGIC)
        if config.EXCLUDE_WEBSITES:
            # Keep ONLY businesses WITHOUT websites
            df = df[df['website'] == 'N/A']
            logger.info(f"After website filter (kept businesses WITHOUT websites): {len(df)} businesses")
        else:
            # Keep ALL businesses (those with AND without websites)
            logger.info(f"Website filter disabled - keeping all businesses: {len(df)} businesses")

        # Filter 2: Must have phone or email
        before_contact = len(df)
        df = df[(df['phone'] != 'N/A') | (df['email'] != 'N/A')]
        logger.info(
            f"After contact filter (must have phone OR email): {len(df)} businesses (removed {before_contact - len(df)})")

        # Filter 3: Minimum rating (convert to numeric, keep NaN)
        before_rating = len(df)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[(df['rating'] >= config.MIN_RATING) | (df['rating'].isna())]
        logger.info(
            f"After rating filter (>= {config.MIN_RATING}): {len(df)} businesses (removed {before_rating - len(df)})")

        # Filter 4: Minimum reviews (convert to numeric, keep NaN)
        before_reviews = len(df)
        df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
        df = df[(df['review_count'] >= config.MIN_REVIEWS) | (df['review_count'].isna())]
        logger.info(
            f"After review filter (>= {config.MIN_REVIEWS} reviews): {len(df)} businesses (removed {before_reviews - len(df)})")

        # Remove duplicates by phone
        before_dedup = len(df)
        df = df.drop_duplicates(subset=['phone'], keep='first')
        logger.info(f"After duplicate removal: {len(df)} businesses (removed {before_dedup - len(df)} duplicates)")

        # Add status columns for tracking
        df['status'] = 'new'
        df['notes'] = ''
        df['email_sent_date'] = ''
        df['preview_url'] = ''

        # Save filtered data
        df.to_csv(output_file, index=False, encoding='utf-8')
        logger.info(f"Filtered data saved to {output_file}")
        logger.info(f"SUMMARY: {original_count} scraped -> {len(df)} qualified leads")

        # Show qualified leads
        if len(df) > 0:
            logger.info("\n=== QUALIFIED LEADS ===")
            for idx, row in df.iterrows():
                logger.info(f"{idx + 1}. {row['business_name']} | Website: {row['website']} | Phone: {row['phone']}")

        return df

    except Exception as e:
        logger.error(f"Filtering failed: {e}")
        raise


def run_filter():
    """Main function to run filter"""
    df = filter_leads(config.RAW_DATA_FILE, config.QUALIFIED_DATA_FILE)
    return df

