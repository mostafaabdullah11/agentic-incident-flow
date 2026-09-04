from pydantic import BaseModel, Field


class IncidentPayload(BaseModel):
    incident_sys_id: str
    number: str
    short_description: str
    description: str
    priority: int = Field(ge=1, le=5)