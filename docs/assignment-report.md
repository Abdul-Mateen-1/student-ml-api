# MLOps Assignment Evidence Report

## Repository and workflow

- Repository: <https://github.com/Abdul-Mateen-1/student-ml-api>
- Container package: <https://github.com/Abdul-Mateen-1/student-ml-api/pkgs/container/student-ml-api>
- PR #1, prediction API: <https://github.com/Abdul-Mateen-1/student-ml-api/pull/1>
- PR #2, model metadata: <https://github.com/Abdul-Mateen-1/student-ml-api/pull/2>

Development followed `feature branch -> pull request -> CI -> merge -> semantic tag -> release workflow -> GHCR`. No application work was pushed directly to `main`, and no image was manually pushed to the registry.

## Application and tests

Version 1.1.0 exposes:

```json
{"status":"healthy","application":"student-ml-api","application_version":"1.1.0","model_version":"model-1"}
```

`POST /predict` applies the deterministic formula `prediction = value * 2`. It rejects absent values, non-numeric values, booleans, non-finite numbers, and malformed JSON with explicit HTTP 400 errors.

The local suite collected eight tests and completed with:

```text
============================== 8 passed in 0.22s ==============================
```

## Local Docker validation for 1.0.0

Commands used included:

```bash
docker build -t student-ml-api:1.0.0 .
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
curl http://localhost:5000/health
docker images student-ml-api
docker ps --filter name=student-ml-api
docker logs student-ml-api
docker inspect student-ml-api
docker exec student-ml-api sh -c 'pwd; python --version'
```

Observed runtime evidence:

| Item | Actual value |
| --- | --- |
| Health response | `{"application":"student-ml-api","status":"healthy","version":"1.0.0"}` |
| Container ID | `e5714fc71223ab6e693d7dbcaff469a61c6f2834201551a8cb7302d081a98664` |
| Local image ID | `sha256:952ae55e7e4a8dcb9b9879b063dd326689951479b5d3610563e8e6c9ce285d30` |
| Published port | `0.0.0.0:5000 -> 5000/tcp` |
| Working directory | `/app` |
| Python in image | `3.11.16` |
| Running command | `gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 2 --timeout 30 app:app` |

Gunicorn logged `Listening at: http://0.0.0.0:5000`, proving that the application is reachable outside the container rather than being bound only to loopback.

## Pull requests and CI evidence

| Evidence | Commit/run | Result |
| --- | --- | --- |
| Initial PR #1 CI | [run 34268279150](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268279150) | Passed |
| Mandatory deliberate failure | [run 34268383240](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268383240) at `99e2cc4` | Failed: 1 failed, 7 passed |
| Corrected PR #1 CI | [run 34268503774](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268503774) at `e1297e7` | Passed |
| PR #2 CI | [run 34269268257](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34269268257) | Passed |

The deliberate failure asserted `wrong` instead of `healthy`. GitHub Actions reported:

```text
tests/test_app.py::test_health FAILED
{'status': 'healthy'} != {'status': 'wrong'}
========================= 1 failed, 7 passed in 0.18s ==========================
Error: Process completed with exit code 1.
```

Commit `e1297e7` (`fix: correct health endpoint test`) restored the correct assertion and turned the PR green before merge.

## Branch protection

The `main` branch protection API reported these active settings:

- Pull requests are required, with zero mandatory approvals because this is an individual repository where an author cannot approve their own PR.
- Strict required status check: `Test and build`; strict mode requires the branch to be current with `main`.
- Administrator enforcement is enabled, so the repository owner does not silently bypass the rule.
- Conversation resolution is required.
- Force pushes and branch deletion are disabled.

These controls keep unvalidated commits out of `main`, make CI a merge gate, and preserve the release history.

## Merge strategy

Both feature PRs used merge commits. This keeps each meaningful conventional commit, including the deliberate failure and its correction, while also creating an explicit merge SHA that links each PR to a release. That history is especially useful for the assignment's audit and traceability requirements.

## Releases and registry

Only `.github/workflows/release.yml` publishes images. It is triggered by `v*.*.*`, validates the semantic tag, derives the image version by removing the leading `v`, runs the tests, logs into GHCR with `secrets.GITHUB_TOKEN`, and publishes version, `latest`, and short-commit-SHA tags.

