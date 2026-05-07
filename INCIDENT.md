# Incident Report

## Incident Summary

During development, database migrations initially failed because Alembic attempted to connect to PostgreSQL using `localhost` while the application database was running inside Docker Compose.

The following error occurred:

```text
sqlalchemy.exc.OperationalError:
connection to server at "localhost", port 5432 failed: Connection refused
```

## Root Cause

The issue happened because:

- PostgreSQL was running in a Docker container
- Alembic was executed from the host machine
- The database container hostname differed depending on execution context

Inside Docker Compose, services communicate using container service names such as `db`.

From the host machine, access must use `localhost:5432`.

This mismatch caused Alembic connection failures.

## Resolution

The issue was resolved by:

1. Ensuring PostgreSQL container port mapping existed:

```yaml
ports:
  - "5432:5432"
```

2. Running Docker Compose before migrations:

```bash
docker compose up -d
```

3. Passing the correct runtime database URL:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/appdb alembic upgrade head
```

4. Updating Alembic `env.py` to dynamically load `DATABASE_URL` from environment variables.

## Prevention

To reduce future migration issues:

- Database configuration is centralized through environment variables
- Alembic reads runtime database configuration dynamically
- CI validates application startup and migrations
- Docker Compose standardizes service networking

## Lessons Learned

This incident reinforced the importance of understanding networking differences between:

- host execution
- container-to-container communication
- CI runtime environments

It also highlighted why environment-driven configuration is critical for portable infrastructure and deployments.