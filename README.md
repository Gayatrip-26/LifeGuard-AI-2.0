# LifeGuard AI 2.0

Production-grade starter scaffold for a real-time predictive health intelligence platform.

## Tech Stack

- Frontend: React + Tailwind CSS + Recharts + Leaflet
- Backend: FastAPI (Python)
- Microservices: Python FastAPI services
- Streaming: Apache Kafka
- Database: PostgreSQL + Redis
- Vector DB: ChromaDB
- Orchestration: Docker Compose

## Quick Start

1. Copy environment file:
   - `cp .env.example .env` (Linux/macOS)
   - `Copy-Item .env.example .env` (PowerShell)
2. Build and run:
   - `docker compose up --build`
3. Access:
   - Frontend: `http://localhost:5173`
   - Backend docs: `http://localhost:8000/docs`

## Project Layout

- `frontend/`: React dashboard app
- `backend/`: Main FastAPI backend
- `microservices/`: Specialized service skeletons
- `shared/`: Shared Python modules and schemas
