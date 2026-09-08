# Student ML API

[![CI](https://github.com/Abdul-Mateen-1/student-ml-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Abdul-Mateen-1/student-ml-api/actions/workflows/ci.yml)
[![Release](https://github.com/Abdul-Mateen-1/student-ml-api/actions/workflows/release.yml/badge.svg)](https://github.com/Abdul-Mateen-1/student-ml-api/actions/workflows/release.yml)

A deterministic Flask prediction API used to demonstrate a professional MLOps workflow with protected pull requests, automated CI, Docker, semantic releases, and GitHub Container Registry.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Reports service, application, and model versions. |
| `POST` | `/predict` | Doubles a finite numeric `value`. |

Example prediction request:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"value": 10}'
```

Expected response:

```json
{"input": 10, "prediction": 20}
```

## Run locally

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest -v
python app.py
```

## Run the published image

```bash
docker pull ghcr.io/abdul-mateen-1/student-ml-api:1.1.0
docker run --rm -p 5000:5000 ghcr.io/abdul-mateen-1/student-ml-api:1.1.0
```

The complete assessed evidence is in [the assignment report](docs/assignment-report.md), with detailed [failure analysis](docs/failure-analysis.md) and [viva answers](docs/viva.md).
