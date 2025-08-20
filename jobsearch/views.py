from django.shortcuts import render
from django.http import JsonResponse
from .utils.jobs import get_jobs_from_rapidapi
from .utils.places import get_lat_lng, get_nearby_places
from .utils.gemini_agent import extract_job_details


def job_search(request):
    jobs = []
    has_results = False

    if request.method == "POST":
        user_input = request.POST.get("query", "").strip()
        extracted = extract_job_details(user_input)
        role = extracted.get("role", "")
        location = extracted.get("location", "")

        if role and location:
            # ✅ Only fetch jobs for now (FAST response)
            jobs = get_jobs_from_rapidapi(role, location)
            has_results = bool(jobs)

            # Don’t fetch places yet — frontend will call AJAX
            for job in jobs:
                job["nearby_places"] = []  

    return render(request, "search.html", {
        "jobs": jobs,
        "has_results": has_results
    })


def load_nearby_places(request):
    """AJAX endpoint: fetch nearby places for a given company/location."""
    company = request.GET.get("company", "")
    location = request.GET.get("location", "")

    lat, lon = get_lat_lng(company, location)
    if not (lat and lon):
        return JsonResponse({"nearby_places": []})

    places = get_nearby_places(lat, lon)
    return JsonResponse({"nearby_places": places})



