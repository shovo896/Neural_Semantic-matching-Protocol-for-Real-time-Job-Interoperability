
import os 
from dotenv import load_dotenv 

from apify_client import ApifyClient

from openai import OpenAI 
load_dotenv() 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = ApifyClient("APIFY_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


'''def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file: The uploaded PDF file.
        """ 
    text = "" 
    try: 
        with fitz.open(uploaded_file) as pdf: 
            for page in pdf: 
                text += page.get_text() 
    except Exception as e: 
        print(f"Error extracting text from {uploaded_file}: {e}")
    return text'''
    
    
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "" 
    for page in doc: 
        text += page.get_text()

    return text




def ask_openai(prompt, model="gpt-oss-128B", temperature=0.7, max_tokens=500):
    """
    Sends a prompt to the OpenAI API and returns the response.

    Args:
        prompt: The prompt to send to the API.
        model: The model to use for the response.
        temperature: The sampling temperature for the response.
        max_tokens: The maximum number of tokens in the response.
    Returns:
        The response from the OpenAI API.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}], 
        max_tokens=max_tokens,
        temperature=temperature 
    )
    return response.choices[0].text.strip()





def fetch_linkedin_job(search_query, location="Bangladesh", rows=60):
    """
    Fetches job listings from LinkedIn based on the search query and location.

    Args:
        search_query: The job title or keywords to search for.
        location: The location to search for jobs in.
        rows: The number of job listings to fetch (default is 60).
    Returns:
        A list of job listings, where each listing is a dictionary containing job details.
    """
    # This is a placeholder implementation. You would need to implement the actual LinkedIn API calls here.
   
# Initialize the ApifyClient with your API token


# Prepare the Actor input
run_input = {
    "cookies": None,
    "userAgent": None,
    "searchUrl": "https://www.linkedin.com/jobs/search/?keywords=&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_C=1035&f_PP=104145663&f_JT=F&f_WT=3%2C2&f_SB2=21&position=1&pageNum=0",
    "filters.keywords": None,
    "filters.location": None,
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
    "count": 25,
}

# Run the Actor and wait for it to finish
run = client.actor("gdbRh93zn42kBYDyS").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)


def fetch_naukri_job(search_query, location="Bangladesh", rows=60):
    """
    Fetches job listings from Naukri based on the search query and location.

    Args:
        search_query: The job title or keywords to search for.
        location: The location to search for jobs in.
        rows: The number of job listings to fetch (default is 60).
    Returns:
        A list of job listings, where each listing is a dictionary containing job details.
    """
    # This is a placeholder implementation. You would need to implement the actual Naukri API calls here.
    


# Prepare the Actor input
run_input = {
    "searchUrls": ["https://www.naukri.com/it-jobs"],
    "maxItems": 30,
    "proxyConfiguration": { "useApifyProxy": False },
}

# Run the Actor and wait for it to finish
run = client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)


    
    



