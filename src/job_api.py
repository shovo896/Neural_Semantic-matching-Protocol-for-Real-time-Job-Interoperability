import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_KEY"))


def fetch_linkedin_job(search_query, location="Bangladesh", rows=60):
    """Fetch LinkedIn job listings through the existing Apify actor."""
    run_input = {
        "cookies": None,
        "filters.keywords": search_query,
        "filters.location": location,
        "count": rows,
    }
    run = client.actor("gdbRh93zn42kBYDyS").call(run_input=run_input)
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


def fetch_naukri_job(search_query, location="Bangladesh", rows=60):
    """Fetch Naukri job listings through the existing Apify actor."""
    run_input = {
        "searchUrls": [f"https://www.naukri.com/{search_query.replace(' ', '-')}-jobs"],
        "maxItems": rows,
        "proxyConfiguration": {"useApifyProxy": False},
    }
    run = client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())
