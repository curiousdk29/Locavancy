from django.shortcuts import render
from django.http import JsonResponse
from .utils.jobs import get_jobs_from_rapidapi
from .utils.places import get_lat_lng, get_nearby_places
from .utils.gemini_agent import extract_job_details


from .utils.jobs import get_jobs_from_rapidapi

def fetch_jobs_safe(role, location):
    try:
        return get_jobs_from_rapidapi(role, location)
    except Exception as e:
        print("Job fetch failed:", e)
        return []


def job_search(request):
    jobs = []
    has_results = False

    if request.method == "POST":
        user_input = request.POST.get("query", "").strip()
        
        # 1. Extract role/location safely
        extracted = {}
        try:
            extracted = extract_job_details(user_input)
        except Exception as e:
            print("Gemini extraction failed:", e)
        
        role = extracted.get("role", "")
        location = extracted.get("location", "")

        # 2. Fetch jobs safely
        if role and location:
            jobs = fetch_jobs_safe(role, location)
            has_results = bool(jobs)
            for job in jobs:
                job["nearby_places"] = []  # placeholder for async fetch

    return render(request, "search.html", {
        "jobs": jobs,
        "has_results": has_results
    })

def load_nearby_places(request):
    company = request.GET.get("company", "")
    location = request.GET.get("location", "")

    try:
        lat, lon = get_lat_lng(company, location)
        if not (lat and lon):
            return JsonResponse({"nearby_places": []})
        places = get_nearby_places(lat, lon)
        return JsonResponse({"nearby_places": places})
    except Exception as e:
        print("Nearby places fetch failed:", e)
        return JsonResponse({"nearby_places": []})



