# FILE: EncarScraper/app/main.py

import asyncio
import logging
import httpx
import os
import signal

from .services import ApiClient, TranslationManager, EurExchangeRateCache, save_new_translations_to_master_file
from .engine import Scraper
from .config import HEADERS, COOKIE_STRING, DATA_DIR, STOP_SIGNAL_FILE
from .translations import (
    BRAND_TRANSLATIONS, MODEL_TRANSLATIONS, BADGE_TRANSLATIONS, COLOR_TRANSLATIONS,
    TRANSMISSION_TRANSLATIONS, MODEL_GROUP_TRANSLATIONS, FUEL_TRANSLATIONS,
    SALE_TYPE_TRANSLATIONS, DIAGNOSIS_RESULT_TRANSLATIONS, SELLER_COMMENT_TRANSLATIONS
)

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s [%(name)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async ***REMOVED***
    scraper = None
    
    def signal_handler(sig, frame):
        logger.info(f"Signal {sig} received, initiating shutdown.")
        if not os.path.exists(STOP_SIGNAL_FILE):
            with open(STOP_SIGNAL_FILE, "w") as f: f.write("stop")
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("--- Scraper worker process started. ---")
    if os.path.exists(STOP_SIGNAL_FILE): os.remove(STOP_SIGNAL_FILE)
    os.makedirs(DATA_DIR, exist_ok=True)
    
    final_headers = HEADERS.copy()
    if COOKIE_STRING: final_headers['cookie'] = COOKIE_STRING

    async with httpx.AsyncClient(headers=final_headers, timeout=30, follow_redirects=True) as http_client:
        translation_maps = {
            'Brand': BRAND_TRANSLATIONS, 'Model': MODEL_TRANSLATIONS, 'Badge': BADGE_TRANSLATIONS,
            'Color': COLOR_TRANSLATIONS, 'Transmission': TRANSMISSION_TRANSLATIONS,
            'Model Group': MODEL_GROUP_TRANSLATIONS, 'Fuel': FUEL_TRANSLATIONS,
            'Sale Type': SALE_TYPE_TRANSLATIONS, 'Diagnosis Result': DIAGNOSIS_RESULT_TRANSLATIONS,
            'Seller Comment': SELLER_COMMENT_TRANSLATIONS,
        }
        translator = TranslationManager(translation_maps)
        
        scraper = Scraper(client=ApiClient(http_client), translator=translator, cache=EurExchangeRateCache())
        await scraper.run()
    
    if any(translator.new_translations.values()):
        logger.info("New translatable terms were found. Saving to a file for review.")
        save_new_translations_to_master_file(translator.new_translations)

***REMOVED***
    try:
        asyncio.run(main())
        logger.info("--- Worker script has finished execution. ---")
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("--- Main process interrupted. ---")
    finally:
        if os.path.exists(STOP_SIGNAL_FILE):
            os.remove(STOP_SIGNAL_FILE)