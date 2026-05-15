from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    user_id: int
    patient_id: str
    message: str


class AlertResponse(BaseModel):
    id: int
    user_id: int
    patient_id: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
