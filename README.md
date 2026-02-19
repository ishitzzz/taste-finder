# Taste Finder (MVP)

A starter backend engine for a platform that infers a person's multi-domain taste and recommends aligned items/people.

## What this MVP does
- Accepts preference signals (music, film, books, design, etc.).
- Infers a normalized taste vector across key taste dimensions.
- Recommends catalog entities by vector similarity with simple explanations.

## Run CLI
```bash
python -m app.cli \
  --signal "music:minimal elegant ambient" \
  --signal "film:retro heartfelt stories"
```

## Test
```bash
pytest -q
```

## Next step
Wire this engine behind an API (FastAPI or similar), add persistence, and connect it to real catalogs and user feedback loops.
