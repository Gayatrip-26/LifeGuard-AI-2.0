from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionCreate(BaseModel):
    user_id: int
    patient_id: str
    issues: list[str]
    risk_score: int
    risk_level: str
    ai_explanation: str


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    patient_id: str
    issues: list[str]
    risk_score: int
    risk_level: str
    ai_explanation: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RiskTrendBlock(BaseModel):
    trend: str
    last_score: int | None = None
    previous_score: int | None = None


class DashboardSummaryResponse(BaseModel):
    total_records: int
    high_risk_count: int
    latest_risk: str | None
    average_score: float
    risk_trend: RiskTrendBlock
