from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text

from app.db.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    issues = Column(JSON, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False, index=True)
    ai_explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
