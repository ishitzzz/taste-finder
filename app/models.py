from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TasteDimension = Literal[
    "minimalism",
    "energy",
    "nostalgia",
    "experimental",
    "sophistication",
    "warmth",
]


@dataclass
class PreferenceSignal:
    domain: str
    text: str


@dataclass
class TasteProfileResponse:
    vector: dict[TasteDimension, float]
    top_dimensions: list[TasteDimension]


@dataclass
class RecommendationItem:
    id: str
    entity_type: Literal["item", "person"]
    title: str
    domains: list[str]
    similarity: float
    matched_dimensions: list[TasteDimension]


@dataclass
class RecommendationResponse:
    profile: TasteProfileResponse
    recommendations: list[RecommendationItem]
