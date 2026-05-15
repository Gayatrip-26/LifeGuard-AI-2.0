from app.rag.vector_store import query_documents

_cache: dict[str, dict] = {}


def _keyword_recommendations(combined_text: str) -> list[str]:
    t = combined_text.lower()
    actions: list[str] = []
    if "dehydration" in t:
        actions.extend(
            [
                "Increase oral hydration with water or electrolyte fluids",
                "Avoid alcohol and excessive caffeine until hydration improves",
            ]
        )
    if "stress" in t:
        actions.extend(
            [
                "Practice brief daily relaxation (breathing, walk, or mindfulness)",
                "Prioritize sleep and consider mental health support if stress persists",
            ]
        )
    if "fever" in t:
        actions.extend(
            [
                "Monitor temperature on a regular schedule",
                "Rest, maintain fluid intake, and seek care if fever is high or prolonged",
            ]
        )
    # De-dupe preserving order
    seen: set[str] = set()
    unique = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            unique.append(a)
    return unique


def _default_actions() -> list[str]:
    return [
        "Track symptoms and vital signs you have been asked to monitor",
        "Rest as needed and contact a clinician if symptoms worsen",
    ]


def query_medical_info(
    query: str,
    patient_history_summary: str | None = None,
) -> dict:
    q = (query or "").strip()
    hist = (patient_history_summary or "").strip()
    cache_key = f"{q}|{hist}"
    if cache_key in _cache:
        return dict(_cache[cache_key])

    results = query_documents(q, top_k=3)

    history_block = ""
    if hist:
        history_block = f"Patient history insight:\n{hist}\n\n"

    if not results:
        recs = _keyword_recommendations(f"{q} {hist}")
        if not recs:
            recs = _default_actions()
        rec_lines = "\n".join(f"- {r}" for r in recs)
        answer = f"""{history_block}No matching reference passages were retrieved for this query.

Recommended Actions:
{rec_lines}

This information is educational only and does not replace professional medical advice."""
        out = {"answer": answer.strip(), "recommended_actions": recs}
        _cache[cache_key] = out
        return dict(out)

    context = " ".join(results)
    combined = f"{q} {context} {hist}"
    keyword_recs = _keyword_recommendations(combined)
    base_recs = [
        "Drink fluids if you may be dehydrated or unwell",
        "Take rest and avoid overexertion while symptoms evolve",
        "Monitor temperature or other vitals if infection is a concern",
    ]
    recs = keyword_recs + [b for b in base_recs if b not in keyword_recs]
    if not recs:
        recs = _default_actions()

    rec_lines = "\n".join(f"- {r}" for r in recs)
    answer = f"""{history_block}Based on your health data, here is an analysis:

{context}

Recommended Actions:
{rec_lines}

Please monitor your symptoms and consult a medical professional if conditions worsen."""

    out = {"answer": answer.strip(), "recommended_actions": recs}
    _cache[cache_key] = out
    return dict(out)
