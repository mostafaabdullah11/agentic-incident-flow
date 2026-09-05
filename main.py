from fastapi import BackgroundTasks, FastAPI, status

from duplicate_guard import mark_if_new
from incident_processor import process_incident
from models import IncidentPayload


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Agentic Incident Flow is running"
    }


@app.post(
    "/webhook",
    status_code=status.HTTP_202_ACCEPTED
)
def webhook(
    incident: IncidentPayload,
    background_tasks: BackgroundTasks,
):
    print("Received incident:")
    print(incident.model_dump())

    if not mark_if_new(incident.incident_sys_id):
        print(
            f"Duplicate incident ignored: "
            f"{incident.number}"
        )

        return {
            "status": "duplicate",
            "incident_number": incident.number,
        }

    print(
        f"Accepted new incident: "
        f"{incident.number}"
    )

    background_tasks.add_task(
        process_incident,
        incident,
    )

    return {
        "status": "accepted",
        "incident_number": incident.number,
    }