import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.config import settings
from backend.app.limiter.limiter import limiter
from app.core.middleware import log_middleware

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

logger = logging.getLogger()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")


@app.get("/status")
async def health_status():
    return {"status": "OK"}


# app.include_router(teams.router)

@app.get("/home")
@limiter.limit("2/minute")
async def homepage(request: Request):
    return "test"
