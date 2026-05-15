"""RAG utilities for medical knowledge retrieval."""

from app.rag.rag_service import query_medical_info
from app.rag.vector_store import ensure_medical_knowledge_loaded

__all__ = ["query_medical_info", "ensure_medical_knowledge_loaded"]
