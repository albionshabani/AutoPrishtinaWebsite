# FILE: EncarScraper/app/enrich.py
# No major changes needed

import asyncio
import logging
import os
import sys
import json
import random
from dotenv import load_dotenv

load_dotenv()

from .config import *
from .engine import EnrichmentEngine
from .services import ApiClient, TranslationManager, EurExchangeRateCache, StatusManager
from .translations import (
    BRAND_TRANSLATIONS, MODEL_TRANSLATIONS, BADGE_TRANSLATIONS, COLOR_TRANSLATIONS,
    TRANSMISSION_TRANSLATIONS, FUEL_TRANSLATIONS,
)

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s [%(name)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("enrich")

async def main():
    logger.info("--- 🟢 Enrichment Process Started ---")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(DISCOVERED_LISTINGS_FILE):
        logger.error(f"FATAL: The discovery data file was not found at {DISCOVERED_LISTINGS_FILE}.")
        sys.exit(1)

    with open(ENRICHMENT_PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    translation_maps = {
        'Brand': BRAND_TRANSLATIONS, 'Model': MODEL_TRANSLATIONS, 'Badge': BADGE_TRANSLATIONS,
        'Color': COLOR_TRANSLATIONS, 'Transmission': TRANSMISSION_TRANSLATIONS,
        'Fuel': FUEL_TRANSLATIONS,
    }
    translator = TranslationManager(translation_maps)
    status_manager = StatusManager()
    
    engine = EnrichmentEngine(translator, EurExchangeRateCache(), status_manager)
    
    try:
        with open(DISCOVERED_LISTINGS_FILE, 'r', encoding='utf-8') as f:
            cars_to_process = json.load(f)
        
        await engine.run_enrichment(cars_to_process)
        
    except json.JSONDecodeError:
        logger.critical(f"Could not read or decode {DISCOVERED_LISTINGS_FILE}. It may be corrupted.")
    except Exception as e:
        logger.critical(f"A fatal error occurred during enrichment: {e}", exc_info=True)
    finally:
        if os.path.exists(ENRICHMENT_PID_FILE):
            os.remove(ENRICHMENT_PID_FILE)
        logger.info("--- 🟢 Enrichment Process Finished ---")

if __name__ == "__main__":
    asyncio.run(main())