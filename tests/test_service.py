from app.service import build_recommendation_payload


def test_build_recommendation_payload_shape():
    payload = build_recommendation_payload(
        [
            {"domain": "music", "text": "minimal elegant ambient"},
            {"domain": "books", "text": "retro heartfelt stories"},
        ],
        limit=4,
    )

    assert "profile" in payload
    assert "vector" in payload["profile"]
    assert "recommendations" in payload
    assert len(payload["recommendations"]) == 4
