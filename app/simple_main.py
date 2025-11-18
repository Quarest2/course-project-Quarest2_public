"""
Упрощенная версия приложения для тестирования
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/v1/features")
async def get_features():
    return {"features": ["feature1", "feature2"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
