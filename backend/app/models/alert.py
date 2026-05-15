from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
