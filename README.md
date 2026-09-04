# Agentic Incident Flow

A small AI-powered incident automation service 

## Project Goal

The completed system will:

1. Receive a newly created ServiceNow incident.
2. Validate the incident payload.
3. Ask Gemini to choose one decision:
   - respond
   - ask
   - escalate
4. Write the result back to the same ServiceNow incident.

## Current Status

Phase 1 — Foundation.

Currently implemented:

- FastAPI application
- Health/root endpoint
- `POST /webhook`
- Incident payload validation
- `202 Accepted` response for valid incidents

## Requirements

- Python 3.11+

## Local Setup

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Current API Endpoints

### GET /

Checks that the application is running.

Example response:

```json
{
  "message": "Agentic Incident Flow is running"
}
```

### POST /webhook

Receives and validates an incident payload.

Example request:

```json
{
  "incident_sys_id": "abc123",
  "number": "INC001",
  "short_description": "Email server down",
  "description": "Users cannot access email",
  "priority": "1"
}
```

Example response:

```json
{
  "status": "accepted",
  "incident_number": "INC001"
}
```

A valid incident returns:

```text
202 Accepted
```

## Environment Variables

The project will later use these environment variables:

```text
GEMINI_API_KEY=
SERVICENOW_INSTANCE_URL=
SERVICENOW_USERNAME=
SERVICENOW_PASSWORD=
```

Real secrets must be stored in `.env`.

The `.env` file must not be committed to GitHub.

The `.env.example` file contains only the variable names and can safely be committed.

## Next Steps

Later phases will add:

- ngrok integration
- ServiceNow integration
- Gemini integration
- incident decision logic
- ServiceNow incident updates
- full testing
- complete architecture documentation