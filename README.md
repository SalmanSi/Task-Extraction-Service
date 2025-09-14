# Task Extraction Service

A FastAPI-based backend service that extracts clearly defined project milestones (tasks with title, description, deliverable, and due date) from uploaded proposal documents (PDF, DOCX, TXT) using OpenAI or Gemini LLMs via LangChain structured outputs.

## Features
- Single upload endpoint that both stores the file and performs milestone extraction
- Structured JSON output enforced by Pydantic schema
- Automatic rejection (status `failed`) when required milestone details are missing or unclear
- Supports OpenAI (`gpt-5-nano` placeholder) or Gemini (`gemini-2.5-flash`) models
- Dockerized for easy deployment
- Simple static demo page (`index.html`) for manual testing

## Tech Stack
- FastAPI
- LangChain (structured output)
- OpenAI / Google Gemini APIs
- Pydantic models for response guarantees

## Environment Variables
Create a `.env` file in the project root (never commit real keys):

```
# One (or both) of these must be set depending on provider you want to use
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key

```

Notes:
- The code currently calls `analyze_milestones(..., provider="openai")` in `main.py`. Change to `gemini` if you prefer Gemini or make it configurable.
- If the chosen provider's key is missing, the request will fail at runtime when the SDK tries to authenticate.

## Running the Service

### Docker
```bash
docker build -t milestone-backend .
docker run --env-file .env -p 8000:8000 -v $(pwd)/documents:/app/documents milestone-backend
```

### Local (no Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```
Service runs at: http://localhost:8000

OpenAPI docs: http://localhost:8000/docs

## Quick Demo (index.html)
A lightweight static demo client is provided as `index.html`.

Open it directly in a browser while the backend is running. It sends a multipart POST to `/upload` and renders the JSON response.


## API Endpoint
### POST /upload
Uploads a document AND triggers milestone extraction.

Request (multipart/form-data):
- file: PDF | DOCX | TXT

Curl example:
```bash
curl -X POST -F "file=@documents/FYP\ Proposal\ Document.docx" http://localhost:8000/upload
```

### Response Schema
The response always matches `MilestoneExtractionResult`:
```
{
  "status": "success" | "failed",
  "tasks": null | [
    {
      "title": "...",
      "description": "...",
      "deliverable": "...",
      "due_date": "YYYY-MM-DD"
    }
  ],
  "message": "" | "Explanation when failed"
}
```

### Successful Extraction Example
(Example adapted from `app.log` – truncated for brevity):
```
{
  "status": "success",
  "tasks": [
    {
      "title": "Module 1: Backend Development & Browser Agent",
      "description": "Objective: Build APIs for model inference, task orchestration, and Judge LLM integration. Develop browser automation agent with Playwright and DOM manipulation.",
      "deliverable": "Fully functional backend service exposing REST APIs, supporting LLM orchestration and real-time browser action execution.",
      "due_date": "2025-10-31"
    },
    {
      "title": "Module 2: Web Extension for End-Users",
      "description": "Objective: Provide a user-facing Chrome/Edge extension where tasks can be entered in natural language, models can be configured (API-based vs local via Ollama), and task progress can be observed live.",
      "deliverable": "Browser extension with configurable settings, real-time feedback, and integration with backend APIs.",
      "due_date": "2025-10-31"
    }
    // ...more tasks...
  ],
  "message": ""
}
```

### Failed Extraction Example
(When required milestone details like due dates or deliverables are missing):
```
{
  "status": "failed",
  "tasks": null,
  "message": "Milestones are described but no explicit due dates for each milestone are provided; only module tentative deadlines are listed, not linked to milestones. Without clear due dates (and corresponding deliverables) for milestones, milestone extraction cannot be performed."
}
```

## Failure Conditions (Enforced by Prompt)
The service will deliberately return `status: failed` when:
- Due dates are missing, unclear, or not per milestone
- Deliverables are not clearly defined
- Description is ambiguous
- (Special rule) A publication task is mentioned but its conference/journal deadline isn’t specified

## Modifying Provider
In `main.py` line where `analyze_milestones(..., provider="openai")` is called, change to `"gemini"` or expose a query/header param if you want dynamic selection.

## Project Structure
```
main.py                # FastAPI app & /upload endpoint
services/milestone_service.py  # Orchestrates extraction & LLM call
models/milestone_models.py     # Pydantic response models
utils/extract.py       # File loaders & text cleaning
utils/llm_selector.py  # Selects OpenAI or Gemini client
documents/             # Uploaded source files
index.html             # Simple static demo frontend
app.log                # Runtime log with extraction history
```

## Troubleshooting
- 400 Unsupported file type: Ensure extension is one of .pdf .docx .txt
- 500 Internal error: Check `app.log` for stacktrace; often missing API key or model name issue
- Empty/failed extraction: Provide clearer milestone definitions with explicit due dates & deliverables

## Security Notes
- Never commit real API keys
- Consider restricting CORS in production
- Validate file size/type further for production hardening

## License
MIT
