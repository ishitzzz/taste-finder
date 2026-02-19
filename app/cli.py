from __future__ import annotations

import argparse
import json

from app.engine import infer_taste_vector, recommend


def main() -> None:
    parser = argparse.ArgumentParser(description="Taste Finder CLI")
    parser.add_argument(
        "--signal",
        action="append",
        default=[],
        help="Signal in the form domain:text (e.g., music:minimal elegant ambient)",
    )
    args = parser.parse_args()

    signals = []
    for entry in args.signal:
        if ":" not in entry:
            continue
        domain, text = entry.split(":", 1)
        signals.append({"domain": domain.strip(), "text": text.strip()})

    profile = infer_taste_vector(signals)
    recommendations = recommend(profile)

    output = {
        "profile": {
            "vector": profile.vector,
            "top_dimensions": profile.top_dimensions,
        },
        "recommendations": [r.__dict__ for r in recommendations],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
