# Taste Finder — Implementation Plan

## 1) Product definition and scope
- **Goal:** infer a user's cross-domain taste profile (music, books, films, fashion, design, hobbies, etc.) and use it for recommendations.
- **MVP outcome:** users submit preferences; system returns
  - a normalized **taste profile** (dimensions + confidence)
  - recommended **items** and **people/profiles** with explanation tags.

## 2) Core data model
- `UserPreferenceInput`
  - free text likes/dislikes
  - optional explicit picks by domain
- `TasteProfile`
  - weighted vector over dimensions (e.g., minimalism, energy, nostalgia, experimental, sophistication, warmth)
  - domain-specific sub-vectors
  - confidence score per dimension
- `CatalogEntity`
  - item or person
  - domains covered
  - precomputed taste vector + tags

## 3) Inference layer (MVP -> advanced)
### MVP (now)
- Keyword + tag mapping into taste dimensions.
- Aggregate and normalize into profile vector.
- Calculate similarity with cosine score against catalog entities.

### Next
- LLM-assisted tagging for nuanced text understanding.
- Embedding-based representation (sentence/document embeddings).
- Hybrid score: metadata match + embedding similarity + diversity term.

## 4) Recommendation logic
- Score entities by similarity with user taste vector.
- Add constraints:
  - variety across domains
  - novelty/exploration (not only nearest neighbors)
  - optional social graph signal (people with similar profile)
- Return rationale (`matched_tags`, top dimensions).

## 5) Platform architecture
- **API service:** FastAPI app exposing profile + recommendation endpoints.
- **Data store:** Postgres (users, preferences, entities, interactions).
- **Search/vector index:** pgvector or dedicated vector DB.
- **Offline jobs:** profile recomputation, popularity priors, cold-start bootstrapping.

## 6) Learning loop
- Collect feedback (`save`, `skip`, `not my vibe`, follow user).
- Update profile weights online.
- Track quality metrics:
  - CTR / save-rate
  - long-term retention
  - recommendation diversity
  - explicit “relatability” score.

## 7) Privacy and trust
- Explainability controls (“why this recommendation”).
- Per-domain opt out.
- Data deletion/export.
- Avoid sensitive trait inference from taste.

## 8) Build milestones
1. **MVP API**: profile inference + recommendations (this commit).
2. Add persistence (Postgres).
3. Add auth and user onboarding quiz.
4. Add LLM/embedding inference and richer catalog ingestion.
5. Add feedback learning and analytics dashboards.
