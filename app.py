import streamlit as 
from src.helper import extract_text_from_pdf ask_openai



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
        
        
    
        