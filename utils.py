# # LocalLead Automator/config.py
# # helper functions

"""
Helper utility functions
"""
# import re
# import os
# import logging
# from datetime import datetime
#
#
# def setup_logging(log_file):
#     """Setup logging configuration"""
#     os.makedirs(os.path.dirname(log_file), exist_ok=True)
#
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         handlers=[
#             logging.FileHandler(log_file),
#             logging.StreamHandler()
#         ]
#     )
#     return logging.getLogger(__name__)
#
#
# def validate_email(email):
#     """Check if email format is valid"""
#     if not email or email == "N/A":
#         return False
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None
#
#
# def clean_phone(phone):
#     """Clean and format phone number"""
#     if not phone or phone == "N/A":
#         return "N/A"
#     # Remove all non-numeric characters
#     cleaned = re.sub(r'\D', '', phone)
#     return cleaned if len(cleaned) >= 10 else "N/A"
#
#
# def clean_website(url):
#     """Clean website URL"""
#     if not url or url == "N/A":
#         return "N/A"
#     url = url.strip()
#     if not url.startswith('http'):
#         url = 'https://' + url
#     return url
#
#
# def ensure_directories():
#     """Create necessary directories if they don't exist"""
#     os.makedirs('data', exist_ok=True)
#     os.makedirs('logs', exist_ok=True)


"""
Helper utility functions
"""
import re
import os
import logging
from datetime import datetime


def setup_logging(log_file):
    """Setup logging configuration"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),  # FIXED: Added UTF-8 encoding
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def validate_email(email):
    """Check if email format is valid"""
    if not email or email == "N/A":
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_phone(phone):
    """Clean and format phone number"""
    if not phone or phone == "N/A":
        return "N/A"
    # Remove all non-numeric characters
    cleaned = re.sub(r'\D', '', phone)
    return cleaned if len(cleaned) >= 10 else "N/A"


def clean_website(url):
    """Clean website URL"""
    if not url or url == "N/A" or url == "":
        return "N/A"
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url


def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
