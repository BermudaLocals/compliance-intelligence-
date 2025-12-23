from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

# health check
@app.get("/health")
def health():
    return {"status": "ok"}

# include v1 router
app.include_router(router, prefix=settings.api_prefix)
