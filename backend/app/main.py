from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import router as v1_router

app = FastAPI(
    title="Compliance Intelligence API",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(v1_router, prefix=settings.api_prefix)
