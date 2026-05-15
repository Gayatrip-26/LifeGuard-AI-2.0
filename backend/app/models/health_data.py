from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    heart_rate = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    stress_level = Column(Float, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="health_data")
