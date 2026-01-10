
# # Phase 2: enrich with Maps data

# """
# Phase 2: Lead Enrichment from Google Maps
# Scrape detailed business information from Maps profiles
# """
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
# import config
# from utils import setup_logging
#
# logger = setup_logging(config.LOG_FILE)
#
#
# class LeadEnricher:
#     def __init__(self):
#         self.driver = None
#         self.wait = None
#
#     def setup_driver(self):
#         """Initialize Chrome WebDriver"""
#         logger.info("Setting up Chrome WebDriver for enrichment...")
#         options = webdriver.ChromeOptions()
#
#         if config.HEADLESS_MODE:
#             options.add_argument('--headless')
#
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
#         options.add_argument('--start-maximized')
#
#         service = Service(ChromeDriverManager().install())
#         self.driver = webdriver.Chrome(service=service, options=options)
#         self.wait = WebDriverWait(self.driver, config.ELEMENT_WAIT)
#         logger.info("WebDriver ready for enrichment!")
#
#     def safe_get_text(self, by, selector, default="N/A"):
#         """Safely get text from element"""
#         try:
#             element = WebDriverWait(self.driver, 3).until(
#                 EC.presence_of_element_located((by, selector))
#             )
#             return element.text.strip() if element.text else default
#         except:
#             return default
#
#     def safe_get_multiple(self, by, selector):
#         """Safely get multiple elements"""
#         try:
#             elements = self.driver.find_elements(by, selector)
#             return elements if elements else []
#         except:
#             return []
#
#     def scroll_to_reviews(self):
#         """Scroll to load reviews section"""
#         try:
#             # Try to find and click "Reviews" tab if exists
#             reviews_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Reviews"]')
#             if reviews_buttons:
#                 reviews_buttons[0].click()
#                 time.sleep(2)
#
#             # Scroll down to load reviews
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
#             time.sleep(1)
#
#         except Exception as e:
#             logger.debug(f"Could not scroll to reviews: {e}")
#
#     # def extract_about(self):
#     #     """Extract business description/about text"""
#     #     try:
#     #         # Try multiple selectors for "About" section
#     #         selectors = [
#     #             'div[class*="description"]',
#     #             'div[aria-label*="About"]',
#     #             'div.WeS02d',  # Common About section class
#     #             'div.PYvSYb'  # Alternative About section
#     #         ]
#     #
#     #         for selector in selectors:
#     #             about = self.safe_get_text(By.CSS_SELECTOR, selector)
#     #             if about != "N/A" and len(about) > 10:
#     #                 return about
#     #
#     #         return "N/A"
#     #     except:
#     #         return "N/A"
#
#     def extract_about(self):
#         """Build an About section from attributes & highlights"""
#         sections = []
#
#         try:
#             groups = self.driver.find_elements(By.CSS_SELECTOR, 'div.AQrsxc')
#
#             for group in groups:
#                 text = group.text.strip()
#                 if text and len(text) > 3:
#                     sections.append(text)
#
#             return " | ".join(sections) if sections else "N/A"
#
#         except:
#             return "N/A"
#
#     def extract_services(self):
#         """Extract list of services offered"""
#         try:
#             services = []
#
#             # Look for service items
#             service_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[jsaction*="service"]')
#
#             if not service_elements:
#                 # Try alternative selectors
#                 service_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'ul[aria-label*="Services"] li')
#
#             for elem in service_elements[:10]:  # Limit to 10 services
#                 text = elem.text.strip()
#                 if text and len(text) > 2:
#                     services.append(text)
#
#             return "; ".join(services) if services else "N/A"
#         except:
#             return "N/A"
#
#     def extract_reviews(self):
#         """Extract top reviews"""
#         reviews = []
#
#         try:
#             self.scroll_to_reviews()
#
#             # Find review elements
#             review_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[data-review-id]')
#
#             if not review_elements:
#                 # Try alternative selector
#                 review_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div.jftiEf')
#
#             for idx, review_elem in enumerate(review_elements[:config.MAX_REVIEWS_TO_SCRAPE]):
#                 try:
#                     # Extract rating
#                     rating = "N/A"
#                     try:
#                         rating_elem = review_elem.find_element(By.CSS_SELECTOR, 'span[aria-label*="stars"]')
#                         rating_text = rating_elem.get_attribute('aria-label')
#                         rating = rating_text.split()[0] if rating_text else "N/A"
#                     except:
#                         pass
#
#                     # Extract review text
#                     review_text = "N/A"
#                     try:
#                         text_elem = review_elem.find_element(By.CSS_SELECTOR, 'span.wiI7pd')
#                         review_text = text_elem.text.strip()
#
#                         # If text is truncated, try to expand it
#                         try:
#                             more_button = review_elem.find_element(By.CSS_SELECTOR, 'button[aria-label*="More"]')
#                             more_button.click()
#                             time.sleep(0.5)
#                             review_text = text_elem.text.strip()
#                         except:
#                             pass
#                     except:
#                         pass
#
#                     # Extract reviewer name
#                     reviewer = "N/A"
#                     try:
#                         reviewer_elem = review_elem.find_element(
#                             By.CSS_SELECTOR, 'div.d4r55'
#                         )
#                         reviewer = reviewer_elem.text.strip()
#                     except:
#                         pass
#
#                     reviews.append({
#                         'name': reviewer,
#                         'rating': rating,
#                         'text': review_text[:500] if review_text != "N/A" else "N/A"  # Limit length
#                     })
#
#                 except Exception as e:
#                     logger.debug(f"Error extracting review {idx + 1}: {e}")
#                     reviews.append({'rating': 'N/A', 'text': 'N/A'})
#
#             # Pad with N/A if not enough reviews
#             while len(reviews) < config.MAX_REVIEWS_TO_SCRAPE:
#                 reviews.append({'rating': 'N/A', 'text': 'N/A'})
#
#         except Exception as e:
#             logger.debug(f"Error extracting reviews: {e}")
#             # Return empty reviews
#             reviews = [{'rating': 'N/A', 'text': 'N/A'}] * config.MAX_REVIEWS_TO_SCRAPE
#
#         return reviews
#
#     def extract_highlights(self):
#         """Extract business highlights/attributes"""
#         try:
#             highlights = []
#
#             # Look for highlight badges/chips
#             highlight_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[class*="accessibility"]')
#
#             if not highlight_elements:
#                 highlight_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div.AQrsxc')
#
#             for elem in highlight_elements[:5]:  # Limit to 5 highlights
#                 text = elem.text.strip()
#                 if text and len(text) > 2:
#                     highlights.append(text)
#
#             return "; ".join(highlights) if highlights else "N/A"
#         except:
#             return "N/A"
#
#     # def extract_opening_hours(self):
#     #     """Extract detailed weekly opening hours from Google Maps"""
#     #     try:
#     #         # Try to find the clickable hours dropdown (span/div)
#     #         hours_triggers = self.driver.find_elements(
#     #             By.XPATH,
#     #             "//span[contains(text(),'Open') or contains(text(),'Closed') or contains(text(),'Hours')]"
#     #         )
#     #
#     #         if hours_triggers:
#     #             self.driver.execute_script(
#     #                 "arguments[0].click();", hours_triggers[0]
#     #             )
#     #             time.sleep(2)
#     #
#     #         # Now scrape the hours table
#     #         rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
#     #
#     #         hours = []
#     #         for row in rows:
#     #             cols = row.find_elements(By.TAG_NAME, "td")
#     #             if len(cols) == 2:
#     #                 day = cols[0].text.strip()
#     #                 time_range = cols[1].text.strip()
#     #                 hours.append(f"{day}: {time_range}")
#     #
#     #         return "; ".join(hours) if hours else "N/A"
#     #
#     #     except Exception as e:
#     #         logger.debug(f"Opening hours not found: {e}")
#     #         return "N/A"
#
#     def extract_opening_hours(self):
#         """Extract clean, readable weekly opening hours from Google Maps"""
#         try:
#             rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.y0skZc")
#
#             hours = []
#
#             for row in rows:
#                 try:
#                     # Day name
#                     day = row.find_element(
#                         By.CSS_SELECTOR, "td.ylH6lf div"
#                     ).text.strip()
#
#                     # Hours (aria-label is clean & semantic)
#                     time_range = row.find_element(
#                         By.CSS_SELECTOR, "td.mxowUb"
#                     ).get_attribute("aria-label").strip()
#
#                     if day and time_range:
#                         hours.append(f"{day}: {time_range}")
#
#                 except Exception:
#                     continue
#
#             return "; ".join(hours) if hours else "N/A"
#
#         except Exception as e:
#             logger.debug(f"Opening hours extraction failed: {e}")
#             return "N/A"
#
#     def enrich_business(self, business_row):
#         """Enrich a single business with Maps data"""
#         enriched = business_row.copy()
#
#         try:
#             maps_url = business_row['maps_url']
#             business_name = business_row['business_name']
#
#             logger.info(f"🔍 Enriching: {business_name}")
#
#             # Visit the Maps URL
#             self.driver.get(maps_url)
#             time.sleep(config.ENRICHMENT_DELAY)
#
#             # Extract all enrichment data
#             enriched['about_business'] = self.extract_about()
#             enriched['services'] = self.extract_services()
#             enriched['highlights'] = self.extract_highlights()
#             enriched['opening_hours'] = self.extract_opening_hours()
#
#             # Extract reviews
#             reviews = self.extract_reviews()
#             for idx, review in enumerate(reviews):
#                 enriched[f'review_{idx + 1}_name'] = review['name']
#                 enriched[f'review_{idx + 1}_rating'] = review['rating']
#                 enriched[f'review_{idx + 1}_text'] = review['text']
#
#             logger.info(
#                 f"✅ Enriched: {business_name} | About: {len(enriched['about_business'])} chars | Reviews: {len(reviews)}")
#
#         except Exception as e:
#             logger.error(f"❌ Error enriching {business_row['business_name']}: {e}")
#
#             # Add empty fields on error
#             enriched['about_business'] = "N/A"
#             enriched['services'] = "N/A"
#             enriched['highlights'] = "N/A"
#             enriched['opening_hours'] = "N/A"
#             for i in range(1, config.MAX_REVIEWS_TO_SCRAPE + 1):
#                 enriched[f'review_{i}_rating'] = "N/A"
#                 enriched[f'review_{i}_text'] = "N/A"
#
#         return enriched
#
#     def enrich_all(self, input_file, output_file):
#         """Enrich all qualified leads"""
#         logger.info(f"Loading qualified leads from {input_file}...")
#
#         try:
#             df = pd.read_csv(input_file)
#             total = len(df)
#
#             if total == 0:
#                 logger.error("No qualified leads to enrich!")
#                 return None
#
#             logger.info(f"Found {total} qualified leads to enrich")
#
#             self.setup_driver()
#
#             enriched_data = []
#
#             for idx, row in df.iterrows():
#                 logger.info(f"\n--- Enriching {idx + 1}/{total} ---")
#                 enriched_row = self.enrich_business(row)
#                 enriched_data.append(enriched_row)
#
#                 # Small delay between businesses
#                 time.sleep(1)
#
#             # Save enriched data
#             enriched_df = pd.DataFrame(enriched_data)
#             enriched_df.to_csv(output_file, index=False, encoding='utf-8')
#
#             logger.info(f"\n✅ Enrichment complete! Saved to {output_file}")
#             logger.info(f"📊 Enriched {len(enriched_df)} businesses")
#
#             return enriched_df
#
#         except Exception as e:
#             logger.error(f"Enrichment failed: {e}")
#             raise
#
#         finally:
#             if self.driver:
#                 logger.info("Keeping browser open for 5 seconds...")
#                 time.sleep(5)
#                 self.driver.quit()
#                 logger.info("Browser closed")
#
#
# def run_enricher():
#     """Main function to run enricher"""
#     enricher = LeadEnricher()
#     df = enricher.enrich_all(config.QUALIFIED_DATA_FILE, config.ENRICHED_DATA_FILE)
#     return df
#
#


