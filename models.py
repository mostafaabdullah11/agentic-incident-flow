from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class IncidentPayload(BaseModel):
    incident_sys_id: str
    number: str
    short_description: str
    description: str
    priority: int = Field(ge=1, le=5)
    
    
class DecisionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Literal["respond", "ask", "escalate"]
    message: str