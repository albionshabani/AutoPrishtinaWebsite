# FILE: EncarScraper/app/services.py

import httpx
import asyncio
import logging
import time
import os
import json
from typing import Optional, Dict

from deep_translator import GoogleTranslator
from .config import DATA_DIR, TRANSLATION_MASTER_FILE, DISCORD_WEBHOOK_URL, DISCORD_MESSAGE_ID_FILE

logger = logging.getLogger("encar_services")

# (The rest of the file is the same as the previous correct version)
def save_new_translations_to_master_file(new_translations: dict):
    if not any(new_translations.values()): return
    master_translations = {}
    if os.path.exists(TRANSLATION_MASTER_FILE):
        with open(TRANSLATION_MASTER_FILE, 'r', encoding='utf-8') as f: master_translations = json.load(f)
    for category, terms in new_translations.items():
        if category not in master_translations: master_translations[category] = {}
        master_translations[category].update(terms)
    with open(TRANSLATION_MASTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(master_translations, f, ensure_ascii=False, indent=4)
    logger.info(f"Updated master translation file: {TRANSLATION_MASTER_FILE}")

class ApiClient:
    def __init__(self, client: httpx.AsyncClient): self.client = client
    async def fetch_json_with_retries(self, url: str, params: Optional[Dict] = None, retries: int = 3, delay: int = 2) -> Optional[Dict]:
        last_exception = None
        for attempt in range(retries):
            try:
                response = await self.client.get(url, params=params, timeout=30); response.raise_for_status(); return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code in [403, 407]: logger.error(f"Critical API Error for {e.request.url}: Status {e.response.status_code}.")
                last_exception = e; break
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Network error on attempt {attempt+1}/{retries} for {url}: {e}"); last_exception = e
            if attempt < retries - 1: await asyncio.sleep(delay * (2 ** attempt))
        return None

class TranslationManager:
    def __init__(self, translation_maps: Dict[str, Dict]):
        self.translation_maps = translation_maps; self.new_translations = {key: {} for key in self.translation_maps.keys()}
    def smart_translate(self, category: str, term: Optional[str]) -> Optional[str]:
        if not term: return None
        if term in self.translation_maps.get(category, {}): return self.translation_maps[category][term]
        try:
            translated_term = GoogleTranslator(source='ko', target='en').translate(term)
            if translated_term:
                self.new_translations[category][term] = translated_term; self.translation_maps[category][term] = translated_term
                return translated_term
        except Exception: pass
        return term

class EurExchangeRateCache:
    def get_rate(self) -> float: return 0.00063

class StatusManager:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url; self.message_id = self._load_message_id(); self.start_time = time.time(); self.last_update_time = 0; self.client = httpx.Client()
    def _load_message_id(self) -> Optional[str]:
        if os.path.exists(DISCORD_MESSAGE_ID_FILE):
            with open(DISCORD_MESSAGE_ID_FILE, 'r') as f: return f.read().strip()
    def _save_message_id(self, message_id: str):
        with open(DISCORD_MESSAGE_ID_FILE, 'w') as f: f.write(message_id)
    def send_or_edit_message(self, content: str, is_final: bool = False):
        if not self.webhook_url or "YOUR_WEBHOOK" in self.webhook_url: return
        url = f"{self.webhook_url}/messages/{self.message_id}" if self.message_id else f"{self.webhook_url}?wait=true"
        method = 'PATCH' if self.message_id else 'POST'
        try:
            res = self.client.request(method, url, json={'content': content}, timeout=15); res.raise_for_status()
            if method == 'POST': self.message_id = res.json()['id']; self._save_message_id(self.message_id)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: self.message_id = None; self.send_or_edit_message(content)
            else: logger.error(f"Discord webhook error: {e.response.status_code} - {e.response.text}")

    def update_discovery_progress(self, current_chunk: int, total_chunks: int, found_so_far: int):
        now = time.time()
        if now - self.last_update_time < 2 and current_chunk < total_chunks: return
        progress = (current_chunk / total_chunks * 100) if total_chunks > 0 else 0
        msg = (f"⚙️ **Phase 1: Discovering...**\n```"
               f"Scanning Mileage Range: {current_chunk} / {total_chunks} ({progress:.1f}%)\n"
               f"Listings Found So Far:  {found_so_far:,}```")
        self.send_or_edit_message(msg); self.last_update_time = now
        
    def update_enrich_progress(self, processed: int, total: int, failed: int, partial_counts: Dict):
        now = time.time()
        total_complete = processed + sum(partial_counts.values())
        if now - self.last_update_time < 5 and total_complete < total: return
        elapsed = now - self.start_time; speed = total_complete / elapsed if elapsed > 0 else 0
        progress = (total_complete / total * 100) if total > 0 else 0
        eta = f"{int((total - total_complete) / speed // 3600)}h {int(((total - total_complete) / speed % 3600) // 60)}m" if speed > 0 else "N/A"
        s = f"S: {processed:,}"; f = f"F: {failed:,}"; ni = f"NI: {partial_counts.get('no_inspection', 0):,}"; nr = f"NR: {partial_counts.get('no_record', 0):,}"; nd = f"ND: {partial_counts.get('no_diagnosis', 0):,}"
        msg = (f"⚙️ **Phase 2: Enriching...**\n```"
               f"Progress: {total_complete:,} / {total:,} ({progress:.1f}%) | Speed: {speed:.1f} cars/sec | ETA: {eta}\n"
               f"--------------------------------------------------\n"
               f"{s} | {f} | {ni} | {nr} | {nd}```")
        self.send_or_edit_message(msg); self.last_update_time = now

    def send_final_message(self, processed: int, failed: int, partial_counts: Dict, status: str):
        emoji, title = {"complete": ("✅", "Run Complete"), "stopped": ("🛑", "Run Stopped"), "crashed": ("💥", "Run Crashed")}.get(status, ("💥", "Run Failed"))
        elapsed = time.time() - self.start_time
        partial_str = "\n".join([f"- No {k.replace('no_', '')}: {v:,}" for k,v in partial_counts.items() if v > 0])
        partial_section = f"\nPartially Processed:\n{partial_str}" if any(partial_counts.values()) else ""
        msg = (f"{emoji} **{title}**\n```"
               f"Successful: {processed:,}\n"
               f"Failed:     {failed:,}{partial_section}\n\n"
               f"Total Duration:  {int(elapsed // 3600)}h {int((elapsed % 3600) // 60)}m```")
        self.send_or_edit_message(msg, is_final=True)
        if os.path.exists(DISCORD_MESSAGE_ID_FILE): os.remove(DISCORD_MESSAGE_ID_FILE)