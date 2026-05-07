# DevSecOps FastAPI Platform

A production-style DevSecOps backend platform built with FastAPI, PostgreSQL, Redis, Docker Compose, Prometheus, Grafana, GitHub Actions, and Terraform.

This project was implemented as part of a DevSecOps engineering assessment focused on secure software delivery, observability, CI/CD automation, and operational readiness.

---

# Features

- FastAPI REST API
- PostgreSQL database integration
- Redis containerized service support
- Nginx reverse proxy
- Dockerized application stack
- Prometheus metrics
- Grafana dashboards
- Structured JSON logging
- API key authentication
- Request rate limiting
- Payload validation
- Alembic database migrations
- Graceful shutdown handling
- GitHub Actions CI/CD
- Bandit SAST scanning
- Trivy vulnerability scanning
- SBOM generation
- GHCR container publishing
- Terraform infrastructure configuration

---

# Architecture

```text
Client
   │
   ▼
Nginx Reverse Proxy
   │
   ▼
FastAPI Application
   ├── PostgreSQL
   ├── Redis
   ├── Prometheus Metrics
   └── Structured JSON Logs

Prometheus ───► Grafana
```

---

# Project Structure

```text
.
├── app/
├── monitoring/
│   ├── grafana/
│   └── prometheus/
├── migrations/
├── infra/
│   └── terraform/
├── tests/
├── .github/workflows/
├── docker-compose.yml
├── docker-compose.observability.yml
├── Dockerfile
├── alembic.ini
├── DECISIONS.md
├── INCIDENT.md
└── README.md
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| Database | PostgreSQL |
| Service Store | Redis |
| Reverse Proxy | Nginx |
| Metrics | Prometheus |
| Dashboards | Grafana |
| CI/CD | GitHub Actions |
| Security Scanning | Bandit + Trivy |
| Container Registry | GHCR |
| IaC | Terraform |

---

# Prerequisites

Install:

- Docker
- Docker Compose
- Python 3.11+
- Git

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@db:5432/appdb
API_KEY=mysecretkey
SHUTDOWN_TIMEOUT_SECONDS=10
```

---

# Running the Application

## Start Core Stack

```bash
docker compose up --build
```

Application:

```text
http://localhost:8080
```

---

# Running Observability Stack

```bash
docker compose -f docker-compose.yml -f docker-compose.observability.yml up --build
```

---

# Local Service URLs

| Service | URL |
|---|---|
| FastAPI API | http://localhost:8080 |
| FastAPI Metrics | http://localhost:8080/metrics |
| FastAPI Health | http://localhost:8080/health |
| Prometheus | http://localhost:9090 |
| Prometheus Health | http://localhost:9090/-/healthy |
| Grafana | http://localhost:3000 |

Grafana default credentials:

```text
admin / admin
```

---

# API Endpoints

## Health Check

```bash
curl http://localhost:8080/health
```

Response:

```json
{"status":"ok"}
```

---

## Create Data

```bash
curl -X POST http://localhost:8080/data \
-H "Content-Type: application/json" \
-H "X-API-Key: mysecretkey" \
-d '{"user_id":"1","payload":"test"}'
```

---

## Get Data

```bash
curl http://localhost:8080/data/1 \
-H "X-API-Key: mysecretkey"
```

---

# Validation

Request payloads are validated using Pydantic.

Oversized payloads are rejected with:

```text
HTTP 422 Unprocessable Entity
```

---

# Rate Limiting

Rate limiting is implemented using SlowAPI.

| Endpoint | Limit |
|---|---|
| POST /data | 5 requests/minute |
| GET /data/{id} | 10 requests/minute |

---

# Database Migrations

Alembic is used for schema migrations.

Generate migration:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/appdb alembic revision --autogenerate -m "migration_name"
```

Apply migrations:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/appdb alembic upgrade head
```

---

# Running Tests

```bash
pytest
```

---

# CI/CD Pipeline

GitHub Actions pipeline includes:

- Dependency installation
- Flake8 linting
- Unit tests
- Bandit SAST scanning
- Docker image build
- Trivy vulnerability scanning
- GHCR image publishing
- SBOM generation

High and critical vulnerabilities detected by Trivy fail the pipeline.

---

# Observability

## Prometheus

Metrics endpoint:

```text
/metrics
```

## Grafana

Grafana dashboards visualize:

- Request traffic
- Error rate
- Request latency
- Service activity

---

# Structured Logging

Application events are logged in structured JSON format.

Example:

```json
{
  "event": "create_data",
  "user_id": "1"
}
```

---

# Security Features

- API key authentication
- Request payload validation
- Rate limiting
- Vulnerability scanning
- Secrets excluded from Git
- SBOM generation

---

# Infrastructure as Code

Terraform configuration is included under:

```text
infra/terraform/
```

The Terraform setup includes:

- AWS VPC
- Security Group
- Remote-state configuration placeholder

The infrastructure configuration was intentionally kept lightweight for assessment/demo purposes and was not applied to avoid unnecessary cloud cost.

---

# Additional Documentation

- `DECISIONS.md`
- `INCIDENT.md`

---

# Suggested Screenshots

- Successful GitHub Actions run
- Grafana dashboard
- Prometheus targets
- Running Docker containers
- Trivy scan output

---

# Loom Walkthrough

Add Loom walkthrough link here:

```text
<LOOM_VIDEO_LINK>
```

---

# Assumptions

- Local development environment only
- Docker Compose used instead of Kubernetes
- PostgreSQL persistence handled through Docker volumes
- Secrets managed through environment variables

---

# Future Improvements

- HTTPS/TLS termination
- Distributed tracing
- Centralized logging stack
- Managed cloud deployment
- Horizontal scaling
- Secret rotation integration

---

# Author

Neha Sonar