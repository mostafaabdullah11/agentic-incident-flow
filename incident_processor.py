from gemini_service import decide_incident
from models import IncidentPayload
from servicenow_service import write_decision


def process_incident(incident: IncidentPayload) -> None:
    try:
        print(f"Processing incident: {incident.number}")

        result = decide_incident(incident)

        print(f"Decision for {incident.number}:")
        print(f"  decision = {result.decision}")
        print(f"  message  = {result.message}")

        write_decision(
            incident_sys_id=incident.incident_sys_id,
            decision=result.decision,
            message=result.message,
        )

        print(
            f"ServiceNow updated successfully "
            f"for {incident.number}"
        )

    except Exception as exc:
        print(
            f"Failed to process incident "
            f"{incident.number}: {exc}"
        )