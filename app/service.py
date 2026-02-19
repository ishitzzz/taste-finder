from __future__ import annotations

from app.engine import infer_taste_vector, recommend


def build_recommendation_payload(signals: list[dict[str, str]], limit: int = 6) -> dict:
    profile = infer_taste_vector(signals)
    recs = recommend(profile, limit=limit)
    return {
        "profile": {
            "vector": profile.vector,
            "top_dimensions": profile.top_dimensions,
        },
        "recommendations": [r.__dict__ for r in recs],
    }
