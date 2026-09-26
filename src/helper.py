import os

import fitz
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_openai(prompt, model="openai/gpt-oss-120b", temperature=0.7, max_tokens=500):
    """Send a prompt to the configured OpenAI API."""
    prompt = prompt[:100_000]
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()
