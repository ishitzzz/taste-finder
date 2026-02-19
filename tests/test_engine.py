from app.engine import infer_taste_vector, recommend


def test_infer_taste_vector_prioritizes_expected_dimensions():
    profile = infer_taste_vector(
        [
            {"domain": "music", "text": "I love minimal ambient and elegant sounds"},
            {"domain": "film", "text": "Retro heartfelt stories"},
        ]
    )

    assert profile.vector["minimalism"] > 0
    assert profile.vector["nostalgia"] > 0
    assert profile.vector["sophistication"] > 0
    assert len(profile.top_dimensions) == 3


def test_recommend_returns_ranked_results():
    profile = infer_taste_vector(
        [{"domain": "design", "text": "minimal elegant clean experimental"}]
    )
    recs = recommend(profile, limit=3)

    assert len(recs) == 3
    assert recs[0].similarity >= recs[1].similarity >= recs[2].similarity
