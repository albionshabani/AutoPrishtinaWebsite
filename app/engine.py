# FILE: EncarScraper/app/engine.py
# FINAL, DEFINITIVE AND COMPLETE VERSION 2.1

import os, json, logging, asyncio, httpx, pandas as pd, re, math, random
from datetime import datetime
from typing import Optional, List, Dict, Any, Set, Tuple
from sqlalchemy import create_engine
from tqdm import tqdm

from .data_models import CarData
from .services import ApiClient, TranslationManager, EurExchangeRateCache, StatusManager, save_new_translations_to_master_file
from .config import *

logger = logging.getLogger("encar_engine")

class Scraper:
    def __init__(self, client: ApiClient, translator: TranslationManager, cache: EurExchangeRateCache):
        self.client = client; self.translator = translator; self.cache = cache
        self.db_engine = create_engine(f'sqlite:///{DB_FILE}') if USE_SQLITE else None
        self.status_manager = StatusManager(DISCORD_WEBHOOK_URL); self.run_status = "running"
        self.eur_rate = self.cache.get_rate()
        
        enrich_headers = { "User-Agent": "Mozilla/5.0...", "Accept": "*/*", "Origin": "https://fem.encar.com", "Referer": "https://fem.encar.com/"}
        self.enrich_client = httpx.AsyncClient(headers=enrich_headers, timeout=30, follow_redirects=True)

    def _load_processed_ids(self) -> Set[str]:
        logger.info("Loading checkpoints for all previously processed IDs...")
        return (self._load_tracker_file(SUCCESS_IDS_FILE) | self._load_tracker_file(FAILED_IDS_FILE) |
                self._load_tracker_file(PARTIAL_NO_INSPECTION_FILE) | self._load_tracker_file(PARTIAL_NO_RECORD_FILE) |
                self._load_tracker_file(PARTIAL_NO_DIAGNOSIS_FILE))

    def _load_tracker_file(self, filepath: str) -> Set[str]:
        if not os.path.exists(filepath): return set()
        with open(filepath, 'r') as f: return {line.strip() for line in f if line.strip()}

    def _append_to_tracker_file(self, filepath: str, ids: Set[str]):
        if ids:
            with open(filepath, 'a') as f:
                for item_id in ids: f.write(f"{item_id}\n")

    async def _parallel_discover_in_range(self, mileage_query: str) -> List[Dict]:
        initial_params = {'count': 'true', 'q': mileage_query, 'sr': '|ModifiedDate|0|1'}
        initial_data = await self.client.fetch_json_with_retries(BASE_URL, params=initial_params)
        if not initial_data or not initial_data.get("Count"): return []
        num_pages = math.ceil(initial_data["Count"] / BATCH_SIZE)
        tasks = [self.client.fetch_json_with_retries(BASE_URL, params={'count': 'true', 'q': mileage_query, 'sr': f'|ModifiedDate|{i*BATCH_SIZE}|{BATCH_SIZE}'}) for i in range(num_pages)]
        return [car for page in await asyncio.gather(*tasks) if page and page.get("SearchResults") for car in page["SearchResults"]]

    async def _discover_all_cars(self) -> List[Dict]:
        all_cars, pbar = [], tqdm(range(0, MAX_MILEAGE, MILEAGE_STEP), desc="Phase 1: Discovering")
        for i, start_mileage in enumerate(pbar):
            if os.path.exists(STOP_SIGNAL_FILE): break
            end = start_mileage + MILEAGE_STEP
            pbar.set_description(f"Discovering {start_mileage:,}-{end:,} km")
            query = f"(And.Hidden.N._.CarType.Y._.Mileage.range(..{end}).)" if start_mileage == 0 else f"(And.Hidden.N._.CarType.Y._.Mileage.range({start_mileage}..{end}).)"
            chunk_results = await self._parallel_discover_in_range(query)
            for car_data in chunk_results:
                if listing_id := car_data.get("Id"):
                    car_data['Enrichment ID'] = listing_id; all_cars.append(car_data)
        unique_ids = {car['Id'] for car in all_cars};
        with open(ALL_LIVE_IDS_FILE, 'w') as f: f.write('\n'.join(unique_ids))
        logger.info(f"Discovery complete. Found {len(unique_ids):,} unique listings.")
        return all_cars

    async def _enrich_car(self, base_car: Dict) -> Tuple[str, Set[str], Dict]:
        listing_id, enrich_id = base_car.get("Id"), base_car.get("Enrichment ID")
        if not (listing_id and enrich_id): return 'failed', set(), {'ID': listing_id or 'Unknown'}
        
        api = ApiClient(self.enrich_client)
        tasks = [
            api.fetch_json_with_retries(f"https://api.encar.com/v1/readside/inspection/vehicle/{enrich_id}"),
            api.fetch_json_with_retries(f"https://api.encar.com/v1/readside/record/vehicle/{enrich_id}/open"),
            api.fetch_json_with_retries(f"https://api.encar.com/v1/readside/diagnosis/vehicle/{enrich_id}")
        ]
        inspection, record, diagnosis = await asyncio.gather(*tasks)
        
        missing = {part for part, data in zip(['no_inspection', 'no_record', 'no_diagnosis'], [inspection, record, diagnosis]) if not data}
        status = 'success' if not missing else 'partial'
        
        def safe_get(d, keys, default=None):
            for key in keys:
                if not isinstance(d, dict): return default
                d = d.get(key)
            return d

        record_data = record or {}; inspection_data = inspection or {}; diagnosis_data = diagnosis or {}
        
        badge_main = base_car.get('Badge', ''); badge_detail = base_car.get('BadgeDetail', '')
        full_badge = f"{badge_main} {badge_detail}" if badge_detail and badge_detail != '(세부등급 없음)' else badge_main
        
        powerpack = base_car.get('Powerpack', ''); adwords = base_car.get('AdWords', '')
        seller_comment = f"{powerpack} | {adwords}" if powerpack and adwords else powerpack or adwords

        accident_cost_krw = record_data.get('myAccidentCost', 0) + record_data.get('otherAccidentCost', 0)
        
        # CORRECTED: Fallback logic for displacement
        displacement = record_data.get('displacement') or safe_get(inspection_data, ['master', 'detail', 'displacement'])
        
        car_dict = {
            'ID': listing_id, 'Enrichment_ID': enrich_id, 'Image_URL': f"https://ci.encar.com{base_car.get('Photo', '')}001.jpg",
            'Year': base_car.get('FormYear'), 'Brand': self.translator.smart_translate('Brand', base_car.get('Manufacturer')),
            'Model': self.translator.smart_translate('Model', base_car.get('Model')), 'Badge': self.translator.smart_translate('Badge', full_badge),
            'Mileage_km': base_car.get('Mileage'), 'Price_KRW': int(base_car.get('Price', 0) * 10000), 'Price_EUR': int(base_car.get('Price', 0) * 10000 * self.eur_rate),
            'Fuel': self.translator.smart_translate('Fuel', base_car.get('FuelType')),
            'Transmission': self.translator.smart_translate('Transmission', base_car.get('Transmission')),
            'First_Registration_Date': record_data.get('firstDate'),
            'Displacement_cc': displacement,
            'Usage_Type': "Rental" if record_data.get('loan') else "Business" if record_data.get('business') else "Personal",
            'Owner_Changes': record_data.get('ownerChangeCnt'), 'Owner_Change_History': ", ".join(record_data.get('ownerChanges', []) or []),
            'Accident_Count': record_data.get('accidentCnt'), 'Total_Accident_Cost_KRW': accident_cost_krw, 'Total_Accident_Cost_EUR': int(accident_cost_krw * self.eur_rate),
            'Accident_History': "; ".join([f"Date: {a.get('date', 'N/A')}" for a in record_data.get('accidents', []) or []]),
            'Diagnosis_Result': self.translator.smart_translate('Diagnosis Result', safe_get(next((item for item in diagnosis_data.get("items", []) if item.get('code') == '006039'), {}), ['result'])),
            'Diagnosis_Items': ", ".join([item.get('name', 'N/A') for item in (diagnosis_data.get("items", []) or [])]),
            'VIN': safe_get(inspection_data, ["master", "detail", "vin"]), 'Motor_Type': safe_get(inspection_data, ["master", "detail", "motorType"]),
            'Sale_Type': self.translator.smart_translate('Sale Type', base_car.get('SellType')),
            'Seller_Comment': self.translator.smart_translate('Seller Comment', seller_comment),
            'Total_Loss_Count': record_data.get('totalLossCnt'), 'Flood_Count': record_data.get('floodTotalLossCnt'),
            'Theft_History_Count': record_data.get('robberCnt'), 'Has_Tuning': safe_get(inspection_data, ['master', 'detail', 'tuning']),
            'Has_Open_Recall': safe_get(inspection_data, ['master', 'detail', 'recall']),
        }
        try: return status, missing, CarData(**car_dict).model_dump(by_alias=True)
        except Exception as e:
            logger.error(f"Pydantic validation for {listing_id} failed: {e}: {car_dict}"); return 'failed', set(), {'ID': listing_id}

    def save_to_db(self, data: List[Dict]):
        if not (USE_SQLITE and data): return
        df = pd.DataFrame(data); ordered_columns = [f.alias or n for n, f in CarData.model_fields.items()]; df = df.reindex(columns=ordered_columns)
        try: df.to_sql('cars', self.db_engine, if_exists='append', index=False)
        except Exception as e: logger.error(f"DB save failed: {e}")

    async def shutdown(self):
        if self.enrich_client and not self.enrich_client.is_closed: await self.enrich_client.aclose()
        logger.info("HTTP clients closed.")

    def export_results(self):
        if not USE_SQLITE: logger.warning("SQLite is disabled, cannot export."); return
        logger.info("Exporting final results from the database...")
        try:
            with self.db_engine.connect() as connection:
                if not self.db_engine.dialect.has_table(connection, "cars"): return logger.warning("DB table not found.")
                df = pd.read_sql_table('cars', connection);
                if df.empty: return logger.warning("DB is empty.")
                logger.info(f"Exporting {len(df)} final records...")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S"); base_filename = DB_FILE.replace('.db', '')
                if EXPORT_CSV: df.to_csv(f"{base_filename}_{timestamp}.csv", index=False, encoding='utf-8-sig')
                if EXPORT_JSON: df.to_json(f"{base_filename}_{timestamp}.json", orient='records', indent=4)
                if EXPORT_EXCEL: df.to_excel(f"{base_filename}_{timestamp}.xlsx", index=False, sheet_name='Encar_Listings')
                logger.info("✅ All final results have been exported.")
        except Exception as e: logger.error(f"Failed to export final results: {e}", exc_info=True)

    async def run(self):
        self.run_status = "running"; successful, failed_count = 0, 0; partial_counts = {'no_inspection': 0, 'no_record': 0, 'no_diagnosis': 0}
        try:
            self.status_manager.send_or_edit_message("🔵 **Scraper Initializing...**"); processed_ids = self._load_processed_ids()
            all_cars_data = await self._discover_all_cars()
            cars_to_process = [car for car in all_cars_data if str(car.get("Id")) not in processed_ids]
            if SAMPLE_MODE_COUNT > 0:
                logger.info(f"--- SAMPLE MODE: Processing a random sample of {SAMPLE_MODE_COUNT} cars. ---")
                random.shuffle(cars_to_process); cars_to_process = cars_to_process[:SAMPLE_MODE_COUNT]
            total_to_process = len(cars_to_process)
            if not total_to_process: self.run_status = "complete"; logger.info("No new cars to process."); return

            pbar = tqdm(total=total_to_process, desc="Phase 2: Enriching New Cars")
            for i in range(0, total_to_process, SAVE_PROGRESS_EVERY):
                if os.path.exists(STOP_SIGNAL_FILE): self.run_status = "stopped"; break
                chunk_to_process = cars_to_process[i:i + SAVE_PROGRESS_EVERY]
                semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
                async def worker(base_car_dict: Dict):
                    async with semaphore: return await self._enrich_car(base_car_dict)
                results = await asyncio.gather(*[worker(car) for car in chunk_to_process])
                
                valid_results = [res[2] for res in results if res and res[0] in ['success', 'partial']];
                if valid_results: self.save_to_db(valid_results)
                
                self._append_to_tracker_file(SUCCESS_IDS_FILE, {res[2]['ID'] for res in results if res and res[0] == 'success'})
                self._append_to_tracker_file(FAILED_IDS_FILE, {res[2]['ID'] for res in results if res and res[0] == 'failed'})
                
                partial_files = {'no_inspection': PARTIAL_NO_INSPECTION_FILE, 'no_record': PARTIAL_NO_RECORD_FILE, 'no_diagnosis': PARTIAL_NO_DIAGNOSIS_FILE}
                for part, filepath in partial_files.items():
                    ids = {res[2]['ID'] for res in results if res and part in res[1]}; self._append_to_tracker_file(filepath, ids); partial_counts[part] += len(ids)
                
                successful += sum(1 for r in results if r and r[0] == 'success'); failed_count += sum(1 for r in results if r and r[0] == 'failed')
                pbar.update(len(chunk_to_process)); self.status_manager.update_enrich_progress(successful, total_to_process, failed_count, partial_counts)

            pbar.close()
            if self.run_status == "running": self.run_status = "complete"
        except Exception as e: logger.critical(f"Fatal error: {e}", exc_info=True); self.run_status = "crashed"
        finally:
            await self.shutdown()
            if self.translator.new_translations and any(self.translator.new_translations.values()): save_new_translations_to_master_file(self.translator.new_translations)
            if self.run_status in ["complete", "stopped"]: self.export_results()
            self.status_manager.send_final_message(successful, failed_count, partial_counts, self.run_status)