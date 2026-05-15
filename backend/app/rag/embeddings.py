# from sentence_transformers import SentenceTransformer

# MODEL_NAME = "all-MiniLM-L6-v2"
# _model = SentenceTransformer(MODEL_NAME)


# def get_embedding(text: str) -> list[float]:
#     """Return embedding vector for a text query/document."""
#     embedding = _model.encode(text, convert_to_numpy=True)
#     return embedding.tolist()
def get_embedding(text: str) -> list[float]:
    """
    Lightweight embedding fallback.
    Converts text into a simple numeric representation.
    """

    # simple hash-based embedding (fast & no ML)
    return [float(ord(c)) / 1000 for c in text[:100]]