from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    health_data = relationship(
        "HealthData",
        back_populates="user",
        cascade="all, delete-orphan",
    )
