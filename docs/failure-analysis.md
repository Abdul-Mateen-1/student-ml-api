# Failure Analysis

## 1. Failed pytest in pull-request CI

### Symptom

GitHub Actions run [34268383240](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268383240) completed with `failure`, preventing PR #1 from being merge-ready.

### Root cause

The deliberate demonstration commit `99e2cc4` changed the expected `/health` status from `healthy` to `wrong`. The application remained correct, so the test contract intentionally disagreed with the response.

### Evidence

```text
tests/test_app.py::test_health FAILED
Differing items:
{'status': 'healthy'} != {'status': 'wrong'}
========================= 1 failed, 7 passed in 0.18s ==========================
Error: Process completed with exit code 1.
```

### Correction

Commit `e1297e7` restored the expected value to `healthy`. Local pytest reported `8 passed`, and Actions run [34268503774](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268503774) passed before PR #1 was merged.

## 2. Wrong container port mapping

### Symptom

The version 1.1.0 image was started with host port 5003 mapped to container port 5001. A request to `http://localhost:5003/health` returned `curl: (52) Empty reply from server` with exit code 52.

### Root cause

Gunicorn listens on container port 5000, but `-p 5003:5001` forwarded traffic to unused port 5001 inside the container.

### Evidence

```text
5001/tcp -> 0.0.0.0:5003
[INFO] Listening at: http://0.0.0.0:5000 (1)
curl: (52) Empty reply from server
curl_exit=52
```

The port report and server log show the mismatch directly.

### Correction

The test container was replaced using `-p 5003:5000`. The mapping then reported `5000/tcp -> 0.0.0.0:5003`, and `/health` returned:

```json
{"application":"student-ml-api","application_version":"1.1.0","model_version":"model-1","status":"healthy"}
```
