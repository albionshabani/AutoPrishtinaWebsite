# FILE: EncarScraper/debug_enrich.py
import httpx
import asyncio
import logging
import json

# --- START: Configuration from your project ---
# These are copied here so the script can run by itself.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0, i",
    "TE": "trailers",
}
COOKIE_STRING = "RecentViewAllCar=39628925%2C38508421%2C39356902%2C39772267%2C39628084%2C39766231%2C38518849%2C37923895%2C39437518%2C39834207%2C39451849%2C39707436%2C39497727; RecentViewCar=39628925%2C38508421%2C39356902%2C39772267%2C39628084%2C39766231%2C38518849%2C37923895%2C39437518%2C39834207%2C39451849%2C39707436%2C39497727; RecentViewTruck=; OAX=kkZoKWhZXXYADyGf; _encar_hostname=http://www.encar.com"

ENRICHMENT_HEADERS = HEADERS.copy()
ENRICHMENT_HEADERS.update({
    "Accept": "*/*",
    "Origin": "https://fem.encar.com",
    "Referer": "https://fem.encar.com/",
    "Sec-Fetch-Site": "same-site",
    "cookie": COOKIE_STRING, # Add the cookie string to the headers
})
# --- END: Configuration ---

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

async def fetch_url(client, url):
    """A simple fetcher that returns the JSON or None on error."""
    try:
        response = await client.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"Request to {url} failed with status: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Request to {url} failed with exception: {e}")
        return None

async def debug_id(enrichment_id: str):
    """Runs the three enrichment API calls for a single ID and prints the results."""
    print("\n" + "="*50)
    print(f"--- DEBUGGING ENRICHMENT ID: {enrichment_id} ---")
    print("="*50)

    async with httpx.AsyncClient(headers=ENRICHMENT_HEADERS, follow_redirects=True) as client:
        # Define the three API calls
        inspection_url = f"https://api.encar.com/v1/readside/inspection/vehicle/{enrichment_id}"
        record_url = f"https://api.encar.com/v1/readside/record/vehicle/{enrichment_id}/open"
        diagnosis_url = f"https://api.encar.com/v1/readside/diagnosis/vehicle/{enrichment_id}"

        # Run them all at the same time
        inspection_data, record_data, diagnosis_data = await asyncio.gather(
            fetch_url(client, inspection_url),
            fetch_url(client, record_url),
            fetch_url(client, diagnosis_url)
        )

        # Print the results clearly
        print("\n[1] INSPECTION DATA (/v1/readside/inspection/vehicle/):")
        if inspection_data is None:
            print("--> RESULT: FAILED (Returned None)")
        else:
            print("--> RESULT: SUCCESS")
            print(json.dumps(inspection_data, indent=2, ensure_ascii=False))

        print("\n[2] RECORD DATA (/v1/readside/record/vehicle/.../open):")
        if record_data is None:
            print("--> RESULT: FAILED (Returned None)")
        else:
            print("--> RESULT: SUCCESS")
            print(json.dumps(record_data, indent=2, ensure_ascii=False))
            
        print("\n[3] DIAGNOSIS DATA (/v1/readside/diagnosis/vehicle/):")
        if diagnosis_data is None:
            print("--> RESULT: FAILED (Returned None)")
        else:
            print("--> RESULT: SUCCESS")
            print(json.dumps(diagnosis_data, indent=2, ensure_ascii=False))
            
    print("\n" + "="*50)
    print("--- DEBUG COMPLETE ---")
    print("="*50)

***REMOVED***
    # --- IMPORTANT ---
    # Put an Enrichment ID here that you know is causing problems.
    # You can get this from the discovery phase or a previous run.
    TEST_ID = "39821850" # Example ID from your logs
    
    print(f"Starting debug for Enrichment ID: {TEST_ID}")
    asyncio.run(debug_id(TEST_ID))