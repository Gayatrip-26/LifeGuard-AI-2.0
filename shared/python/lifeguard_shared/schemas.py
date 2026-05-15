from pydantic import BaseModel, Field


class HealthSignal(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    heart_rate: float = Field(..., ge=0)
    spo2: float = Field(..., ge=0, le=100)
    timestamp: str = Field(..., description="ISO8601 timestamp")


class RiskScore(BaseModel):
    patient_id: str
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    timestamp: str
