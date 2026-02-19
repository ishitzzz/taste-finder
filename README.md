# Taste Finder (MVP)

A starter product for inferring a person's cross-domain taste and recommending people/items with a similar vibe.

## What's included
- Taste inference engine with weighted dimensions.
- Similarity-based recommendation ranking.
- Starter catalog (`data/catalog.json`).
- CLI for fast experiments.
- Minimal modern web app (sans-serif aesthetic) with live taste analysis.

---

## Vibecoder quickstart (Codespaces/local)

### 1) Go to the repo root (important)
In your screenshot, the failing command used `/workspace/taste-finder`.
In Codespaces, the path is usually `/workspaces/taste-finder` (plural).

```bash
cd /workspaces/taste-finder
pwd
```

You should see the folder that contains `app/`, `web/`, and `README.md`.

### 2) Sanity check your environment
```bash
make doctor
```

### 3) Run tests
```bash
make test
```

### 4) Start the web app
```bash
make run-web
```
Then open:
- `http://localhost:8000`

### 5) CLI smoke test
```bash
make run-cli
```

---

## API test commands (while web server is running)

### Health
```bash
curl -s http://127.0.0.1:8000/api/health
```

### Recommendation
```bash
curl -s -X POST http://127.0.0.1:8000/api/recommend \
  -H 'Content-Type: application/json' \
  -d '{
    "signals": [
      {"domain": "music", "text": "minimal elegant ambient"},
      {"domain": "film", "text": "retro heartfelt stories"}
    ]
  }'
```

---

## Common issues (exactly what happened in your screenshot)

### `bash: cd: /workspace/taste-finder: No such file or directory`
Use the correct Codespaces path:
```bash
cd /workspaces/taste-finder
```

### `No module named app.web`
Usually one of these:
1. You are **not in repo root**.
2. You are on an **older commit/branch** where `app/web.py` is missing.

Fix:
```bash
cd /workspaces/taste-finder
ls app
# should include: web.py
```

If `web.py` is missing:
```bash
git pull
# or switch to the branch with latest changes
```

---

## Next step ideas
- Save user profiles and feedback in Postgres.
- Replace keyword mapping with embeddings + LLM enrichment.
- Add social matching (people-to-people taste alignment).
