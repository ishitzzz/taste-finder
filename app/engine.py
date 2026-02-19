from __future__ import annotations

import json
import math
from pathlib import Path

from app.models import RecommendationItem, TasteDimension, TasteProfileResponse

DIMENSIONS: list[TasteDimension] = [
    "minimalism",
    "energy",
    "nostalgia",
    "experimental",
    "sophistication",
    "warmth",
]

KEYWORD_WEIGHTS: dict[str, dict[TasteDimension, float]] = {
    "minimal": {"minimalism": 1.0, "sophistication": 0.4},
    "clean": {"minimalism": 0.7, "sophistication": 0.3},
    "hype": {"energy": 1.0},
    "intense": {"energy": 0.9, "experimental": 0.2},
    "vintage": {"nostalgia": 1.0, "warmth": 0.4},
    "retro": {"nostalgia": 0.9, "warmth": 0.4},
    "experimental": {"experimental": 1.0, "energy": 0.2},
    "avant": {"experimental": 0.8, "sophistication": 0.2},
    "elegant": {"sophistication": 1.0, "minimalism": 0.4},
    "luxury": {"sophistication": 0.9, "warmth": 0.1},
    "cozy": {"warmth": 1.0, "nostalgia": 0.3},
    "heartfelt": {"warmth": 0.9, "nostalgia": 0.2},
}

DOMAIN_WEIGHTS: dict[str, float] = {
    "music": 1.1,
    "film": 1.0,
    "books": 1.0,
    "fashion": 1.1,
    "design": 1.2,
    "hobbies": 0.9,
    "sports": 0.8,
}


def _normalize(vector: dict[TasteDimension, float]) -> dict[TasteDimension, float]:
    norm = math.sqrt(sum(v * v for v in vector.values()))
    if norm == 0:
        return {k: 0.0 for k in DIMENSIONS}
    return {k: round(v / norm, 4) for k, v in vector.items()}


def infer_taste_vector(signals: list[dict[str, str]]) -> TasteProfileResponse:
    vector: dict[TasteDimension, float] = {k: 0.0 for k in DIMENSIONS}

    for signal in signals:
        domain = signal.get("domain", "").lower().strip()
        text = signal.get("text", "").lower()
        domain_weight = DOMAIN_WEIGHTS.get(domain, 1.0)

        for token, weights in KEYWORD_WEIGHTS.items():
            if token in text:
                for dim, score in weights.items():
                    vector[dim] += score * domain_weight

    normalized = _normalize(vector)
    top_dimensions = sorted(normalized, key=normalized.get, reverse=True)[:3]
    return TasteProfileResponse(vector=normalized, top_dimensions=top_dimensions)


def _cosine_similarity(a: dict[TasteDimension, float], b: dict[TasteDimension, float]) -> float:
    dot = sum(a[k] * b[k] for k in DIMENSIONS)
    norm_a = math.sqrt(sum(a[k] * a[k] for k in DIMENSIONS))
    norm_b = math.sqrt(sum(b[k] * b[k] for k in DIMENSIONS))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def load_catalog(path: str | Path = "data/catalog.json") -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def recommend(profile: TasteProfileResponse, limit: int = 5) -> list[RecommendationItem]:
    catalog = load_catalog()
    results: list[RecommendationItem] = []

    for entity in catalog:
        entity_vector = entity["vector"]
        similarity = _cosine_similarity(profile.vector, entity_vector)

        ranked_dims = sorted(
            DIMENSIONS,
            key=lambda d: min(profile.vector[d], entity_vector[d]),
            reverse=True,
        )[:2]

        results.append(
            RecommendationItem(
                id=entity["id"],
                entity_type=entity["entity_type"],
                title=entity["title"],
                domains=entity["domains"],
                similarity=round(similarity, 4),
                matched_dimensions=ranked_dims,
            )
        )

    return sorted(results, key=lambda r: r.similarity, reverse=True)[:limit]
