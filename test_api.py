# FILE: test_api_response.py
# A standalone script to test all Encar API endpoints, including authenticated ones.

import httpx
import json
import os

# We import the new token directly from our app's config to ensure tests match reality
try:
    from app.config import API_AUTH_TOKEN
except ImportError:
    API_AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsibWVkaWFfYXBpIiwibW9iaWxlX2FwaSIsImRpYWdub3Npc19hcGkiLCJlbmNhcl9yZXNvdXJjZSJdLCJzY29wZSI6WyJyZWFkIl0sImV4cCI6MjU1MzU4OTIyMCwiYXV0aG9yaXRpZXMiOlsiVVNFUiJdLCJqdGkiOiJlMDk0ZjkyNS01MTc5LTQzNjctYWVkYi03NmM4ZGVmMTBjMTgiLCJjbGllbnRfaWQiOiJiYzI4NWEwMy03OTE5LTRjZTktYWEyOC1mMWU0ZmZhYzM2MzIifQ._bXyZvx3Ie7wJxbOBXXyu5rpuE5ZwUNg_rnhfpTNvKw" # Fallback if run outside the project structure

# --- STEP 1: CONFIGURE THE TEST YOU WANT TO RUN ---
# Uncomment ONE of the sections below to choose which API endpoint to test.
# Make sure to put a real, working car ID in the ENRICH_ID variable.

# ======== Configuration ========
ENRICH_ID = "39624169"  # <-- IMPORTANT: USE A RECENT, VALID CAR ID FOR ENRICHMENT TESTS

# --- Test 1: Search API (Main List) ---
# CONFIG = {
#     "test_name": "SEARCH",
#     "url": "https://api.encar.com/search/car/list/premium",
#     "params": {'count': 'true', 'q': '(And.Hidden.N._.CarType.Y._.Mileage.range(..10000).)', 'sr': '|ModifiedDate|0|20'},
#     "is_enrichment": False,
# }

# --- Test 2: Record API (Owner/Accident History) ---
# CONFIG = {
#     "test_name": f"RECORD_{ENRICH_ID}",
#     "url": f"https://api.encar.com/v1/readside/record/vehicle/{ENRICH_ID}/open",
#     "params": None,
#     "is_enrichment": True,
# }

# --- Test 3: Diagnosis API (Inspection Results) ---
# CONFIG = {
#     "test_name": f"DIAGNOSIS_{ENRICH_ID}",
#     "url": f"https://api.encar.com/v1/readside/diagnosis/vehicle/{ENRICH_ID}",
#     "params": None,
#     "is_enrichment": True,
# }

# --- Test 4: Inspection API (VIN) ---
# CONFIG = {
#     "test_name": f"INSPECTION_{ENRICH_ID}",
#     "url": f"https://api.encar.com/v1/readside/inspection/vehicle/{ENRICH_ID}",
#     "params": None,
#     "is_enrichment": True,
# }

# --- Test 5: Verification API (Options) ---
# This is the new, authenticated endpoint.
CONFIG = {
    "test_name": f"OPTIONS_{ENRICH_ID}",
    "url": f"https://api.encar.com/verification/{ENRICH_ID}/simple",
    "params": {"optionIds": "10,16,327,328,329,330,1,332,85"}, # The IDs from your curl
    "is_enrichment": True,
    "is_authenticated": True, # This flag triggers the auth header
}


# --- STEP 2: RUN THE SCRIPT ---
# (No more changes needed below this line)

def get_headers(is_enrichment: bool, is_authenticated: bool = False) -> dict:
    """Returns the correct headers based on the API endpoint type."""
    if not is_enrichment:
        headers = {"Referer": "http://www.encar.com/", "Origin": "http://www.encar.com"}
    else:
        headers = {"Referer": "https://fem.encar.com/", "Origin": "https://fem.encar.com"}

    # Add common headers
    headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "application/json, text/plain, */*",
    })

    # NEW: Add the Authorization header if the endpoint requires it
    if is_authenticated:
        if not API_AUTH_TOKEN or "YOUR" in API_AUTH_TOKEN:
            print("⚠️ WARNING: API_AUTH_TOKEN is not set. The authenticated request will likely fail.")
        headers['Authorization'] = f'Bearer {API_AUTH_TOKEN}'
    
    return headers

def run_test(test_config: dict):
    """Fetches data from the target URL and saves the JSON response to a file."""
    test_name = test_config["test_name"]
    url = test_config["url"]
    params = test_config.get("params")
    is_enrichment = test_config.get("is_enrichment", False)
    is_authenticated = test_config.get("is_authenticated", False)
    
    output_filename = f"api_test_output_{test_name}.json"
    
    print(f"--- Running Test: {test_name} ---")
    print(f"Fetching from: {url}")
    if is_authenticated:
        print("Authentication: Using Bearer Token")

    headers = get_headers(is_enrichment, is_authenticated)

    try:
        with httpx.Client(headers=headers, timeout=30, follow_redirects=True) as client:
            response = client.get(url, params=params)
            
            print(f"Status Code: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"✅ Success! Raw API response saved to: {output_filename}")

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code} - Review the response below.")
        print(f"Response Body: {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

***REMOVED***
    if not os.path.exists("api_test_output_SEARCH.json"):
        print("First, ensure you have the 'httpx' library installed.")
        print("You can install it by running: pip install httpx\n")
    
    run_test(CONFIG)