# FILE: EncarScraper/app/engine.py
# FINAL CORRECTED VERSION (v4.4 - Using Discovery Photo Path)

import os, json, logging, asyncio, httpx, pandas as pd, re
from datetime import datetime
from typing import Optional, List, Dict, Any, Set, Tuple
from sqlalchemy import create_engine
from tqdm import tqdm

from .data_models import CarData
from .services import ApiClient, TranslationManager, EurExchangeRateCache, StatusManager, save_new_translations_to_master_file
from .config import *

logger = logging.getLogger("enrich_engine")

class EnrichmentEngine:
    def __init__(self, translator: TranslationManager, cache: EurExchangeRateCache, status_manager: StatusManager):
        self.translator = translator
        self.cache = cache
        self.status_manager = status_manager
        self.db_engine = create_engine(f'sqlite:///{DB_FILE}') if USE_SQLITE else None
        self.run_status = "running"
        self.eur_rate = self.cache.get_rate()
        self.options_map = {}
        
        enrich_headers = { "User-Agent": "Mozilla/5.0...", "Accept": "*/*", "Origin": "https://fem.encar.com", "Referer": "https://fem.encar.com/"}
        self.enrich_client = httpx.AsyncClient(headers=enrich_headers, timeout=30, follow_redirects=True, limits=httpx.Limits(max_connections=CONCURRENT_REQUESTS+10))

    async def _cache_standard_options(self):
        logger.info("Caching and pre-translating standard options dictionary...")
        api = ApiClient(self.enrich_client)
        url = "https://api.encar.com/v1/readside/vehicles/car/options/standard"
        options_data = await api.fetch_json_with_retries(url)
        
        if not (options_data and "options" in options_data):
            logger.error("Could not fetch the standard options dictionary. Option list will be codes only.")
            return

        all_options = []
        for option in options_data["options"]:
            all_options.append(option)
            if sub_options := option.get("subOptions"):
                all_options.extend(sub_options)
        
        for option in all_options:
            if code := option.get("optionCd"):
                korean_name = option.get("groupOptionName") or option.get("optionName")
                if korean_name:
                    english_name = self.translator.smart_translate('Options', korean_name)
                    self.options_map[code] = english_name
        
        logger.info(f"✅ Successfully cached and pre-translated {len(self.options_map)} options.")

    def _load_processed_ids(self) -> Set[str]:
        logger.info("Loading checkpoints for all previously processed IDs...")
        return (self._load_tracker_file(SUCCESS_IDS_FILE) | self._load_tracker_file(FAILED_IDS_FILE))

    def _load_tracker_file(self, filepath: str) -> Set[str]:
        if not os.path.exists(filepath): return set()
        with open(filepath, 'r') as f: return {line.strip() for line in f if line.strip()}

    def _append_to_tracker_file(self, filepath: str, ids: Set[str]):
        if ids:
            with open(filepath, 'a') as f:
                for item_id in ids: f.write(f"{item_id}\n")

    def _calculate_flags(self, car_dict: Dict) -> Dict:
        flags = {}
        current_year = datetime.now().year
        try:
            year = int(car_dict.get('Year'))
            mileage = int(car_dict.get('Mileage_km'))
            age = current_year - year if current_year > year else 1
            flags['isLowMileage'] = (mileage / age) < 15000 if age > 0 else mileage < 15000
        except (TypeError, ValueError, ZeroDivisionError): flags['isLowMileage'] = None
        if (owner_changes := car_dict.get('Owner_Changes')) is not None: flags['isFirstOwner'] = (owner_changes == 0)
        try:
            flags['isWellMaintained'] = ((car_dict.get('Total_Loss_Count', 0) or 0) == 0 and (car_dict.get('Flood_Count', 0) or 0) == 0 and (car_dict.get('Accident_Count', 0) or 0) == 0)
        except (TypeError, ValueError): flags['isWellMaintained'] = None
        fuel, displacement = car_dict.get('Fuel'), car_dict.get('Displacement_cc')
        if fuel in ['Electric', 'Hybrid']: flags['isFuelEfficient'] = True
        elif fuel in ['Gasoline', 'LPG', 'Diesel'] and displacement is not None:
            try: flags['isFuelEfficient'] = int(displacement) < 1600
            except (ValueError, TypeError): flags['isFuelEfficient'] = None
        options_str = car_dict.get('Options', '').lower()
        if 'sunroof' in options_str and 'navigation' in options_str and ('leather' in options_str or 'alcantara' in options_str) and 'smart key' in options_str: flags['isFullyLoaded'] = True
        return flags

    async def _enrich_car(self, base_car: Dict) -> Tuple[str, Dict]:
        listing_id = base_car.get("ID")
        photo_path = base_car.get("Photo")
        
        api = ApiClient(self.enrich_client)
        
        def safe_get(d, keys, default=None):
            for key in keys:
                if not isinstance(d, dict): return default
                d = d.get(key)
            return d

        vehicle_url = f"https://api.encar.com/v1/readside/vehicle/{listing_id}?include=ADVERTISEMENT,CATEGORY,OPTIONS,SPEC,VIEW,VIN"
        record_url = f"https://api.encar.com/v1/readside/record/vehicle/{listing_id}/open"
        
        vehicle_data, record_data = await asyncio.gather(
            api.fetch_json_with_retries(vehicle_url),
            api.fetch_json_with_retries(record_url)
        )

        if not vehicle_data:
            return 'failed', {'ID': listing_id}

        record = record_data or {}
        
        grade_name = safe_get(vehicle_data, ['category', 'gradeName'], '')
        grade_detail = safe_get(vehicle_data, ['category', 'gradeDetailName'], '')
        full_badge = f"{grade_name} {grade_detail}".strip()

        option_codes = safe_get(vehicle_data, ['options', 'standard'], [])
        option_names = [self.options_map.get(code, f"Code_{code}") for code in option_codes]
        
        accident_cost_krw = (record.get('myAccidentCost', 0) or 0) + (record.get('otherAccidentCost', 0) or 0)
        
        image_url = f"https://ci.encar.com{photo_path}" if photo_path else None

        car_dict = {
            'ID': listing_id, 'VIN': safe_get(vehicle_data, ['vin']), 'Year': safe_get(vehicle_data, ['category', 'formYear']), 'Brand': self.translator.smart_translate('Brand', safe_get(vehicle_data, ['category', 'manufacturerName'])), 'Model': self.translator.smart_translate('Model', safe_get(vehicle_data, ['category', 'modelName'])), 'Badge': self.translator.smart_translate('Badge', full_badge), 'Body_Type': self.translator.smart_translate('Body Type', safe_get(vehicle_data, ['spec', 'bodyName'])), 'Mileage_km': safe_get(vehicle_data, ['spec', 'mileage']), 'Price_KRW': int(safe_get(vehicle_data, ['advertisement', 'price'], 0) * 10000), 'Price_EUR': int(safe_get(vehicle_data, ['advertisement', 'price'], 0) * 10000 * self.eur_rate), 'Fuel': self.translator.smart_translate('Fuel', safe_get(vehicle_data, ['spec', 'fuelName'])), 'Transmission': self.translator.smart_translate('Transmission', safe_get(vehicle_data, ['spec', 'transmissionName'])), 'Displacement_cc': safe_get(vehicle_data, ['spec', 'displacement']), 'Color': self.translator.smart_translate('Color', safe_get(vehicle_data, ['spec', 'colorName'])), 'Image_URL': image_url, 'View_Count': safe_get(vehicle_data, ['manage', 'viewCount']), 'First_Registration_Date': record.get('firstDate'), 'Owner_Changes': record.get('ownerChangeCnt'), 'Owner_Change_History': ", ".join(record.get('ownerChanges', []) or []), 'Accident_Count': (record.get('myAccidentCnt', 0) or 0) + (record.get('otherAccidentCnt', 0) or 0), 'Total_Accident_Cost_KRW': accident_cost_krw, 'Total_Accident_Cost_EUR': int(accident_cost_krw * self.eur_rate), 'Accident_History': "; ".join([f"Date: {a.get('date', 'N/A')}" for a in record.get('accidents', []) or []]), 'Total_Loss_Count': record.get('totalLossCnt'), 'Flood_Count': record.get('floodTotalLossCnt'), 'Theft_History_Count': record.get('robberCnt'), 'Usage_Type': "Rental" if record.get('loan') else "Business" if record.get('business') else "Personal", 'Options': ", ".join(sorted(option_names)),
        }
        
        car_dict.update(self._calculate_flags(car_dict))
        
        try:
            return 'success', CarData(**car_dict).model_dump(by_alias=True)
        except Exception as e:
            logger.error(f"Pydantic validation for {listing_id} failed: {e}: {car_dict}")
            return 'failed', {'ID': listing_id}
    
    def save_to_db(self, data: List[Dict]):
        if not (USE_SQLITE and data): return
        df = pd.DataFrame(data)
        if df.empty: return
        ordered_columns = [f.alias or n for n, f in CarData.model_fields.items()]
        df = df.reindex(columns=ordered_columns)
        try:
            df.to_sql('cars', self.db_engine, if_exists='append', index=False)
        except Exception as e:
            logger.error(f"DB save failed: {e}")

    async def shutdown(self):
        if self.enrich_client and not self.enrich_client.is_closed: await self.enrich_client.aclose()
        logger.info("HTTP clients closed.")

    def export_results(self):
        if not USE_SQLITE: logger.warning("SQLite is disabled, cannot export."); return
        logger.info("Exporting final results from the database...")
        try:
            with self.db_engine.connect() as connection:
                if not self.db_engine.dialect.has_table(connection, "cars"):
                    logger.warning("DB table 'cars' not found for export.")
                    return
                df = pd.read_sql_table('cars', connection)
                if df.empty:
                    logger.warning("DB table is empty, nothing to export.")
                    return
                logger.info(f"Exporting {len(df)} final records...")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_filename = DB_FILE.replace('.db', '')
                if EXPORT_CSV: df.to_csv(f"{base_filename}_{timestamp}.csv", index=False, encoding='utf-8-sig')
                if EXPORT_JSON: df.to_json(f"{base_filename}_{timestamp}.json", orient='records', indent=4)
                if EXPORT_EXCEL: df.to_excel(f"{base_filename}_{timestamp}.xlsx", index=False, sheet_name='Encar_Listings')
                logger.info("✅ All final results have been exported.")
        except Exception as e:
            logger.error(f"Failed to export final results: {e}", exc_info=True)

    async def run_enrichment(self, all_discovered_cars: list):
        await self._cache_standard_options()
        
        self.run_status = "running"
        successful_count, failed_count = 0, 0
        
        try:
            processed_ids = self._load_processed_ids()
            cars_to_process = [car for car in all_discovered_cars if str(car.get("ID")) not in processed_ids]
            
            if SAMPLE_MODE_COUNT > 0:
                logger.info(f"--- SAMPLE MODE: Processing a random sample of {SAMPLE_MODE_COUNT} cars. ---")
                cars_to_process = cars_to_process[:SAMPLE_MODE_COUNT]
            
            total_to_process = len(cars_to_process)
            self.status_manager.initialize(total_to_process)

            if not total_to_process:
                self.run_status = "complete"
                self.export_results()
                self.status_manager.send_final_message(0, 0, {}, "complete")
                return

            pbar = tqdm(total=total_to_process, desc="Phase 2: Enriching New Cars")
            for i in range(0, total_to_process, SAVE_PROGRESS_EVERY):
                if os.path.exists(STOP_SIGNAL_FILE):
                    self.run_status = "stopped"; break
                
                chunk_to_process = cars_to_process[i:i + SAVE_PROGRESS_EVERY]
                semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
                async def worker(base_car_dict: Dict):
                    async with semaphore: return await self._enrich_car(base_car_dict)
                
                results = await asyncio.gather(*[worker(car) for car in chunk_to_process])
                
                success_results = [res[1] for res in results if res and res[0] == 'success']
                failed_ids = {res[1]['ID'] for res in results if res and res[0] == 'failed'}
                
                if success_results:
                    self.save_to_db(success_results)
                    self._append_to_tracker_file(SUCCESS_IDS_FILE, {res['ID'] for res in success_results if 'ID' in res})
                if failed_ids:
                    self._append_to_tracker_file(FAILED_IDS_FILE, failed_ids)
                
                successful_count += len(success_results)
                failed_count += len(failed_ids)
                pbar.update(len(chunk_to_process))
                self.status_manager.update_enrich_progress(successful_count, total_to_process, failed_count, {})

            pbar.close()
            if self.run_status == "running": self.run_status = "complete"
        except Exception as e:
            logger.critical(f"Fatal error during enrichment: {e}", exc_info=True)
            self.run_status = "crashed"
        finally:
            await self.shutdown()
            if self.translator.new_translations and any(self.translator.new_translations.values()):
                save_new_translations_to_master_file(self.translator.new_translations)
            
            if self.run_status in ["complete", "stopped"]:
                self.export_results()
            
            self.status_manager.send_final_message(successful_count, failed_count, {}, self.run_status)