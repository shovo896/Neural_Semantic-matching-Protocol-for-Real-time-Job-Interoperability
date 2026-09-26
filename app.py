import streamlit as 
from src.helper import extract_text_from_pdf ask_openai
from scr.job_api import search_jobs 




st.set_page_config(page_title="Job Search", page_icon=":mag:", layout="wide")
st.title("Job Search Application")
st.markdown("This application allows you to search for jobs, upload your resume, and get job recommendations based on your skills and experience.")
uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
if uploaded_file : 
    with st.spinner("Extracting text from the uploaded PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.success("Text extracted successfully!")
        st.text_area("Extracted Text", text, height=300)
        
    with st.spinner("summarizing your resume...."): 
        summary = ask_openai(f"Summarize the following resume text:\n{text}", model="gpt-oss-128B", temperature=0.7, max_tokens=500)
        st.success("Resume summarized successfully!")
        
    with st.spinner("Finding skill gaps on your resume.... "):
        skill_gaps = ask_openai(f"Identify skill gaps in the following resume text:\n{text}", model="gpt-oss-128B", temperature=0.7, max_tokens=500)
        st.success("Skill gaps identified successfully!")
        st.text_area("Identified Skill Gaps", skill_gaps, height=300)
        
    with st.spinner("suggest  a future roadmap to improve this persons career:",max_tokens=400):
        roadmap = ask_openai(f"Suggest a future roadmap to improve the career of the person based on the following resume text:\n{text}", model="gpt-oss-128B", temperature=0.7, max_tokens=500)
        st.success("Future roadmap suggested successfully!")
        st.text_area("Suggested Future Roadmap", roadmap, height=300)
        
        
    #display nicely formatter results 
    
    st.markdown("----")
    st.header("Summary of Resume") 
    st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>{summary}</div>", unsafe_allow_html=True)
    
    
    st.markdown("----")
    st.header("Identified Skill Gaps")
    st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>{skill_gaps}</div>", unsafe_allow_html=True)
    
    st.markdown("----")
    st.header("Suggested Future Roadmap") 
    st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>{roadmap}</div>", unsafe_allow_html=True)
    
    
    
    if st.button("Get job recommendations"): 
        with st.spinner("Fetching job recommendations..."): 
            keywords = ask_openai(f"Extract relevant keywords from the following resume text:\n{text}", model="gpt-oss-128B", temperature=0.7, max_tokens=500)
            st.success("Keywords extracted successfully!")
            search_query = keywords.replace("\n", ", ").strip()
            
        st.success(f"Extracted Keywords: {search_query}")
        
        
        with st.spinner("fetching jobs from LinkedIn and Naukri ...."):
            linkedin_jobs = search_jobs(search_query, location="Bangladesh", rows=60)
            naukri_jobs = search_jobs(search_query, location="Bangladesh", rows=60)
            st.success("Job recommendations fetched successfully!")
            
            
        st.markdown("----") 
        st.header("Job Recommendations from LinkedIn")
        
        if linkedin_jobs:
            for job in linkedin_jobs:
                st.subheader(job['title'])
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Link:** [Apply Here]({job['link']})")
                st.markdown("----")
        else:
            st.info("No job recommendations found on LinkedIn.")
            
        if naukri_jobs:
            st.markdown("----") 
            st.header("Job Recommendations from Naukri")
            for job in naukri_jobs:
                st.subheader(job['title'])
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Link:** [Apply Here]({job['link']})")
                st.markdown("----")
        else:
            st.info("No job recommendations found on Naukri.")
            
            
    
        
        
    
        