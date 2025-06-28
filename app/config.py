# FILE: EncarScraper/app/config.py

import os

# ========== Core Scraping Settings ==========
MAX_CARS_TO_PROCESS = int(os.getenv("MAX_CARS_TO_PROCESS", "500000"))
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENCY", "50"))
SAVE_PROGRESS_EVERY = int(os.getenv("SAVE_PROGRESS_EVERY", "200"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

# --- Sample Mode for Backend Development ---
# Set to a number > 0 to process only that many new cars and then stop.
# Set to 0 to run the full scraper.
SAMPLE_MODE_COUNT = int(os.getenv("SAMPLE_MODE_COUNT", "0"))

# --- Settings for Mileage-based search ---
MILEAGE_STEP = 10000
MAX_MILEAGE = 500000

# ========== API & Network Settings ==========
BASE_URL = "https://api.encar.com/search/car/list/premium"

# --- NEW HEADERS for the primary search/discovery API ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Origin": "http://www.encar.com",
    "Connection": "keep-alive",
    "Referer": "http://www.encar.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
}

# Cookie string is still useful and can be updated if needed
COOKIE_STRING = "RecentViewAllCar=39628925%2C38508421%2C39356902%2C39772267%2C39628084%2C39766231%2C38518849%2C37923895%2C39437518%2C39834207%2C39451849%2C39707436%2C39497727; RecentViewCar=39628925%2C38508421%2C39356902%2C39772267%2C39628084%2C39766231%2C38518849%2C37923895%2C39437518%2C39834207%2C39451849%2C39707436%2C39497727; RecentViewTruck=; OAX=kkZoKWhZXXYADyGf; _encar_hostname=http://www.encar.com"


# ========== Output, Caching, and Database ==========
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "encar_cars_output.db")
TRANSLATION_MASTER_FILE = os.path.join(DATA_DIR, "translations_master.json")
DISCORD_MESSAGE_ID_FILE = os.path.join(DATA_DIR, "discord_message_id.txt")
STOP_SIGNAL_FILE = os.path.join(DATA_DIR, "stop_signal.txt")

# ========== ID Tracking Files ==========
ALL_LIVE_IDS_FILE = os.path.join(DATA_DIR, "tracker_all_live_ids.txt")
SUCCESS_IDS_FILE = os.path.join(DATA_DIR, "tracker_processed_successfully.txt")
FAILED_IDS_FILE = os.path.join(DATA_DIR, "tracker_failed_enrichment.txt")
PARTIAL_NO_INSPECTION_FILE = os.path.join(DATA_DIR, "tracker_partial_no_inspection.txt")
PARTIAL_NO_RECORD_FILE = os.path.join(DATA_DIR, "tracker_partial_no_record.txt")
PARTIAL_NO_DIAGNOSIS_FILE = os.path.join(DATA_DIR, "tracker_partial_no_diagnosis.txt")

# ========== Feature Toggles ==========
USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"
EXPORT_CSV = os.getenv("EXPORT_CSV", "true").lower() == "true"
EXPORT_JSON = os.getenv("EXPORT_JSON", "true").lower() == "true"
EXPORT_EXCEL = os.getenv("EXPORT_EXCEL", "true").lower() == "true"
    
# ========== Notifications ==========
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", ***REMOVED***)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "***REMOVED***")