import asyncio
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
import os
import time
from sqlalchemy.exc import OperationalError
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas

API_KEY = os.getenv("API_KEY", "mysecretkey")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

shutdown_timeout = int(os.getenv("SHUTDOWN_TIMEOUT_SECONDS", "10"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print(f"Shutdown started. Waiting up to {shutdown_timeout}s for in-flight requests.")
    await asyncio.sleep(min(shutdown_timeout, 10))
    print("Shutdown complete.")

app = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Key validation
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Unauthorized")

@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Apply rate limit here
@app.post("/data", response_model=schemas.DataResponse)
@limiter.limit("5/minute")
def create_data(
    request: Request,   # ⚠️ REQUIRED for slowapi
    data: schemas.DataCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_data = models.Data(user_id=data.user_id, payload=data.payload)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# ✅ Apply rate limit here
@app.get("/data/{id}", response_model=schemas.DataResponse)
@limiter.limit("10/minute")
def get_data(
    request: Request,   # ⚠️ REQUIRED for slowapi
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_data = db.query(models.Data).filter(models.Data.id == id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_data

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})