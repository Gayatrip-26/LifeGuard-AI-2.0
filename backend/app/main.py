from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.ai import router as ai_router
from app.api.routes.alert import router as alert_router
from app.api.routes.auth import router as auth_router
from app.api.routes.health_data import router as health_data_router
from app.api.routes.health import router as health_router
from app.api.routes.prediction import dashboard_router, router as prediction_router
from app.api.routes.user import router as user_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models.alert  # noqa: F401
from app.models import health_data, prediction, user  # noqa: F401
from app.rag.vector_store import ensure_medical_knowledge_loaded

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Main API for LifeGuard AI 2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(health_data_router)
app.include_router(ai_router)
app.include_router(alert_router)
app.include_router(prediction_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_medical_knowledge_loaded()


@app.get("/")
def root() -> dict:
    return {
        "message": "LifeGuard AI 2.0 backend is running.",
        "environment": settings.app_env,
    }
