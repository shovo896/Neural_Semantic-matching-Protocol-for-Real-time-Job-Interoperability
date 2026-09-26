# Neural Semantic Matching Protocol for Real-Time Job Interoperability

A Python project for analysing a PDF resume, generating AI-assisted career guidance, and retrieving job listings. It contains both a Streamlit web application and an MCP server for tool-based job search.

## What it does

- Extracts text from an uploaded PDF resume.
- Uses OpenRouter's `openai/gpt-oss-120b` model to generate a resume summary, skill-gap analysis, career roadmap, and job-search keywords.
- Retrieves Naukri and LinkedIn job listings through existing Apify actors.
- Exposes the job-search functions as MCP tools for use with MCP Inspector or another compatible client.

## Architecture and request flow

```text
PDF resume
   │
   ▼
Streamlit app (app.py)
   │
   ├── PyMuPDF text extraction (src/helper.py)
   │      │
   │      ▼
   │   OpenRouter / openai/gpt-oss-120b
   │      ├── summary
   │      ├── skill-gap analysis
   │      ├── career roadmap
   │      └── job-search keywords
   │
   ▼
Apify job actors (src/job_api.py)
   ├── LinkedIn listings
   └── Naukri listings

MCP client / Inspector ──► mcp_server.py ──► the same Apify job functions
```

The Streamlit application and MCP server are independent entry points. Both reuse the same job-search implementation in `src/job_api.py`.

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

### Component responsibilities

| Component | Responsibility |
| --- | --- |
| `app.py` | Uploads a PDF, calls the AI helper, displays analysis, and requests recommendations. |
| `src/helper.py` | Extracts PDF text and makes OpenRouter-compatible Chat Completions calls. |
| `src/job_api.py` | Builds Apify actor input and returns job-listing records. |
| `mcp_server.py` | Registers LinkedIn and Naukri search functions as stdio MCP tools. |
| `requirements.txt` | Reproducible dependency list; `mcp<2` preserves the FastMCP v1 API used by this project. |

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

### First-run verification

Run these checks before starting the app:

```bash
python --version
python -m pip check
python -m py_compile app.py src/helper.py src/job_api.py mcp_server.py
```

Expected result: Python 3.13 is active, `pip check` reports no broken requirements, and compilation returns without an error.

## Environment variables

Create a `.env` file in the project root. Do not commit this file or share its values.

```env
# OpenRouter API key; the existing code reads it through this variable name.
OPENAI_API_KEY=sk-or-v1-...

# Apify API token used by the job-search actors.
APIFY_API_KEY=apify_api_...
```

### Provider configuration

| Service | Used for | Code location | Required credential |
| --- | --- | --- | --- |
| OpenRouter | Resume analysis and keyword extraction | `src/helper.py` | `OPENAI_API_KEY` containing an OpenRouter key |
| Apify | LinkedIn and Naukri job actors | `src/job_api.py` | `APIFY_API_KEY` |
| LinkedIn | Required by the LinkedIn Apify actor | MCP tool input | A valid, non-empty cookie array |

Although the variable is named `OPENAI_API_KEY`, the configured base URL is OpenRouter: `https://openrouter.ai/api/v1`.

## Run the Streamlit application

```bash
source .venv/bin/activate
streamlit run app.py
```

Open the local URL printed by Streamlit, normally [http://localhost:8501](http://localhost:8501).

Upload a PDF resume to generate its summary, skill gaps, and roadmap. The application limits any prompt to the first 100,000 characters so that large PDFs do not exceed the model context limit.

### Streamlit workflow

1. Upload a text-based PDF resume.
2. Wait for text extraction and the three AI outputs: summary, skill gaps, and career roadmap.
3. Review the displayed analysis.
4. Select **Get job recommendations** to generate search keywords and call the Apify job actors.

The model is called separately for each analysis step. AI and Apify calls can consume credits and their runtime depends on the external providers.

> **LinkedIn note:** the current Streamlit page does not collect a LinkedIn cookie. The LinkedIn Apify actor requires one, so use the MCP tool for authenticated LinkedIn searches, or add a secure cookie-input flow before relying on the Streamlit LinkedIn result section. Naukri does not require this MCP cookie parameter.

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

### Test a tool with Inspector

1. Confirm the status in the top-right corner says **Connected**.
2. Open the **Tools** tab.
3. Select `fetch_naukri_jobs` and enter a value such as `data scientist` for `listofkeywords`.
4. Run the tool and inspect the returned listing records.
5. For `fetch_linkedin_jobs`, provide both `listofkeywords` and a valid `cookies` array.

If source code changes while Inspector is open, stop it with `Ctrl+C`, run the Inspector command again, and reconnect. The stdio server is started as a child process, so it does not automatically reload edited Python files.

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

### MCP response behavior

Each tool waits for its corresponding Apify actor run to complete and then returns the actor's dataset items as a list. The fields returned by an actor are controlled by Apify, so inspect an actual result before assuming a particular field is always present.

## Known limitations

- PDF extraction works best for PDFs containing selectable text. Image-only or scanned PDFs may return little or no text.
- Only the first 100,000 extracted prompt characters are sent to the model; content beyond that limit is not analysed.
- LinkedIn search requires a valid session cookie when invoked through MCP.
- Job availability, actor schema, pricing, and response fields are controlled by Apify and the external job platforms.
- The application does not persist uploaded resumes, analysis results, or chat history after the Streamlit session ends.

## Development commands

| Task | Command |
| --- | --- |
| Install/update dependencies | `python -m pip install --only-binary=:all: -r requirements.txt` |
| Check dependency consistency | `python -m pip check` |
| Compile Python modules | `python -m py_compile app.py src/helper.py src/job_api.py mcp_server.py` |
| Run web app | `streamlit run app.py` |
| Run MCP stdio server | `python mcp_server.py` |
| Launch MCP Inspector | `npx --yes @modelcontextprotocol/inspector "$PWD/.venv/bin/python" "$PWD/mcp_server.py"` |

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
