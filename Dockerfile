# ===============================
# Builder Stage
# ===============================
FROM python:3.10-slim AS builder

ENV PIP_NO_CACHE_DIR=1
ENV HF_HOME=/root/.cache
ENV TRANSFORMERS_CACHE=/root/.cache
ENV HF_HUB_DISABLE_TELEMETRY=1

WORKDIR /build

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only Torch first
RUN pip install torch==2.0.1+cpu \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding model
RUN python - <<EOF
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
print("Embedding model cached")
EOF

# Make sure cache exists (important)
RUN mkdir -p /root/.cache


# ===============================
# Runtime Stage
# ===============================
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HOME=/app/.cache

WORKDIR /app

# Copy installed packages
COPY --from=builder /usr/local /usr/local

# Copy HuggingFace model cache
COPY --from=builder /root/.cache /app/.cache

# Copy application code
COPY app ./app
COPY frontend ./frontend

# Create non-root user
RUN useradd -m appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Production server (2 workers)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]


# # Builder
# # ===============================
# FROM python:3.10-slim AS builder

# ENV PIP_NO_CACHE_DIR=1
# WORKDIR /build

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # ---- Install CPU-only Torch FIRST ----
# RUN pip install --upgrade pip && \
#     pip install torch==2.0.1 \
#       --index-url https://download.pytorch.org/whl/cpu

# # ---- Install runtime deps ----
# COPY requirements-runtime.txt .
# RUN pip install --no-cache-dir -r requirements-runtime.txt

# # ---- Pre-download embedding model ----
# RUN python - <<EOF
# from sentence_transformers import SentenceTransformer
# SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
# print("✅ Embedding model cached")
# EOF

# # ===============================
# # Runtime
# # ===============================
# FROM python:3.10-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV TRANSFORMERS_OFFLINE=1
# ENV HF_HUB_DISABLE_TELEMETRY=1
# ENV HF_HOME=/app/.cache

# WORKDIR /app

# # Copy libs + model cache
# COPY --from=builder /usr/local /usr/local
# COPY --from=builder /root/.cache /app/.cache

# # App code
# COPY app ./app
# COPY frontend ./frontend

# # Non-root user
# RUN useradd -m appuser \
#     && mkdir -p /app/data \
#     && chown -R appuser:appuser /app

# USER appuser

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
