# Neural Semantic Matching Protocol for Real-Time Job Interoperability

A Python project for analysing a PDF resume, generating AI-assisted career guidance, and retrieving job listings. It contains both a Streamlit web application and an MCP server for tool-based job search.

## What it does

- Extracts text from an uploaded PDF resume.
- Uses OpenRouter's `openai/gpt-oss-120b` model to generate a resume summary, skill-gap analysis, career roadmap, and job-search keywords.
- Retrieves Naukri and LinkedIn job listings through existing Apify actors.
- Exposes the job-search functions as MCP tools for use with MCP Inspector or another compatible client.

## Project layout

```text
.
├── app.py              # Streamlit resume-analysis application
├── mcp_server.py       # MCP stdio server
├── requirements.txt    # Python dependencies
└── src/
    ├── helper.py        # PDF extraction and OpenRouter client
    └── job_api.py       # Apify job-search integrations
```

## Requirements

- Python 3.13
- Node.js and `npx` only when using MCP Inspector
- An OpenRouter API key
- An Apify API token for job-search calls

## Setup

Create and activate a Python 3.13 virtual environment from the project directory:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: -r requirements.txt
python -m pip check
```

`--only-binary=:all:` avoids compiling `cryptography` with Rust/Cargo on macOS.

## Environment variables

Create a `.env` file in the project root. Do not commit this file or share its values.

```env
# OpenRouter API key; the existing code reads it through this variable name.
OPENAI_API_KEY=sk-or-v1-...

# Apify API token used by the job-search actors.
APIFY_API_KEY=apify_api_...
```

## Run the Streamlit application

```bash
source .venv/bin/activate
streamlit run app.py
```

Open the local URL printed by Streamlit, normally [http://localhost:8501](http://localhost:8501).

Upload a PDF resume to generate its summary, skill gaps, and roadmap. The application limits any prompt to the first 100,000 characters so that large PDFs do not exceed the model context limit.

## Run and inspect the MCP server

The server uses the stdio transport, so it does not have its own browser UI. Start it directly for an MCP client:

```bash
source .venv/bin/activate
python mcp_server.py
```

For an interactive browser UI, launch MCP Inspector from the project root:

```bash
source .venv/bin/activate
npx --yes @modelcontextprotocol/inspector "$PWD/.venv/bin/python" "$PWD/mcp_server.py"
```

Keep that terminal running, then open the URL shown by Inspector, usually [http://127.0.0.1:6274](http://127.0.0.1:6274).

### MCP tools

| Tool | Input | Purpose |
| --- | --- | --- |
| `fetch_linkedin_jobs` | `listofkeywords`, `cookies` | Searches LinkedIn jobs through Apify. |
| `fetch_naukri_jobs` | `listofkeywords` | Searches Naukri jobs through Apify. |

The LinkedIn Apify actor requires a non-empty array of valid LinkedIn session cookies. In Inspector, provide the cookie input in this shape:

```json
[
  {
    "name": "li_at",
    "value": "YOUR_LINKEDIN_SESSION_VALUE",
    "domain": ".linkedin.com",
    "path": "/"
  }
]
```

Never paste a real cookie into source code, commit it to Git, or share it publicly.

## Troubleshooting

| Error | Resolution |
| --- | --- |
| `Incorrect API key provided` | Verify that `OPENAI_API_KEY` contains an OpenRouter key and that `src/helper.py` keeps the OpenRouter base URL. |
| `gpt-oss-128B is not a valid model ID` | The configured model is `openai/gpt-oss-120b`; do not use the old ID. |
| Context-length `400` error | Use the existing prompt limit in `src/helper.py`; very large resumes are truncated before the API request. |
| `Failed building wheel for cryptography` | Reinstall with `python -m pip install --only-binary=:all: -r requirements.txt`. |
| `Field input.cookies must ...` | Supply a non-empty valid LinkedIn cookie array to the MCP tool. |
| `No module named mcp.server.fastmcp` | Install dependencies from `requirements.txt`; this project pins `mcp<2` because it uses the FastMCP v1 API. |

## Security notes

- Keep `.env`, API keys, Apify tokens, and LinkedIn cookies private.
- Do not add credentials to `README.md`, source files, screenshots, or Git commits.
- Apify actor runs and model requests may consume credits associated with your own accounts.
