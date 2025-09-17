import requests
from app.config import settings

def fetch_jobs(query: str, location: str = "india", results_per_page: int = 5):
    """
    Fetch jobs from Adzuna API for a given query.
    Falls back to mock jobs if none found or on error.
    """
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "where": location,
        "content-type": "application/json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("results", [])

            if jobs:  # ✅ real jobs found
                return [
                    {
                        "title": job.get("title"),
                        "company": job.get("company", {}).get("display_name"),
                        "location": job.get("location", {}).get("display_name"),
                        "redirect_url": job.get("redirect_url"),
                    }
                    for job in jobs
                ]

        # ✅ fallback if no jobs
        return [
            {
                "title": f"{query} Specialist",
                "company": "Demo Company",
                "location": location,
                "redirect_url": "https://example.com/job",
            }
        ]

    except Exception as e:
        # fallback on error
        return [
            {
                "title": f"{query} Engineer",
                "company": "Fallback Corp",
                "location": location,
                "redirect_url": "https://example.com/job",
            }
        ]
