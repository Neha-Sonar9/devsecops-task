# Decisions

## Containerization

The application is containerized with Docker and runs as a non-root user. Docker Compose is used because the task explicitly allows Compose and does not require Kubernetes.

The local stack includes:

- FastAPI application
- PostgreSQL relational database
- Redis cache/service store
- Nginx reverse proxy
- Prometheus
- Grafana

## Secrets Management

Local development uses `.env` and `.env.example`. Real secrets are not committed.

In production, I would use AWS Secrets Manager because it integrates well with ECS/Fargate, IAM roles, audit logging, encryption with KMS, and secret rotation. Application containers would receive secrets at runtime through task roles rather than storing secrets in images or source control.

## Authentication

The data endpoints require an API key through the `X-API-Key` header. The `/health` endpoint remains public for load balancer and uptime checks.

## Rate Limiting

Rate limiting is applied per IP using SlowAPI. This is acceptable for the local task because requests come directly through Nginx. In production, I would prefer rate limiting per API key at the gateway or reverse proxy layer to avoid shared-IP false positives.

## Input Validation

Request payloads are validated using Pydantic. `user_id` and `payload` have size limits to reduce abuse risk and protect database/storage resources.

## Database Migrations

Alembic is used for database schema migrations. The container runs `alembic upgrade head` before starting the FastAPI process.

For a multi-replica production deployment, migrations should not be run independently by every application replica because this can cause race conditions. The application rollout should proceed only after migrations complete successfully.

## Observability

Prometheus scrapes the `/metrics` endpoint, and Grafana displays request rate, latency, and error-related metrics. Application events are logged in structured JSON format so they can be consumed by systems like CloudWatch Logs, Loki, ELK, or Splunk.

## CI/CD

GitHub Actions runs linting, unit tests, Bandit SAST, Docker build, Trivy scanning, GHCR image publishing, and SBOM generation. High and critical vulnerability findings from Trivy fail the pipeline.

## Infrastructure as Code

Terraform is included as a lightweight AWS infrastructure representation. It includes a VPC, security group, and commented remote-state configuration. I did not apply it to avoid unnecessary cloud cost.