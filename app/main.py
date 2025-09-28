from fastapi import FastAPI

from app.routers import features

app = FastAPI(
    title="Feature Votes API",
    version="1.0.0",
    description="API для голосования за фичи проекта",
)

app.include_router(features.router, prefix="/api/v1", tags=["features"])


@app.get("/")
def read_root():
    return {"message": "Feature Votes API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
