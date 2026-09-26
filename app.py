import streamlit as 
from src.helper import extract_text_from_pdf 



st.set_page_config(page_title="Job Search", page_icon=":mag:", layout="wide")
st.title("Job Search Application")
st.markdown("This application allows you to search for jobs, upload your resume, and get job recommendations based on your skills and experience.")
uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
if uploaded_file : 
    with st.spinner("Extracting text from the uploaded PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.success("Text extracted successfully!")
        st.text_area("Extracted Text", text, height=300)
        