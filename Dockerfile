FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements-serving.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/python -m pip install --no-cache-dir -r requirements-serving.txt

COPY src/pipeline/ src/pipeline/
COPY src/train_final_model.py src/train_final_model.py
RUN /opt/venv/bin/python src/pipeline/collect.py \
    && /opt/venv/bin/python src/pipeline/preprocess.py \
    && /opt/venv/bin/python src/pipeline/features.py \
    && /opt/venv/bin/python src/train_final_model.py

FROM python:3.11-slim AS runtime

WORKDIR /app

RUN useradd --create-home appuser
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /build/models/ models/
COPY --chown=appuser:appuser src/serve.py src/serve.py

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)" || exit 1

USER appuser
CMD ["python", "src/serve.py"]
