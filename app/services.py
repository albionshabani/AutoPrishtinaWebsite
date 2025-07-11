# FILE: EncarScraper/app/services.py
# UPDATED for Robust Two-Stage Pipeline

import httpx
import asyncio
import logging
import time
import os
import json
from typing import Optional, Dict

from deep_translator import GoogleTranslator
from .config import *

logger = logging.getLogger("encar_services")

def save_new_translations_to_master_file(new_translations: dict):
    if not any(new_translations.values()): return
    master_translations = {}
    if os.path.exists(TRANSLATION_MASTER_FILE):
        with open(TRANSLATION_MASTER_FILE, 'r', encoding='utf-8') as f:
            try: master_translations = json.load(f)
            except json.JSONDecodeError: logger.error(f"Could not decode master translation file: {TRANSLATION_MASTER_FILE}")
    for category, terms in new_translations.items():
        if category not in master_translations: master_translations[category] = {}
        master_translations[category].update(terms)
    with open(TRANSLATION_MASTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(master_translations, f, ensure_ascii=False, indent=4)
    logger.info(f"Updated master translation file: {TRANSLATION_MASTER_FILE}")

class ApiClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
    async def fetch_json_with_retries(self, url: str, params: Optional[Dict] = None, retries: int = 3, delay: int = 2) -> Optional[Dict]:
        last_exception = None
        for attempt in range(retries):
            try:
                response = await self.client.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code in [403, 407, 400]:
                    logger.error(f"Critical API Error for {e.request.url}: Status {e.response.status_code}. Aborting retries.")
                    last_exception = e
                    break
                last_exception = e
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Network error on attempt {attempt+1}/{retries} for {url}: {e}")
                last_exception = e
            if attempt < retries - 1:
                await asyncio.sleep(delay * (2 ** attempt))
        return None

class TranslationManager:
    def __init__(self, translation_maps: Dict[str, Dict]):
        self.translation_maps = translation_maps
        # This dictionary holds only the NEW terms found during this run.
        self.new_translations = {key: {} for key in self.translation_maps.keys()}

    def smart_translate(self, category: str, term: Optional[str]) -> Optional[str]:
        """
        Hybrid translation: Checks local cache first, then falls back to Google Translate API.
        """
        if not term:
            return None
        
        # 1. Check local, pre-populated dictionary first for instant speed.
        if term in self.translation_maps.get(category, {}):
            return self.translation_maps[category][term]
        
        # 2. If not found, fallback to Google Translate.
        try:
            # This is a network call and will be slower.
            translated_term = GoogleTranslator(source='ko', target='en').translate(term)
            if translated_term:
                logger.info(f"Google Translated '{term}' -> '{translated_term}' in category '{category}'")
                # 3a. Cache in memory for the rest of this run.
                self.translation_maps.setdefault(category, {})[term] = translated_term
                # 3b. Add to our 'new_translations' dict to be saved to file later.
                self.new_translations.setdefault(category, {})[term] = translated_term
                return translated_term
        except Exception as e:
            logger.warning(f"Google Translate failed for term '{term}': {e}. Returning original.")
            
        # 4. If all else fails, return the original Korean term.
        return term

class EurExchangeRateCache:
    def get_rate(self) -> float: return 0.00063

class StatusManager:
    """
    Manages the status of the enrichment process by writing it to a JSON file.
    The Discord bot will read this file to report progress.
    """
    def __init__(self):
        self.status_file = ENRICHMENT_STATUS_FILE
        self.start_time = time.time()
        self.last_update_time = 0

    def _write_status(self, data: dict):
        """Atomically writes the status dictionary to the file."""
        temp_file = self.status_file + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        os.replace(temp_file, self.status_file)

    def initialize(self, total: int):
        status_data = {
            "phase": "Enrichment",
            "status": "Initializing",
            "processed": 0, "total": total, "failed": 0, "partial_counts": {},
            "progress": "0.0%", "speed": "N/A", "eta": "N/A"
        }
        self._write_status(status_data)

    def update_enrich_progress(self, processed: int, total: int, failed: int, partial_counts: Dict):
        now = time.time()
        total_complete = processed + sum(partial_counts.values())
        if now - self.last_update_time < 5 and total_complete < total:
            return
            
        elapsed = now - self.start_time
        speed = total_complete / elapsed if elapsed > 0 else 0
        progress = (total_complete / total * 100) if total > 0 else 0
        eta = f"{int((total - total_complete) / speed // 3600)}h {int(((total - total_complete) / speed % 3600) // 60)}m" if speed > 0 else "N/A"
        
        status_data = {
            "phase": "Enrichment",
            "status": "Running",
            "processed": processed,
            "total": total,
            "failed": failed,
            "partial_counts": partial_counts,
            "progress": f"{progress:.1f}%",
            "speed": f"{speed:.1f} cars/sec",
            "eta": eta
        }
        self._write_status(status_data)
        self.last_update_time = now

    def send_final_message(self, processed: int, failed: int, partial_counts: Dict, status: str):
        elapsed = time.time() - self.start_time
        duration = f"{int(elapsed // 3600)}h {int((elapsed % 3600) // 60)}m"
        final_status = {
            "phase": "Enrichment",
            "status": status.capitalize(),
            "processed": processed,
            "failed": failed,
            "partial_counts": partial_counts,
            "duration": duration
        }
        self._write_status(final_status)
        logger.info(f"Final enrichment status written to file: {status}")