# Agentic Incident Flow

A small AI-powered incident automation service.

## Project Goal

The system:

1. Receives a newly created ServiceNow incident.
2. Validates the incident payload.
3. Uses Gemini to choose one decision:
   - respond
   - ask
   - escalate
4. Writes the result back to the same ServiceNow incident.

## Architecture

```text
ServiceNow Incident
        |
        v
Business Rule
        |
        v
ngrok
        |
        v
FastAPI POST /webhook
        |
        +----> Validate payload
        |
        +----> Duplicate protection
        |
        +----> Return 202 Accepted
        |
        v
Background processing
        |
        v
Five supplied KB articles
        +
Gemini prompt
        |
        v
Gemini
        |
        v
respond / ask / escalate
        |
        v
ServiceNow REST API PATCH
        |
        v
Same incident updated
```

## Current Status

The complete Agentic Incident Flow is implemented.

The system now supports:

- ServiceNow incident creation trigger
- Automatic Business Rule webhook delivery
- FastAPI `POST /webhook`
- Incident payload validation
- Fast `202 Accepted` response
- Background incident processing
- In-memory duplicate protection
- Gemini decision engine
- Five-article knowledge-base grounding
- Structured `respond`, `ask`, or `escalate` output
- Retry handling for temporary Gemini API failures
- Automatic ServiceNow REST API write-back
- Customer-visible clarification comments
- Internal escalation work notes
- Automatic resolution for supported incidents
- Required three decision tests

## Requirements

- Python 3.11+
- ServiceNow Personal Developer Instance (PDI)
- ngrok account and application
- Gemini API key

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

The application runs locally at:

```text
http://127.0.0.1:8000
```

Open the API documentation at:

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

Receives and validates an incident payload from ServiceNow.

Example request:

```json
{
  "incident_sys_id": "abc123",
  "number": "INC001",
  "short_description": "Email server down",
  "description": "Users cannot access email",
  "priority": 1
}
```

A valid new incident returns:

```text
202 Accepted
```

## Expose the Local Service with ngrok

Start the FastAPI service:

```bash
uvicorn main:app --reload
```

In another terminal, start ngrok:

```bash
ngrok http 8000
```

ngrok will provide a public HTTPS URL such as:

```text
https://example.ngrok-free.app
```

The public webhook URL is:

```text
https://example.ngrok-free.app/webhook
```

The ngrok URL may change when ngrok is restarted. If it changes, update the ServiceNow Business Rule endpoint.

## ServiceNow Business Rule

In the ServiceNow PDI:

1. Open **System Definition > Business Rules**.
2. Create a new Business Rule.
3. Configure it with:
   - Name: `Task0 - Send Incident to Agent`
   - Table: `Incident [incident]`
   - Advanced: enabled
   - When: `after`
   - Insert: enabled
4. Paste the Business Rule script from:

```text
servicenow/business_rule.js
```

5. Replace:

```text
YOUR_ENDPOINT
```

with the current ngrok HTTPS URL.

Keep `/webhook` at the end.

Example:

```text
https://example.ngrok-free.app/webhook
```

The Business Rule sends each newly created ServiceNow incident to the FastAPI webhook automatically.

## Incident Payload

ServiceNow sends the following fields to `POST /webhook`:

- `incident_sys_id`
- `number`
- `short_description`
- `description`
- `priority`

Example:

```json
{
  "incident_sys_id": "abc123",
  "number": "INC0010001",
  "short_description": "Printer not printing after office move",
  "description": "It was working yesterday. I tried turning it off and on.",
  "priority": 3
}
```

The exact payload contract is available in:

```text
data/payload_contract.json
```

## Duplicate Protection

The service keeps an in-memory set of processed ServiceNow incident `sys_id` values.

If the same incident is received more than once:

- the first request is accepted as new
- later requests with the same `incident_sys_id` are ignored as duplicates

The duplicate guard is stored only in memory and resets if the Python service restarts.

## Gemini Configuration

The project uses the Gemini API for incident decisions.

Create a `.env` file based on `.env.example`.

Required Gemini variables:

```env
GEMINI_API_KEY=
GEMINI_MODEL=
```

- `GEMINI_API_KEY` is your private Gemini API key.
- `GEMINI_MODEL` is the Gemini model used by the service.

The real `.env` file must not be committed to Git.

## AI Decisions

Gemini receives:

- the ServiceNow incident
- the five supplied knowledge-base articles
- the decision rules from `prompt.txt`

The model must return exactly one of:

- `respond`
- `ask`
- `escalate`

### Respond

Used when a supplied knowledge-base article clearly covers the issue and the ticket contains enough information to apply the solution.

### Ask

Used when a knowledge-base article may apply, but the incident is too vague or incomplete to determine that confidently.

### Escalate

Used when none of the supplied knowledge-base articles covers the issue.

Gemini is instructed to use only the provided knowledge base.

## Knowledge Base

The approved knowledge base is stored in:

```text
data/kb_articles.json
```

It contains five articles covering:

1. Printer not printing
2. Email not sending
3. Cannot access system
4. Slow network
5. Browser pages not loading

The Gemini prompt must use these articles and no other knowledge source.

## Gemini Prompt

The exact prompt sent to Gemini is stored in:

```text
prompt.txt
```

The prompt defines:

- knowledge-base restrictions
- `respond`, `ask`, and `escalate` rules
- JSON output requirements
- the incident and knowledge-base placeholders

## ServiceNow Write-Back

Gemini produces exactly one decision.

### `respond`

The solution is written back to the incident and the ticket is resolved.

Fields used:

- `work_notes`
- `close_notes`
- `state = 6`
- `close_code = "Solution provided"`

### `ask`

A short clarification question is written to:

- `comments`

This makes the question customer-visible.

### `escalate`

The escalation reason is written to:

- `work_notes`

This keeps the message internal for the support team.

## Decision Tests

The required test incidents are stored in:

```text
data/test_incidents.json
```

Run:

```bash
python -m tests.test_decisions
```

Expected decisions:

| Incident | Expected Decision |
| --- | --- |
| Printer not printing after office move | `respond` |
| Cannot send email / vague description | `ask` |
| Annual leave approval request | `escalate` |

A successful run should report:

```text
Passed: 3
Failed: 0
```

## Validation

The project was validated for:

- valid webhook payload → `202 Accepted`
- missing required field → `422`
- priority outside `1–5` → `422`
- duplicate incident → ignored after first processing
- webhook returns quickly while Gemini runs in the background
- Gemini decision tests → `3 passed, 0 failed`
- printer incident → `respond` → resolved
- vague email incident → `ask` → customer-visible comment
- annual leave request → `escalate` → internal work note
- ServiceNow → FastAPI → Gemini → ServiceNow full automatic loop

## Environment Variables

The project uses the following environment variables:

```text
GEMINI_API_KEY=
GEMINI_MODEL=
SERVICENOW_INSTANCE_URL=
SERVICENOW_USERNAME=
SERVICENOW_PASSWORD=
```

Real secrets must be stored in:

```text
.env
```

The `.env` file must not be committed to GitHub.

The `.env.example` file should contain:

```env
GEMINI_API_KEY=
GEMINI_MODEL=
SERVICENOW_INSTANCE_URL=
SERVICENOW_USERNAME=
SERVICENOW_PASSWORD=
```

The `.env.example` file contains only variable names and can safely be committed.

## Security

Do not commit:

- `.env`
- ServiceNow passwords
- Gemini API keys
- ngrok authentication tokens

Sensitive values should only be stored locally in environment variables.
