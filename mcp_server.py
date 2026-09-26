from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_job, fetch_naukri_job


mcp = FastMCP(
    name="Job Search Application",
    instructions="Search LinkedIn and Naukri jobs using resume keywords.",
)


@mcp.tool()

async def fetch_linkedin_jobs(listofkeywords: str, cookies: list[dict]):
    return fetch_linkedin_job(listofkeywords, location="Bangladesh", rows=60, cookies=cookies)

@mcp.tool()

async def fetch_naukri_jobs(listofkeywords):
    return fetch_naukri_job(listofkeywords, location="Bangladesh", rows=60)



if __name__ == "__main__": 
    mcp.run(transport="stdio") 
    
