from fastapi import FastAPI, status
from models import IncidentPayload
from duplicate_guard import mark_if_new

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Agentic Incident Flow is running"}


@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
def webhook(incident: IncidentPayload):
    print("Received incident:")
    print(incident.model_dump())

    if not mark_if_new(incident.incident_sys_id):
        print(f"Duplicate incident ignored: {incident.number}")

        return {
            "status": "duplicate",
            "incident_number": incident.number
        }

    print(f"Accepted new incident: {incident.number}")

    return {
        "status": "accepted",
        "incident_number": incident.number
    }