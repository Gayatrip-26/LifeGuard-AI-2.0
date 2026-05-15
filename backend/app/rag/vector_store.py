import os
import re
from typing import Sequence

import chromadb
from chromadb.config import Settings

from app.core.config import settings
from app.rag.embeddings import get_embedding

COLLECTION_NAME = "medical_knowledge"

MEDICAL_KNOWLEDGE = [
    "High heart rate above 100 bpm may indicate stress, anxiety, dehydration, or cardiovascular issues.",
    "Fever above 38°C often indicates infection such as viral or bacterial illness.",
    "Low sleep less than 5 hours can lead to fatigue, reduced cognitive performance, and increased stress.",
    "High stress levels can cause anxiety, high blood pressure, and sleep disturbances.",
    "Dehydration can cause dizziness, fatigue, dry mouth, and increased heart rate.",
    "Prolonged high temperature and heart rate together may indicate serious infection or heat-related illness.",
    "Fatigue combined with stress and low sleep may lead to burnout and mental health issues.",
    "Severe dehydration may require immediate medical attention.",
    "Persistent fever should be monitored and treated appropriately.",
    "Irregular heart rate patterns may need medical evaluation.",
]

# 🔹 Cache (important)
_client = None
_collection = None


def _keyword_fallback(query: str, top_k: int) -> Sequence[str]:
    tokens = set(re.findall(r"[a-zA-Z]+", query.lower()))
    if not tokens:
        return MEDICAL_KNOWLEDGE[:top_k]

    ranked = sorted(
        MEDICAL_KNOWLEDGE,
        key=lambda doc: len(tokens.intersection(re.findall(r"[a-zA-Z]+", doc.lower()))),
        reverse=True,
    )
    return ranked[:top_k]


# ✅ 1. GET CLIENT (stable + no telemetry issues)
def _get_client():
    global _client

    if _client:
        return _client

    try:
        # Try HTTP (Docker Chroma)
        _client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
        )
    except Exception:
        # Fallback to local DB
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")

        _client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

    return _client


# ✅ 2. SAFE COLLECTION (NO CRASH VERSION)
def _get_collection():
    global _collection

    if _collection:
        return _collection

    client = _get_client()

    try:
        _collection = client.get_or_create_collection(name=COLLECTION_NAME)
    except Exception:
        _collection = client.get_collection(name=COLLECTION_NAME)

    return _collection


# ✅ 3. ADD DOCUMENTS (safe + no duplicate crash)
def add_documents(docs: list[str]) -> int:
    if not docs:
        return 0

    collection = _get_collection()

    try:
        current_count = collection.count()
        if current_count > 0:
            return 0

        ids = [f"doc_{i}" for i in range(current_count, current_count + len(docs))]
        embeddings = [get_embedding(doc) for doc in docs]

        collection.add(
            ids=ids,
            documents=docs,
            embeddings=embeddings,
        )

        return len(docs)

    except Exception as e:
        print("❌ Error adding documents:", e)
        return 0


# ✅ 4. QUERY DOCUMENTS (safe)
def query_documents(query: str, top_k: int = 3) -> Sequence[str]:
    try:
        collection = _get_collection()

        if collection.count() == 0:
            return _keyword_fallback(query, top_k)

        result_count = min(top_k, collection.count())
        if result_count <= 0:
            return []

        result = collection.query(
            query_embeddings=[get_embedding(query)],
            n_results=result_count,
            include=["documents"],
        )

        documents = result.get("documents", [[]])
        return documents[0] if documents else []

    except Exception as e:
        print("❌ Query error:", e)
        return _keyword_fallback(query, top_k)


# ✅ 5. LOAD DEFAULT DATA (only once)
def ensure_medical_knowledge_loaded() -> None:
    try:
        collection = _get_collection()

        existing = collection.count()
        if existing == 0:
            print("📚 Loading medical knowledge...")
            add_documents(MEDICAL_KNOWLEDGE)

    except Exception as e:
        print(f"⚠️ Chroma init error: {e}")