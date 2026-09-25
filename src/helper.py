import fitz 

import os 
from dotenv import load_dotenv 
load_dotenv()


def extract_text_from_pdf(uploaded_file):
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
    return text