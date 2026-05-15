from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthDataCreate(BaseModel):
    user_id: int
    heart_rate: float
    temperature: float
    stress_level: float
    sleep_hours: float
    timestamp: datetime


class HealthDataResponse(BaseModel):
    id: int
    user_id: int
    heart_rate: float
    temperature: float
    stress_level: float
    sleep_hours: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
