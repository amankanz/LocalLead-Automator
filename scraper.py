# locallead/LocalLead Automator/scraper.py

"""
Google Maps scraper for dental clinic data
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import pandas as pd
import config
from utils import setup_logging, clean_phone, clean_website

logger = setup_logging(config.LOG_FILE)


class GoogleMapsScraper:
    def __init__(self):
        self.driver = None
        self.results = []
        self.wait = None

    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        logger.info("Setting up Chrome WebDriver...")
        options = webdriver.ChromeOptions()

        if config.HEADLESS_MODE:
            options.add_argument('--headless')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_argument('--start-maximized')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, config.ELEMENT_WAIT)
        logger.info("WebDriver setup complete - Browser should be visible now!")

    def search_google_maps(self):
        """Perform Google Maps search"""
        search_url = f"https://www.google.com/maps/search/{config.SEARCH_QUERY}+in+{config.SEARCH_LOCATION}"
        logger.info(f"Searching: {search_url}")

        self.driver.get(search_url)
        time.sleep(config.PAGE_LOAD_WAIT)
        logger.info("Search page loaded - you should see results now")

    def scroll_results(self):
        """Scroll through results to load more businesses"""
        logger.info("Scrolling to load results...")

        try:
            # Wait for results to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

            for i in range(3):  # Reduced scrolls for testing
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(config.SCROLL_PAUSE_TIME)
                logger.info(f"Scroll {i + 1}/3 complete")

        except Exception as e:
            logger.warning(f"Scroll error: {e}")

    def safe_get_text(self, by, selector, default="N/A"):
        """Safely get text from element with retry logic"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                element = self.wait.until(EC.presence_of_element_located((by, selector)))
                return element.text if element.text else default
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                if attempt == max_retries - 1:
                    return default
                time.sleep(0.5)
        return default

    def safe_get_attribute(self, by, selector, attribute, default="N/A"):
        """Safely get attribute from element"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                element = self.wait.until(EC.presence_of_element_located((by, selector)))
                value = element.get_attribute(attribute)
                return value if value else default
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                if attempt == max_retries - 1:
                    return default
                time.sleep(0.5)
        return default

    def extract_business_data(self):
        """Extract data from currently open business details panel"""
        data = {
            'business_name': 'N/A',
            'category': 'N/A',
            'phone': 'N/A',
            'email': 'N/A',
            'website': 'N/A',
            'rating': 'N/A',
            'review_count': 'N/A',
            'address': 'N/A',
            'city': config.SEARCH_LOCATION,
            'maps_url': 'N/A'
        }

        try:
            # Wait for the details panel to load
            time.sleep(2)

            # Business Name
            data['business_name'] = self.safe_get_text(By.CSS_SELECTOR, 'h1.DUwDvf')

            # Category
            data['category'] = self.safe_get_text(By.CSS_SELECTOR, 'button[jsaction*="category"]')

            # Rating
            data['rating'] = self.safe_get_text(By.CSS_SELECTOR, 'div.F7nice span[aria-hidden="true"]')

            # Review Count
            try:
                reviews_elem = self.driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-label*="reviews"]')
                reviews_text = reviews_elem.get_attribute('aria-label')
                data['review_count'] = reviews_text.split()[0].replace(',', '')
            except:
                data['review_count'] = 'N/A'

            # Address
            data['address'] = self.safe_get_attribute(By.CSS_SELECTOR, 'button[data-item-id="address"]', 'aria-label')
            if data['address'] != 'N/A':
                data['address'] = data['address'].replace('Address: ', '')

            # Phone
            phone_text = self.safe_get_attribute(By.CSS_SELECTOR, 'button[data-item-id*="phone"]', 'aria-label')
            if phone_text != 'N/A':
                data['phone'] = clean_phone(phone_text.replace('Phone: ', ''))

            # Website
            website_url = self.safe_get_attribute(By.CSS_SELECTOR, 'a[data-item-id="authority"]', 'href')
            data['website'] = clean_website(website_url)

            # Maps URL
            data['maps_url'] = self.driver.current_url

            logger.info(f"✓ Extracted: {data['business_name']} | Phone: {data['phone']} | Website: {data['website']}")

        except Exception as e:
            logger.error(f"Error extracting business data: {e}")

        return data

    def scrape(self):
        """Main scraping logic"""
        try:
            self.setup_driver()
            self.search_google_maps()
            self.scroll_results()

            # Get all business listings - FIXED: Get fresh list each time
            logger.info("Finding business listings...")

            count = 0
            max_attempts = config.MAX_RESULTS * 3  # Safety limit
            attempts = 0

            while count < config.MAX_RESULTS and attempts < max_attempts:
                attempts += 1

                try:
                    # Get fresh list of listings each iteration (avoids stale elements)
                    listings = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div > a')

                    if count >= len(listings):
                        logger.info("No more listings available")
                        break

                    logger.info(f"Processing business {count + 1}/{config.MAX_RESULTS}...")

                    # Click on the listing
                    listing = listings[count]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", listing)
                    time.sleep(0.5)
                    listing.click()
                    time.sleep(2)

                    # Extract data
                    business_data = self.extract_business_data()

                    # Only save if we got at least a name
                    if business_data['business_name'] != 'N/A':
                        self.results.append(business_data)
                        count += 1

                    time.sleep(1)

                except StaleElementReferenceException:
                    logger.warning(f"Stale element at position {count}, retrying...")
                    time.sleep(1)
                    continue

                except Exception as e:
                    logger.error(f"Error processing listing {count + 1}: {e}")
                    count += 1  # Move to next even if this one failed
                    continue

            logger.info(f"Scraping complete! Collected {len(self.results)} businesses")

        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise

        finally:
            if self.driver:
                logger.info("Keeping browser open for 5 seconds so you can see the results...")
                time.sleep(5)
                self.driver.quit()
                logger.info("Browser closed")

    def save_to_csv(self):
        """Save scraped data to CSV"""
        if not self.results:
            logger.warning("No data to save")
            return None

        df = pd.DataFrame(self.results)
        df.to_csv(config.RAW_DATA_FILE, index=False, encoding='utf-8')
        logger.info(f"Data saved to {config.RAW_DATA_FILE}")

        # Print preview
        logger.info("\n=== DATA PREVIEW ===")
        for idx, row in df.iterrows():
            logger.info(f"{idx + 1}. {row['business_name']} | Website: {row['website']} | Phone: {row['phone']}")

        return df


def run_scraper():
    """Main function to run scraper"""
    scraper = GoogleMapsScraper()
    scraper.scrape()
    df = scraper.save_to_csv()
    return df

