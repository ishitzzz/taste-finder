# Taste Finder (MVP)

A starter product for inferring a person's cross-domain taste and recommending people/items with a similar vibe.

## What's included
- Taste inference engine with weighted dimensions.
- Similarity-based recommendation ranking.
- Starter catalog (`data/catalog.json`).
- CLI for fast experiments.
- Minimal modern web app (sans-serif aesthetic) with live taste analysis.

## Run the web app
```bash
python -m app.web
```
Then open `http://localhost:8000`.

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

## Next step ideas
- Save user profiles and feedback in Postgres.
- Replace keyword mapping with embeddings + LLM enrichment.
- Add social matching (people-to-people taste alignment).
