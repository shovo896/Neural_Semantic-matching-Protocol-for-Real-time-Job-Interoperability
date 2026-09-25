import fitz 
import stream 
import os 
from dotenv import load_dotenv 

from openai import OpenAI 
load_dotenv() 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
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




def ask_openai(prompt, model="gpt-oss", temperature=0.7, max_tokens=500):
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

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}], 
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()



    
    



