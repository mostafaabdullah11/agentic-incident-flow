from gemini_service import decide_incident
from models import IncidentPayload


def process_incident(incident: IncidentPayload) -> None:


    try:
        print(f"Processing incident: {incident.number}")

        result = decide_incident(incident)

        print(f"Decision for {incident.number}:")
        print(f"  decision = {result.decision}")
        print(f"  message  = {result.message}")

    except Exception as exc:
        print(
            f"Failed to process incident {incident.number}: {exc}"
        )