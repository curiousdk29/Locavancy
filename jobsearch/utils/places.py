import requests
import time
import re
import os
from dotenv import load_dotenv
load_dotenv()
def clean_text(text):
    if not text:
        return ""
    return re.sub(r'[^\w\s,]', '', text).strip()

def get_lat_lng(company_name=None, location=None):
    queries = []

    # Clean the inputs
    company_name = clean_text(company_name)
    location = clean_text(location)

    # Create fallback search queries
    if company_name and location:
        queries = [
            f"{company_name}, {location}",
            f"{company_name.split()[0]}, {location}",
            location,
            company_name
        ]
    elif company_name:
        queries = [
            company_name,
            company_name.split()[0]
        ]
    elif location:
        queries = [location]
    else:
        return None, None  # Nothing to search

    for query in queries:
        try:
            print(f"🌐 Trying location: {query}")
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": query,
                "format": "json",
                "limit": 1
            }
            headers = {"User-Agent": "MyApp"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            if data:
                lat = data[0]["lat"]
                lon = data[0]["lon"]
                return float(lat), float(lon)
        except Exception as e:
            print(f"❌ Error searching {query}: {e}")
            time.sleep(1)

    print("⚠️ No coordinates found after all attempts.")
    return None, None

def get_nearby_places(lat, lon, query="cafe"):
    url = "https://places-api.foursquare.com/places/search"
    headers = {
        "Authorization": os.getenv("FOURSQUARE_API_KEY"),
        "Accept": "application/json",
        "X-Places-Api-Version": "2025-06-17",
    }

    queries = ["metro station", "bus stop", "restaurant", "hostel", "gym", "coffee shop", "bank", "ATM"]
    all_results = []

    for q in queries:
        print(f"[FOURSQUARE] Searching for '{q}' near {lat}, {lon}")
        params = {
            "ll": f"{lat},{lon}",
            "query": q,
            "limit": 1,
            "radius": 1000,  # 1 km radius
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            print(f"[FOURSQUARE RESULTS] Found {len(results)} places for '{q}'")
            all_results.extend(results)
        except Exception as e:
            print(f"[FOURSQUARE ERROR] {e}")

    return all_results
