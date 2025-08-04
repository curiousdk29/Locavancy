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
            jobs = get_jobs_from_rapidapi(role, location)
            has_results = bool(jobs)

            for job in jobs:
                # Form the location string
                job_loc = f"{job.get('company', '')}, {job.get('location', '')}"

                # Try getting lat/lon
                lat, lon = get_lat_lng(job.get("company", ""), job.get("location", ""))

                if lat and lon:
                    # Get nearby places (like cafés)
                    job["nearby_places"] = get_nearby_places(lat, lon)

                else:
                    job["nearby_places"] = []

    return render(request, "search.html", {
        "jobs": jobs,
        "has_results": has_results
    })


def company_location_lookup(request):
    company = request.GET.get("company")
    location = request.GET.get("location")

    if not location and not company:
        return JsonResponse({"error": "Please provide at least a company or location."}, status=400)

    lat, lon = get_lat_lng(company, location)

    if lat and lon:
        return JsonResponse({"latitude": lat, "longitude": lon})
    else:
        return JsonResponse({"error": "Coordinates not found."}, status=404)
