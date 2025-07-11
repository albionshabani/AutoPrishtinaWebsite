# FILE: EncarScraper/app/discover.py
# FINAL CORRECTED VERSION (v4.4 - Capturing Photo Path at Discovery)

import asyncio
import httpx
import logging
import os
import sys
import json
import math
import random
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

from .config import *
from .services import ApiClient

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s [%(name)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("discover")

async def discover_bracket_concurrently(client: ApiClient, mileage_query: str) -> list | None:
    """
    Performs a highly concurrent, but controlled, multi-page discovery for a single mileage bracket.
    """
    initial_params = {'count': 'true', 'q': mileage_query, 'sr': f'|MobileModifiedDate|0|{BATCH_SIZE}'}
    initial_page_data = await client.fetch_json_with_retries(BASE_URL, params=initial_params)

    if initial_page_data is None or "Count" not in initial_page_data:
        logger.error(f"Failed to get initial page/count for query: {mileage_query}. Skipping bracket.")
        return None

    total_count = initial_page_data.get("Count", 0)
    if total_count == 0: return []
        
    first_page_results = initial_page_data.get("SearchResults", [])
    all_results = list(first_page_results)

    num_pages = math.ceil(total_count / BATCH_SIZE)
    if num_pages <= 1: return all_results

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    async def fetch_page(params):
        async with semaphore:
            await asyncio.sleep(random.uniform(0.05, 0.25))
            return await client.fetch_json_with_retries(BASE_URL, params=params)

    tasks = []
    for i in range(1, num_pages):
        offset = i * BATCH_SIZE
        params = {'count': 'true', 'q': mileage_query, 'sr': f'|MobileModifiedDate|{offset}|{BATCH_SIZE}'}
        tasks.append(fetch_page(params))
        
    logger.info(f"  [*] Fetching {len(tasks)} more pages for this bracket with a concurrency limit of {CONCURRENT_REQUESTS}...")
    page_results = await asyncio.gather(*tasks)
    
    for page in page_results:
        if page and page.get("SearchResults"):
            all_results.extend(page["SearchResults"])
            
    return all_results


async def main():
    logger.info("--- 🔵 Discovery Process Started ---")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(DISCOVERY_PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    all_cars = []
    try:
        limits = httpx.Limits(max_connections=CONCURRENT_REQUESTS + 5, max_keepalive_connections=20)
        async with httpx.AsyncClient(headers=HEADERS, timeout=45, follow_redirects=True, limits=limits) as http_client:
            client = ApiClient(http_client)
            pbar = tqdm(range(0, MAX_MILEAGE, MILEAGE_STEP), desc="Phase 1: Discovering Listings")
            
            for start_mileage in pbar:
                if os.path.exists(STOP_SIGNAL_FILE):
                    logger.warning("Stop signal detected, aborting discovery loop.")
                    break
                    
                end = start_mileage + MILEAGE_STEP
                pbar.set_description(f"Discovering {start_mileage:,}-{end:,} km")
                
                query = f"(And.Hidden.N._.CarType.A._.Mileage.range(..{end}).)" if start_mileage == 0 else f"(And.Hidden.N._.CarType.A._.Mileage.range({start_mileage}..{end}).)"
                
                chunk_results = await discover_bracket_concurrently(client, query)
                
                if chunk_results is not None:
                    logger.info(f"  [+] Discovered {len(chunk_results):,} listings in range {start_mileage:,}-{end:,} km.")
                    for car_data in chunk_results:
                         if listing_id := car_data.get("Id"):
                            # --- THIS IS THE FIX ---
                            # We are now saving both the ID and the reliable Photo path.
                            all_cars.append({
                                "ID": listing_id,
                                "Photo": car_data.get("Photo") 
                            })
                else:
                    logger.error(f"  [!] Failed to process mileage range {start_mileage:,}-{end:,} km. Skipping to next range.")

        logger.info(f"Discovery complete. Found a grand total of {len(all_cars):,} listings.")
        
        with open(DISCOVERED_LISTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_cars, f)
        logger.info(f"✅ Successfully saved {len(all_cars)} listings to {DISCOVERED_LISTINGS_FILE}")

    except Exception as e:
        logger.critical(f"A fatal unhandled error occurred in main discovery loop: {e}", exc_info=True)
    finally:
        if os.path.exists(DISCOVERY_PID_FILE):
            os.remove(DISCOVERY_PID_FILE)
        logger.info("--- 🔵 Discovery Process Finished ---")

if __name__ == "__main__":
    asyncio.run(main())