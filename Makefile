.PHONY: test run-web run-cli doctor

test:
	pytest -q

run-web:
	python -m app.web

run-cli:
	python -m app.cli --signal "music:minimal elegant ambient" --signal "film:retro heartfelt stories"

doctor:
	python scripts/doctor.py
