# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed packages
COPY --from=builder /root/.local /home/appuser/.local

# Copy app code
COPY . .

# Set PATH
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]