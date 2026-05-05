# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel jaraco.context && \
    pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

RUN pip install --no-cache-dir --upgrade pip setuptools wheel jaraco.context

COPY --from=builder /root/.local /home/appuser/.local

COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]