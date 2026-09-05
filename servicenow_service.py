import requests

from config import (
    SERVICENOW_INSTANCE_URL,
    SERVICENOW_USERNAME,
    SERVICENOW_PASSWORD,
)


def validate_servicenow_config() -> None:
    if not SERVICENOW_INSTANCE_URL:
        raise RuntimeError(
            "SERVICENOW_INSTANCE_URL is not configured."
        )

    if not SERVICENOW_USERNAME:
        raise RuntimeError(
            "SERVICENOW_USERNAME is not configured."
        )

    if not SERVICENOW_PASSWORD:
        raise RuntimeError(
            "SERVICENOW_PASSWORD is not configured."
        )


def update_incident(
    incident_sys_id: str,
    fields: dict,
) -> dict:
    validate_servicenow_config()

    url = (
        f"{SERVICENOW_INSTANCE_URL}"
        f"/api/now/table/incident/{incident_sys_id}"
    )

    response = requests.patch(
        url,
        auth=(
            SERVICENOW_USERNAME,
            SERVICENOW_PASSWORD,
        ),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=fields,
        timeout=15,
    )

    if not response.ok:
        print(
            "ServiceNow status:",
            response.status_code,
        )

        print(
            "ServiceNow response:",
            response.text,
        )

    response.raise_for_status()

    return response.json()


def write_respond(
    incident_sys_id: str,
    message: str,
) -> dict:
    fields = {
        "work_notes": message,
        "state": "6",
        "close_notes": message,
        "close_code": "Solution provided",
    }

    return update_incident(
        incident_sys_id=incident_sys_id,
        fields=fields,
    )

def write_ask(
    incident_sys_id: str,
    message: str,
) -> dict:
    fields = {
        "comments": message,
    }

    return update_incident(
        incident_sys_id=incident_sys_id,
        fields=fields,
    )


def write_escalate(
    incident_sys_id: str,
    message: str,
) -> dict:
    fields = {
        "work_notes": message,
    }

    return update_incident(
        incident_sys_id=incident_sys_id,
        fields=fields,
    )


def write_decision(
    incident_sys_id: str,
    decision: str,
    message: str,
) -> dict:
    if decision == "respond":
        return write_respond(
            incident_sys_id,
            message,
        )

    if decision == "ask":
        return write_ask(
            incident_sys_id,
            message,
        )

    if decision == "escalate":
        return write_escalate(
            incident_sys_id,
            message,
        )

    raise ValueError(
        f"Unsupported decision: {decision}"
    )