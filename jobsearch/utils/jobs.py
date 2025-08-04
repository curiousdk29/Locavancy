import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_jobs_from_rapidapi(role, location):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{role} in {location}",
        "page": "1",
        "num_pages": "1",
       
    }

    headers = {
        "X-RapidAPI-Key":  os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("job_title"),
                "company": item.get("employer_name"),
                "location": item.get("job_city") or item.get("job_country"),
                "url": item.get("job_apply_link")
            })
        return jobs

    except Exception as e:
        print("Error fetching jobs from RapidAPI:", e)
        return []
