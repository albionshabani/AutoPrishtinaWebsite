# FILE: EncarScraper/app/config.py
# FINAL VERSION (Updated for Mobile API)

import os

# ========== Core Scraping Settings ==========
MAX_CARS_TO_PROCESS = int(os.getenv("MAX_CARS_TO_PROCESS", "500000"))
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENCY", "50"))
SAVE_PROGRESS_EVERY = int(os.getenv("SAVE_PROGRESS_EVERY", "200"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "200")) # <-- CHANGED: Mobile API uses a larger batch size

# --- Sample Mode for Backend Development ---
SAMPLE_MODE_COUNT = int(os.getenv("SAMPLE_MODE_COUNT", "0"))

# --- Settings for Mileage-based search ---
MILEAGE_STEP = 10000
MAX_MILEAGE = 500000

# ========== API & Network Settings ==========
# <-- CHANGED: Using the mobile API endpoint now
BASE_URL = "https://api.encar.com/search/car/list/mobile"

# --- NEW HEADERS for the mobile search API ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Origin": "https://car.encar.com",
    "Connection": "keep-alive",
    "Referer": "https://car.encar.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}

# ========== NEW: File paths for Two-Stage Pipeline ==========
DATA_DIR = "data"
# This file will store the raw data from the discovery process.
DISCOVERED_LISTINGS_FILE = os.path.join(DATA_DIR, "discovered_listings.json")
ENRICHMENT_STATUS_FILE = os.path.join(DATA_DIR, "enrich_status.json")

# These files will be used to track if a process is running for the !status command.
DISCOVERY_PID_FILE = os.path.join(DATA_DIR, "discover.pid")
ENRICHMENT_PID_FILE = os.path.join(DATA_DIR, "enrich.pid")



# ========== Output, Caching, and Database ==========
DB_FILE = os.path.join(DATA_DIR, "encar_cars_output.db")
TRANSLATION_MASTER_FILE = os.path.join(DATA_DIR, "translations_master.json")
DISCORD_MESSAGE_ID_FILE = os.path.join(DATA_DIR, "discord_message_id.txt")
STOP_SIGNAL_FILE = os.path.join(DATA_DIR, "stop_signal.txt")
DEBUG_MODE = False

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
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")