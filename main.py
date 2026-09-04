from fastapi import FastAPI, status

from models import IncidentPayload


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Agentic Incident Flow is running"}


@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
def webhook(incident: IncidentPayload):
    return {
        "status": "accepted",
        "incident_number": incident.number
    }