FROM python:3.11-slim

ARG APPLICATION_VERSION="unknown"
ARG VCS_REF="unknown"
ARG REPOSITORY="unknown"
ARG BUILD_DATE="unknown"

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.description="Deterministic prediction API for an MLOps workflow demonstration" \
      org.opencontainers.image.version="${APPLICATION_VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="${REPOSITORY}" \
      org.opencontainers.image.created="${BUILD_DATE}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependencies first so application-only changes can reuse the install layer.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py VERSION ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
