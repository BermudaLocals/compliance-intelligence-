from fastapi import FastAPI

app = FastAPI(
    title="Compliance Intelligence API",
    version="0.0.1",
)

@app.get("/health")
def health():
    return {"status": "ok"}
