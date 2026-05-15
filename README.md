# 🚑 LifeGuard AI 2.0 – Real-Time Predictive Health Intelligence Platform

A production-inspired **AI-powered healthcare monitoring platform** built using **FastAPI, ReactJS, Kafka, PostgreSQL, Redis, Docker, and RAG (ChromaDB)** for real-time health ingestion, AI-based risk prediction, and intelligent medical insights.

![Tech](https://img.shields.io/badge/Tech-FastAPI%20%7C%20React%20%7C%20Kafka%20%7C%20PostgreSQL%20%7C%20Docker-blue)
![AI](https://img.shields.io/badge/AI-RAG%20%7C%20ChromaDB%20%7C%20Transformers-green)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-orange)
![Status](https://img.shields.io/badge/Project_Status-Completed-success)

---

# 📌 Table of Contents

* [Overview](#-overview)
* [Aim of the Project](#-aim-of-the-project)
* [Objectives](#-objectives)
* [Key Features](#-key-features)
* [System Architecture](#-system-architecture)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Microservices Overview](#-microservices-overview)
* [Backend Setup](#-backend-setup)
* [Frontend Setup](#-frontend-setup)
* [Docker Setup](#-docker-setup)
* [Environment Variables](#-environment-variables)
* [API Overview](#-api-overview)
* [AI & RAG Pipeline](#-ai--rag-pipeline)
* [Authentication Flow](#-authentication-flow)
* [Database Design](#-database-design)
* [Screenshots](#-screenshots)
* [Future Improvements](#-future-improvements)
* [License](#-license)
* [Note](#-note)
* [Author](#-author)

---

# 🚀 Overview

**LifeGuard AI 2.0** is a real-time intelligent healthcare analytics platform designed to monitor patient health data continuously and generate AI-powered insights for early risk detection.

The system collects health vitals such as:

✔️ Heart Rate
✔️ Body Temperature
✔️ Stress Level
✔️ Sleep Hours

The platform processes these values using a **distributed event-driven microservices architecture** powered by **Kafka**, stores structured data in **PostgreSQL**, caches responses with **Redis**, and generates intelligent medical explanations using **RAG (Retrieval-Augmented Generation)** with **ChromaDB** and **Transformers**.

The project demonstrates concepts used in modern large-scale systems including:

✅ Distributed Systems
✅ Microservices
✅ Event-Driven Architecture
✅ AI-Powered Recommendations
✅ Real-Time Data Streaming
✅ JWT Authentication
✅ Dockerized Deployment
✅ Scalable Backend Engineering

---

# 🎯 Aim of the Project

The main aim of **LifeGuard AI 2.0** is to build a scalable AI-driven healthcare monitoring platform capable of:

* Collecting real-time patient health data
* Detecting abnormal health conditions
* Providing AI-generated medical insights
* Supporting scalable microservices communication
* Demonstrating production-grade backend architecture

---

# 🎯 Objectives

### ✔️ Real-Time Monitoring

Monitor patient health vitals continuously using streaming pipelines.

### ✔️ AI-Based Prediction

Predict health risks using AI processing pipelines and intelligent analysis.

### ✔️ Distributed System Design

Implement scalable communication using Kafka-based event streaming.

### ✔️ Secure Authentication

Protect patient data using JWT authentication and role isolation.

### ✔️ RAG-Based Medical Insights

Generate contextual AI explanations using vector search and retrieval pipelines.

### ✔️ Scalable Architecture

Design production-inspired infrastructure using Dockerized services.

---

# 🔑 Key Features

## 🔐 Authentication System

* JWT-based authentication
* Secure login and registration
* Password hashing using bcrypt
* Protected API routes

---

## 📊 Real-Time Health Monitoring

* Live patient vital ingestion
* Health trends visualization
* Risk monitoring dashboard
* Prediction processing pipeline

---

## 🤖 AI Health Insights

* AI-generated health explanations
* Risk analysis and recommendations
* Retrieval-Augmented Generation (RAG)
* Context-aware medical responses

---

## ⚡ Event-Driven Architecture

* Kafka-based communication
* Asynchronous health event streaming
* Decoupled microservices
* Scalable ingestion pipelines

---

## 🧠 RAG + Vector Database

* ChromaDB vector storage
* Semantic health knowledge retrieval
* Transformer embeddings
* AI-powered contextual reasoning

---

## 🐳 Dockerized Deployment

* Multi-container architecture
* Docker Compose orchestration
* Independent service deployment
* Easy scalability

---

# 🏗 System Architecture

```text
Frontend (React Dashboard)
            │
            ▼
     FastAPI Backend
            │
            ▼
   Kafka Event Streaming
            │
 ┌──────────┴──────────┐
 ▼                     ▼
Ingestion Service   Prediction Service
 │                     │
 ▼                     ▼
PostgreSQL         AI Risk Analysis
 │                     │
 ▼                     ▼
Redis Cache       RAG + ChromaDB
```

---

# 🛠 Tech Stack

# 🎨 Frontend

* ReactJS
* Tailwind CSS
* Recharts
* Axios
* React Router
* Leaflet Maps

---

# ⚙️ Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic
* JWT Authentication
* REST APIs

---

# 📦 Database & Storage

* PostgreSQL
* Redis
* ChromaDB

---

# ⚡ Streaming & Distributed Systems

* Apache Kafka
* Zookeeper
* Event-Driven Architecture
* Microservices

---

# 🤖 AI / Machine Learning

* Transformers
* Sentence Transformers
* RAG (Retrieval-Augmented Generation)
* Vector Embeddings

---

# 🐳 DevOps & Deployment

* Docker
* Docker Compose
* Uvicorn
* Environment Variables

---

# 📁 Project Structure

```text
LifeGuard_AI_2.0/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── charts/
│   └── services/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── auth/
│   └── database/
│
├── microservices/
│   ├── ingestion_service/
│   ├── prediction_service/
│   └── ai_service/
│
├── shared/
│   ├── kafka/
│   ├── utils/
│   └── schemas/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Microservices Overview

## 🩺 Ingestion Service

Responsible for:

* Receiving patient health data
* Validating incoming requests
* Publishing Kafka events

Runs on:

```text
http://localhost:8101
```

---

## 📈 Prediction Service

Responsible for:

* Consuming Kafka health events
* Running health-risk prediction logic
* Generating alerts

Runs on:

```text
http://localhost:8102
```

---

## 🤖 AI Service

Responsible for:

* RAG pipeline execution
* ChromaDB vector retrieval
* AI-generated explanations

---

# ⚙️ Backend Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/LifeGuard-AI-2.0.git
```

---

## 2️⃣ Navigate to Project

```bash
cd LifeGuard-AI-2.0
```

---

## 3️⃣ Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# 🎨 Frontend Setup

## 1️⃣ Navigate to Frontend

```bash
cd frontend
```

---

## 2️⃣ Install Dependencies

```bash
npm install
```

---

## 3️⃣ Run Frontend

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🐳 Docker Setup

## ▶️ Start Entire Project

```bash
docker compose up --build
```

---

## ▶️ Run in Background

```bash
docker compose up -d
```

---

## ▶️ Stop Containers

```bash
docker compose down
```

---

# 🔐 Environment Variables

Create `.env` file inside backend:

```env
DATABASE_URL=postgresql://postgres:password@postgres:5432/lifeguard
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
REDIS_HOST=redis
CHROMA_HOST=chromadb
```

---

# 📡 API Overview

# 🔐 Authentication APIs

## POST `/auth/register`

Registers a new user.

---

## POST `/auth/login`

Authenticates users and generates JWT token.

---

# 🩺 Health APIs

## POST `/health`

Stores patient health data.

Example Request:

```json
{
  "patient_id": "user_3",
  "user_id": 3,
  "heart_rate": 80,
  "temperature": 36,
  "stress_level": 30,
  "sleep_hours": 8,
  "timestamp": "2026-05-15T10:56:39.987Z"
}
```

---

## GET `/health/{user_id}`

Returns historical health records.

---

# 🤖 AI APIs

## POST `/ai/query`

Returns AI-generated health explanations and recommendations.

---

# 🧠 AI & RAG Pipeline

LifeGuard AI 2.0 uses **Retrieval-Augmented Generation (RAG)** to generate intelligent medical explanations.

### Pipeline Flow

1️⃣ User submits health data
2️⃣ Data stored in PostgreSQL
3️⃣ Kafka streams events
4️⃣ Prediction service analyzes risk
5️⃣ ChromaDB retrieves relevant medical context
6️⃣ Transformers generate AI explanation
7️⃣ Dashboard displays insights

---

# 🔐 Authentication Flow

```text
User Login
    │
    ▼
JWT Token Generated
    │
    ▼
Protected API Access
    │
    ▼
Secure Health Data Isolation
```

---

# 🗄 Database Design

## PostgreSQL Tables

### Users

* id
* email
* hashed_password
* created_at

### Health Records

* patient_id
* heart_rate
* temperature
* stress_level
* sleep_hours
* timestamp

---

# 📸 Screenshots

## 🔐 Login Page

![Login Page](screenshots/loginPage.png)

<p align="center">
  <em>User authentication page with secure JWT-based login system.</em>
</p>

---

## 📝 Registration Page

![Registration Page](screenshots/registrationPage.png)

<p align="center">
  <em>User registration interface for creating new LifeGuard AI accounts.</em>
</p>

---

## 🏠 Dashboard

![Dashboard](screenshots/healthdatainput.png)

<p align="center">
  <em>Main healthcare monitoring dashboard showing patient analytics and insights.</em>
</p>

---

## 📊 Health Analytics

![Health Analytics](screenshots/analysisgraph.png)

<p align="center">
  <em>Interactive cards displaying heart rate, stress level, temperature, and sleep trends.</em>
</p>

---

## 🤖 AI Health Insights

![AI Insights](screenshots/AIhealthInsights.png)

<p align="center">
  <em>RAG-based AI explanations and intelligent healthcare recommendations.</em>
</p>

---

## 📈 Prediction Monitoring

![Prediction Monitoring](screenshots/predictions.png)

<p align="center">
  <em>Prediction service dashboard showing health-risk analysis and processing.</em>
</p>

---

## 🧠 ChromaDB / AI Pipeline

![Health Data Ingestion](screenshots/backendinput.png)
<p align="center"><em>Real-time health data ingestion through FastAPI microservice with Kafka-based event streaming.</em></p>
![AI Health Insights](screenshots/queryaiexplanation.png)
<p align="center"><em>RAG-powered AI health analysis generating personalized risk explanations and medical recommendations.</em></p>

---

## 🐳 Docker Containers

![Docker Containers](screenshots/docker.png)

<p align="center">
  <em>Dockerized microservices architecture running multiple backend services.</em>
</p>

---

# 🚀 Future Improvements

* Wearable device integration
* Real ML prediction models
* SMS & email emergency alerts
* Kubernetes deployment
* Role-based doctor dashboards
* Real-time WebSocket streaming
* Multi-patient monitoring
* Cloud deployment on AWS/GCP

---

# 📜 License

## Custom Portfolio Showcase License

This project is provided strictly for:

✅ Portfolio showcase
✅ Educational purposes
✅ Recruiter evaluation

The following are **NOT permitted** without explicit permission:

❌ Commercial usage
❌ Re-distribution
❌ Re-selling
❌ Production deployment
❌ Copying core architecture for commercial projects

© 2026 Gayatri Patil. All Rights Reserved.

---

# ⚠️ Note

> This repository is a **portfolio showcase version** of LifeGuard AI 2.0.
>
> Some advanced production features, AI pipelines, internal optimizations, and enterprise-level infrastructure components are intentionally excluded from the public repository.

---

# 👩‍💻 Author

## Gayatri Patil

📧 Email: [gayatripp26@gmail.com](mailto:gayatripp26@gmail.com)

🐙 GitHub: [https://github.com/Gayatrip-26](https://github.com/Gayatrip-26)

💼 LinkedIn: [https://www.linkedin.com/in/gayatri-patil-524620283/](https://www.linkedin.com/in/gayatri-patil-524620283/)

---
