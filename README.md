````markdown
# 🩺 LifeGuard AI 2.0 — Real-Time Predictive Health Intelligence Platform

> An AI-powered real-time health monitoring and predictive analytics platform built using distributed systems, event-driven microservices, and Retrieval-Augmented Generation (RAG).

![Frontend](https://img.shields.io/badge/Frontend-ReactJS-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Streaming](https://img.shields.io/badge/Streaming-Kafka-orange)
![VectorDB](https://img.shields.io/badge/VectorDB-ChromaDB-red)
![Deployment](https://img.shields.io/badge/Deployment-Docker-informational)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-success)
![Status](https://img.shields.io/badge/Project_Status-Production--Grade-success)

---

# ⚠️ Important Notice

> **Note:**  
> This repository is a portfolio showcase version of **LifeGuard AI 2.0**.  
> Some advanced production features, internal AI pipelines, enterprise integrations, infrastructure configurations, and proprietary implementations are intentionally excluded.

---

# 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Project Aim](#-project-aim)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Microservices Architecture](#-microservices-architecture)
- [Project Structure](#-project-structure)
- [Frontend Features](#-frontend-features)
- [Backend Features](#-backend-features)
- [AI & RAG Pipeline](#-ai--rag-pipeline)
- [Authentication System](#-authentication-system)
- [Real-Time Data Pipeline](#-real-time-data-pipeline)
- [Database Design](#-database-design)
- [Docker Deployment](#-docker-deployment)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [API Overview](#-api-overview)
- [Screenshots](#-screenshots)
- [Learning Outcomes](#-learning-outcomes)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Author](#-author)

---

# 📖 Overview

LifeGuard AI 2.0 is a real-time predictive healthcare intelligence platform designed to monitor patient health vitals, analyze risk levels, generate AI-driven insights, and provide alert-based monitoring using distributed microservices.

The system processes live health data streams through Apache Kafka, stores structured records in PostgreSQL, caches data with Redis, and uses ChromaDB-powered Retrieval-Augmented Generation (RAG) for intelligent AI explanations and recommendations.

The platform demonstrates production-grade backend architecture concepts including:

- Event-driven systems
- Distributed microservices
- Real-time streaming
- AI-powered analytics
- JWT authentication
- Dockerized deployment
- RAG-based intelligence systems

---

# ❗ Problem Statement

Traditional health monitoring systems often suffer from:

- Delayed detection of critical health conditions
- Lack of intelligent prediction systems
- Poor scalability for real-time monitoring
- No AI-based explanation for medical risks
- Limited real-time alerting capabilities

LifeGuard AI 2.0 addresses these issues using scalable distributed system architecture and AI-driven predictive analytics.

---

# 🎯 Project Aim

The main aim of LifeGuard AI 2.0 is to build a scalable, intelligent, and real-time health monitoring platform capable of:

- Monitoring patient vitals continuously
- Detecting abnormal health conditions
- Generating predictive risk analysis
- Providing AI-generated medical explanations
- Supporting scalable distributed architecture

---

# 🎯 Objectives

- Build real-time health data ingestion pipelines
- Implement event-driven communication using Kafka
- Create secure JWT-based authentication
- Develop predictive health risk analysis
- Integrate AI-powered RAG explanations
- Build scalable microservices architecture
- Visualize health trends through dashboards
- Enable Docker-based deployment

---

# 🚀 Key Features

## 🔐 Authentication System

- JWT-based secure login/register
- Password hashing using bcrypt
- Protected APIs
- User-based health isolation

## 📊 Real-Time Dashboard

- Live health monitoring
- Risk score visualization
- Alert notifications
- AI-generated recommendations
- Auto-refresh dashboard

## ⚡ Distributed Architecture

- Event-driven microservices
- Kafka streaming pipeline
- Independent scalable services

## 🧠 AI Health Intelligence

- RAG-powered AI explanations
- Health recommendation engine
- Risk interpretation
- Context-aware health analysis

## 📈 Predictive Analytics

- Health risk scoring
- High-risk detection
- Trend analysis
- Alert generation

---

# 🏗️ System Architecture

```text
Frontend (React Dashboard)
        │
        ▼
FastAPI Backend API
        │
        ▼
Kafka Event Streaming
        │
 ┌───────────────┬────────────────┐
 ▼               ▼                ▼
Ingestion     Prediction       AI/RAG
Service       Service          Service
 │               │                │
 ▼               ▼                ▼
PostgreSQL     Redis          ChromaDB
````

---

# 🛠️ Tech Stack

## 🎨 Frontend

* ReactJS
* Tailwind CSS
* Recharts
* Axios
* React Router
* Vite

## ⚙️ Backend

* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication
* REST APIs

## 🗄️ Databases

* PostgreSQL
* Redis
* ChromaDB

## ⚡ Streaming & Distributed Systems

* Apache Kafka
* Zookeeper

## 🤖 AI & Machine Learning

* Sentence Transformers
* Transformers
* PyTorch
* Retrieval-Augmented Generation (RAG)

## 🐳 DevOps & Deployment

* Docker
* Docker Compose

---

# 🧩 Microservices Architecture

The platform follows a distributed microservices architecture:

## 1️⃣ Backend Service

Handles:

* Authentication
* User management
* API gateway
* Dashboard APIs

## 2️⃣ Ingestion Service

Handles:

* Incoming health vitals
* Kafka event publishing
* Real-time ingestion

## 3️⃣ Prediction Service

Handles:

* Risk analysis
* Health score generation
* Alert creation

## 4️⃣ AI/RAG Service

Handles:

* AI explanations
* Context retrieval
* Recommendation generation

---

# 📁 Project Structure

```text
LifeGuard-AI-2.0/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── backend/
│   ├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   └── services/
│
├── microservices/
│   ├── ingestion_service/
│   ├── prediction_service/
│   └── internal_model/
│
├── shared/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🎨 Frontend Features

* Health dashboard
* Authentication pages
* Real-time charts
* Risk cards
* Alert notifications
* Health input forms
* AI insight cards

---

# ⚙️ Backend Features

* REST APIs
* JWT security
* Kafka integration
* PostgreSQL ORM models
* Redis caching
* AI service integration
* Health prediction APIs

---

# 🧠 AI & RAG Pipeline

The AI system uses Retrieval-Augmented Generation (RAG):

1. Health records are processed
2. Relevant context retrieved from ChromaDB
3. AI generates contextual explanation
4. Recommendations returned to dashboard

This improves explainability and intelligent decision support.

---

# 🔐 Authentication System

The system uses:

* JWT Tokens
* Password hashing
* Protected routes
* User-specific dashboards

Authentication flow:

```text
User Login → JWT Token → Protected APIs → Dashboard Access
```

---

# ⚡ Real-Time Data Pipeline

```text
Health Input
     │
     ▼
Ingestion Service
     │
     ▼
Kafka Topic
     │
     ▼
Prediction Service
     │
     ▼
Database + Alerts + AI
```

---

# 🗄️ Database Design

## PostgreSQL Stores

* Users
* Health records
* Predictions
* Alerts

## Redis Stores

* Cached predictions
* Fast dashboard responses

## ChromaDB Stores

* AI embeddings
* RAG knowledge context

---

# 🐳 Docker Deployment

The project is fully containerized using Docker Compose.

Services include:

* Frontend
* Backend
* Kafka
* Zookeeper
* PostgreSQL
* Redis
* ChromaDB
* Prediction Service
* Ingestion Service

---

# ⚡ Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Gayatrip-26/LifeGuard-AI-2.0.git
```

---

## 2️⃣ Open Project

```bash
cd LifeGuard-AI-2.0
```

---

## 3️⃣ Start Docker Services

```bash
docker compose up --build
```

---

# 🌐 Access Application

| Service      | URL                                                      |
| ------------ | -------------------------------------------------------- |
| Frontend     | [http://localhost:5173](http://localhost:5173)           |
| Backend Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ChromaDB     | [http://localhost:8001](http://localhost:8001)           |

---

# 🔑 Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/lifeguard
SECRET_KEY=your_secret_key
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
REDIS_URL=redis://redis:6379
CHROMA_HOST=chromadb
```

---

# 📡 API Overview

## Authentication APIs

### POST `/auth/register`

Register user.

### POST `/auth/login`

Authenticate user.

---

## Health APIs

### POST `/health`

Submit health vitals.

### GET `/health/{user_id}`

Get health history.

---

## AI APIs

### POST `/ai/query`

Generate AI explanation.

---

# 📸 Screenshots

## Dashboard

* Real-time risk monitoring
* AI insights
* Alerts and analytics

## Health Input

* Submit health vitals
* Trigger predictions

## AI Explanation Panel

* Intelligent medical insights
* Recommendations

---

# 📚 Learning Outcomes

Through this project, the following concepts were implemented and learned:

* Distributed systems
* Microservices architecture
* Event-driven systems
* Kafka streaming
* Docker deployment
* AI integration
* RAG pipelines
* JWT authentication
* PostgreSQL optimization
* System design concepts

---

# 🚀 Future Enhancements

* Kubernetes deployment
* Wearable device integration
* Real ML prediction models
* Mobile application
* Multi-hospital architecture
* Advanced analytics engine
* Real-time WebSocket updates
* Cloud deployment (AWS/GCP)

---

# 📜 License

```text
MIT License

Copyright (c) 2026 Gayatri Patil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use
the Software for personal, educational, and portfolio review purposes only.

Commercial usage, resale, redistribution, SaaS deployment,
AI model replication, or production deployment without explicit
written permission from the author is prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

# 👩‍💻 Author

## Gayatri Patil

* GitHub: [https://github.com/Gayatrip-26](https://github.com/Gayatrip-26)
* LinkedIn: [https://www.linkedin.com/in/gayatri-patil-524620283/](https://www.linkedin.com/in/gayatri-patil-524620283/)
* Portfolio: [https://Gayatrip-26.github.io/](https://Gayatrip-26.github.io/)

---

# ⭐ If you liked this project

Give this repository a ⭐ on GitHub to support the project.

```
```