"""
Phase 2: Lead Enrichment from Google Maps
Scrape detailed business information from Maps profiles
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import config
from utils import setup_logging

logger = setup_logging(config.LOG_FILE)


class LeadEnricher:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        logger.info("Setting up Chrome WebDriver for enrichment...")
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
        logger.info("WebDriver ready for enrichment!")

    def safe_get_text(self, by, selector, default="N/A"):
        """Safely get text from element"""
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((by, selector))
            )
            return element.text.strip() if element.text else default
        except:
            return default

    def safe_get_multiple(self, by, selector):
        """Safely get multiple elements"""
        try:
            elements = self.driver.find_elements(by, selector)
            return elements if elements else []
        except:
            return []

    def scroll_to_reviews(self):
        """Scroll to load reviews section"""
        try:
            # Try to find and click "Reviews" tab if exists
            reviews_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Reviews"]')
            if reviews_buttons:
                reviews_buttons[0].click()
                time.sleep(2)

            # Scroll down to load reviews
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)

        except Exception as e:
            logger.debug(f"Could not scroll to reviews: {e}")

    def extract_about(self):
        """Extract business description/about text"""
        try:
            # Try multiple selectors for "About" section
            selectors = [
                'div[class*="description"]',
                'div[aria-label*="About"]',
                'div.WeS02d',  # Common About section class
                'div.PYvSYb'  # Alternative About section
            ]

            for selector in selectors:
                about = self.safe_get_text(By.CSS_SELECTOR, selector)
                if about != "N/A" and len(about) > 10:
                    return about

            return "N/A"
        except:
            return "N/A"

    def extract_services(self):
        """Extract list of services offered"""
        try:
            services = []

            # Look for service items
            service_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[jsaction*="service"]')

            if not service_elements:
                # Try alternative selectors
                service_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'ul[aria-label*="Services"] li')

            for elem in service_elements[:10]:  # Limit to 10 services
                text = elem.text.strip()
                if text and len(text) > 2:
                    services.append(text)

            return "; ".join(services) if services else "N/A"
        except:
            return "N/A"

    # def extract_reviews(self):
    #     """Extract top reviews"""
    #     reviews = []
    #
    #     try:
    #         self.scroll_to_reviews()
    #
    #         # Find review elements
    #         review_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[data-review-id]')
    #
    #         if not review_elements:
    #             # Try alternative selector
    #             review_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div.jftiEf')
    #
    #         for idx, review_elem in enumerate(review_elements[:config.MAX_REVIEWS_TO_SCRAPE]):
    #             try:
    #                 # Extract rating
    #                 rating = "N/A"
    #                 try:
    #                     rating_elem = review_elem.find_element(By.CSS_SELECTOR, 'span[aria-label*="stars"]')
    #                     rating_text = rating_elem.get_attribute('aria-label')
    #                     rating = rating_text.split()[0] if rating_text else "N/A"
    #                 except:
    #                     pass
    #
    #                 # Extract review text
    #                 review_text = "N/A"
    #                 try:
    #                     text_elem = review_elem.find_element(By.CSS_SELECTOR, 'span.wiI7pd')
    #                     review_text = text_elem.text.strip()
    #
    #                     # If text is truncated, try to expand it
    #                     try:
    #                         more_button = review_elem.find_element(By.CSS_SELECTOR, 'button[aria-label*="More"]')
    #                         more_button.click()
    #                         time.sleep(0.5)
    #                         review_text = text_elem.text.strip()
    #                     except:
    #                         pass
    #                 except:
    #                     pass
    #
    #                 reviews.append({
    #                     'rating': rating,
    #                     'text': review_text[:500] if review_text != "N/A" else "N/A"  # Limit length
    #                 })
    #
    #             except Exception as e:
    #                 logger.debug(f"Error extracting review {idx + 1}: {e}")
    #                 reviews.append({'rating': 'N/A', 'text': 'N/A'})
    #
    #         # Pad with N/A if not enough reviews
    #         while len(reviews) < config.MAX_REVIEWS_TO_SCRAPE:
    #             reviews.append({'rating': 'N/A', 'text': 'N/A'})
    #
    #     except Exception as e:
    #         logger.debug(f"Error extracting reviews: {e}")
    #         # Return empty reviews
    #         reviews = [{'rating': 'N/A', 'text': 'N/A'}] * config.MAX_REVIEWS_TO_SCRAPE
    #
    #     return reviews

    def extract_reviews(self):
        """Extract top customer reviews (text reviews only)"""
        reviews = []

        try:
            self.scroll_to_reviews()

            review_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")

            for review_elem in review_elements:
                if len(reviews) >= config.MAX_REVIEWS_TO_SCRAPE:
                    break

                try:
                    # Reviewer name
                    name = "N/A"
                    try:
                        name = review_elem.find_element(
                            By.CSS_SELECTOR, "div.d4r55"
                        ).text.strip()
                    except:
                        pass

                    # Rating
                    rating = "N/A"
                    try:
                        rating_elem = review_elem.find_element(
                            By.CSS_SELECTOR, 'span[aria-label*="stars"]'
                        )
                        rating = rating_elem.get_attribute("aria-label").split()[0]
                    except:
                        pass

                    # Review text (MANDATORY)
                    review_text = ""
                    try:
                        text_elem = review_elem.find_element(
                            By.CSS_SELECTOR, "span.wiI7pd"
                        )

                        # Expand if truncated
                        try:
                            more = review_elem.find_element(
                                By.CSS_SELECTOR, 'button[aria-label*="More"]'
                            )
                            self.driver.execute_script("arguments[0].click();", more)
                            time.sleep(0.3)
                        except:
                            pass

                        review_text = text_elem.text.strip()
                    except:
                        continue  # 🚨 skip reviews without text

                    if not review_text:
                        continue  # 🚨 skip empty reviews

                    reviews.append({
                        "name": name,
                        "rating": rating,
                        "text": review_text[:500]
                    })

                except Exception:
                    continue

        except Exception as e:
            logger.debug(f"Review extraction failed: {e}")

        return reviews

    def extract_highlights(self):
        """Extract business highlights/attributes"""
        try:
            highlights = []

            # Look for highlight badges/chips
            highlight_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div[class*="accessibility"]')

            if not highlight_elements:
                highlight_elements = self.safe_get_multiple(By.CSS_SELECTOR, 'div.AQrsxc')

            for elem in highlight_elements[:5]:  # Limit to 5 highlights
                text = elem.text.strip()
                if text and len(text) > 2:
                    highlights.append(text)

            return "; ".join(highlights) if highlights else "N/A"
        except:
            return "N/A"

    # def extract_opening_hours(self):
    #     """Extract business hours"""
    #     try:
    #         # Look for hours button/section
    #         hours_button = self.safe_get_text(By.CSS_SELECTOR, 'button[data-item-id*="hours"]')
    #
    #         if hours_button != "N/A":
    #             return hours_button
    #
    #         # Try alternative selector
    #         hours_text = self.safe_get_text(By.CSS_SELECTOR, 'div[aria-label*="Hours"]')
    #
    #         return hours_text if hours_text != "N/A" else "N/A"
    #     except:
    #         return "N/A"

    def extract_opening_hours(self):
        """Extract clean weekly opening hours from Google Maps"""
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.y0skZc")
            hours = []

            for row in rows:
                try:
                    day = row.find_element(
                        By.CSS_SELECTOR, "td.ylH6lf div"
                    ).text.strip()

                    time_range = row.find_element(
                        By.CSS_SELECTOR, "td.mxowUb"
                    ).get_attribute("aria-label").strip()

                    if day and time_range:
                        hours.append(f"{day}: {time_range}")

                except StaleElementReferenceException:
                    continue

            return "; ".join(hours) if hours else "N/A"

        except Exception as e:
            logger.debug(f"Opening hours extraction failed: {e}")
            return "N/A"

    def enrich_business(self, business_row):
        """Enrich a single business with Maps data"""
        enriched = business_row.copy()

        try:
            maps_url = business_row['maps_url']
            business_name = business_row['business_name']

            logger.info(f"🔍 Enriching: {business_name}")

            # Visit the Maps URL
            self.driver.get(maps_url)
            time.sleep(config.ENRICHMENT_DELAY)

            # Extract all enrichment data
            enriched['about_business'] = self.extract_about()
            enriched['services'] = self.extract_services()
            enriched['highlights'] = self.extract_highlights()
            enriched['opening_hours'] = self.extract_opening_hours()

            # Extract reviews
            reviews = self.extract_reviews()
            for idx, review in enumerate(reviews):
                enriched[f'review_{idx + 1}_name'] = review['name']  # ← This line adds name
                enriched[f'review_{idx + 1}_rating'] = review['rating']
                enriched[f'review_{idx + 1}_text'] = review['text']

            for i in range(len(reviews) + 1, config.MAX_REVIEWS_TO_SCRAPE + 1):
                enriched[f'review_{i}_name'] = "N/A"
                enriched[f'review_{i}_rating'] = "N/A"
                enriched[f'review_{i}_text'] = "N/A"

            logger.info(
                f"✅ Enriched: {business_name} | About: {len(enriched['about_business'])} chars | Reviews: {len(reviews)}")

        except Exception as e:
            logger.error(f"❌ Error enriching {business_row['business_name']}: {e}")

            # Add empty fields on error
            enriched['about_business'] = "N/A"
            enriched['services'] = "N/A"
            enriched['highlights'] = "N/A"
            enriched['opening_hours'] = "N/A"
            for i in range(1, config.MAX_REVIEWS_TO_SCRAPE + 1):
                enriched[f'review_{i}_rating'] = "N/A"
                enriched[f'review_{i}_text'] = "N/A"

        return enriched

    def enrich_all(self, input_file, output_file):
        """Enrich all qualified leads"""
        logger.info(f"Loading qualified leads from {input_file}...")

        try:
            df = pd.read_csv(input_file)
            total = len(df)

            if total == 0:
                logger.error("No qualified leads to enrich!")
                return None

            logger.info(f"Found {total} qualified leads to enrich")

            self.setup_driver()

            enriched_data = []

            for idx, row in df.iterrows():
                logger.info(f"\n--- Enriching {idx + 1}/{total} ---")
                enriched_row = self.enrich_business(row)
                enriched_data.append(enriched_row)

                # Small delay between businesses
                time.sleep(1)

            # Save enriched data
            enriched_df = pd.DataFrame(enriched_data)
            enriched_df.to_csv(output_file, index=False, encoding='utf-8')

            logger.info(f"\n✅ Enrichment complete! Saved to {output_file}")
            logger.info(f"📊 Enriched {len(enriched_df)} businesses")

            return enriched_df

        except Exception as e:
            logger.error(f"Enrichment failed: {e}")
            raise

        finally:
            if self.driver:
                logger.info("Keeping browser open for 5 seconds...")
                time.sleep(5)
                self.driver.quit()
                logger.info("Browser closed")


def run_enricher():
    """Main function to run enricher"""
    enricher = LeadEnricher()
    df = enricher.enrich_all(config.QUALIFIED_DATA_FILE, config.ENRICHED_DATA_FILE)
    return df