| Version | Release run | Merge commit / SHA tag | Registry digest |
| --- | --- | --- | --- |
| 1.0.0 | [34268731623](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34268731623) | `d4e8daaa330af5985deb648050b8c9486722ebdf` / `d4e8daa` | `sha256:01435066e6d602c7c9350df578a05d58af7787f66f6a28690079dd92395b2664` |
| 1.1.0 | [34269374544](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34269374544) | `2990b54f1534fb8850472b25d597eb95f59fa50c` / `2990b54` | `sha256:1a4b2e0979fe3e16021ca5fe28cedc910f4e14d76d160797f3621f8c1d980b39` |
| latest | [34269374544](https://github.com/Abdul-Mateen-1/student-ml-api/actions/runs/34269374544) | Resolves to 1.1.0 | `sha256:1a4b2e0979fe3e16021ca5fe28cedc910f4e14d76d160797f3621f8c1d980b39` |

OCI inspection of the published 1.0.0 image recorded version `1.0.0`, revision `d4e8daaa330af5985deb648050b8c9486722ebdf`, repository URL, and UTC build time. The 1.1.0 commit tag `2990b54` resolves to the same digest as 1.1.0 and `latest`. A commit-specific tag permits exact deployment even if a mutable convenience tag moves.

## Version 1.1.0 traceability chain

```text
PR #2
  -> merge commit 2990b54f1534fb8850472b25d597eb95f59fa50c
  -> Git tag v1.1.0
  -> ghcr.io/abdul-mateen-1/student-ml-api:1.1.0
  -> sha256:1a4b2e0979fe3e16021ca5fe28cedc910f4e14d76d160797f3621f8c1d980b39
```

## Reproducibility and rollback

The local `student-ml-api:1.0.0` image and its running container were removed. The command below then downloaded the release artifact rather than rebuilding source:

```bash
docker pull ghcr.io/abdul-mateen-1/student-ml-api:1.0.0
docker run -d --name student-ml-api-rollback -p 5002:5000 \
  ghcr.io/abdul-mateen-1/student-ml-api:1.0.0
curl http://localhost:5002/health
```

Observed response:

```json
{"application":"student-ml-api","status":"healthy","version":"1.0.0"}
```

The pull reported digest `sha256:01435066e6d602c7c9350df578a05d58af7787f66f6a28690079dd92395b2664`. Registry rollback is faster and safer than `git clone`, dependency installation, and direct execution because it starts the exact already-tested immutable artifact; it avoids build-time dependency drift and eliminates an emergency rebuild.

## CI and release responsibility

PR CI tests proposed code and validates that its Docker image can build, but it does not publish an artifact. Publishing every PR would fill the registry with unreviewed images, create ambiguous versions, and increase the impact of untrusted changes. The release workflow runs only for an approved semantic tag on merged history, repeats the tests, derives the version, attaches source metadata, and publishes the distributable artifact. This separation makes registry contents intentional, auditable releases rather than temporary review builds.

## Docker layer caching experiment

After a baseline build, only `app.py` was changed. Docker reported `CACHED` for `WORKDIR`, `COPY requirements.txt`, and `RUN pip install`; only `COPY app.py VERSION` and image export ran again, completing in about 0.5 seconds after metadata loading.

Next, `requirements.txt` alone was changed. `COPY requirements.txt` ran again and invalidated `RUN pip install`, which redownloaded/reinstalled packages and took about 15 seconds before the application copy ran. The order `COPY requirements.txt`, `RUN pip install`, then `COPY app.py VERSION` isolates the expensive dependency layer from frequent source edits; copying the whole repository first would invalidate dependency installation on every application change.

## Final checklist

- [x] Required application, test, Docker, version, and workflow files exist.
- [x] At least two professionally documented PRs are preserved.
- [x] One failed CI run, multiple successful CI runs, and successful release runs are linked.
- [x] GHCR contains immutable 1.0.0 and 1.1.0 tags, `latest`, and commit-SHA tags.
- [x] Git tags `v1.0.0` and `v1.1.0` exist.
- [x] Registry pull and rollback to 1.0.0 were demonstrated without rebuilding.
- [x] The 1.1.0 traceability chain contains real repository and registry values.
- [x] Two failure scenarios are documented in `docs/failure-analysis.md`.
- [x] Viva answers are prepared in `docs/viva.md`.
