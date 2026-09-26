import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_KEY"))


def fetch_linkedin_job(search_query, location="Bangladesh", rows=60):
    """Fetch LinkedIn job listings through the existing Apify actor."""
    run_input = {
        "cookies": [],
        "userAgent": None,
        "searchUrl": "https://www.linkedin.com/jobs/search/?keywords=&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_C=1035&f_PP=104145663&f_JT=F&f_WT=3%2C2&f_SB2=21&position=1&pageNum=0",
        "filters.keywords": search_query,
        "filters.location": location,
        "filters.geoId": None,
        "filters.distance": None,
        "filters.sortBy": None,
        "filters.timePostedRange": None,
        "filters.experience": None,
        "filters.company": None,
        "filters.jobType": None,
        "filters.workplaceType": None,
        "filters.salaryBucketV2": None,
        "filters.industry": None,
        "filters.function": None,
        "filters.title": None,
        "filters.populatedPlace": None,
        "filters.commitments": None,
        "filters.applyWithLinkedin": False,
        "filters.earlyApplicant": False,
        "filters.jobInYourNetwork": False,
        "filters.verifiedJob": False,
        "filters.workRemoteAllowed": False,
        "filters.fairChanceEmployer": False,
        "scrapeJobDetails": False,
        "scrapeSkills": False,
        "scrapeCompany": False,
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
