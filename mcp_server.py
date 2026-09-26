from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_job, fetch_naukri_job


mcp = FastMCP(
    title="Job Search Application",
    description="This application allows you to search for jobs, upload your resume, and get job recommendations based on your skills and experience.",
    theme="light",
    layout="wide",
    favicon=":mag:",
)


@mcp.tool()

async def fetch_linkedin_jobs(listofkeywords):
    return fetch_linkedin_job(listofkeywords, location="Bangladesh", rows=60)

@mcp.tool()

async def fetch_naukri_jobs(listofkeywords):
    return fetch_naukri_job(listofkeywords, location="Bangladesh", rows=60)


