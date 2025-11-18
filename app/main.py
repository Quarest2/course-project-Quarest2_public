"""
Основной файл приложения для тестирования NFR
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.routers import features
from app.services.monitoring import logger, track_performance

app = FastAPI(
    title="Feature Votes API",
    description="API для голосования за фичи",
    version="1.0.0",
)

# Подключаем роутеры
app.include_router(features.router, prefix="/api/v1", tags=["features"])

# Middleware для безопасности (NFR-004)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    with track_performance("root"):
        logger.info("Root endpoint called")
        return {"message": "Feature Votes API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check эндпоинт для мониторинга (NFR-003)"""
    import datetime

    with track_performance("health_check"):
        logger.info("Health check requested")
        return {
            "status": "ok",
            "service": "feature-votes",
            "timestamp": datetime.datetime.now().isoformat(),
        }


# Middleware для добавления security headers (NFR-004)
@app.middleware("http")
async def add_security_headers(request, call_next):
    with track_performance("security_middleware"):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response


# Exception handlers для логирования ошибок (NFR-006)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        "HTTP Exception",
        path=str(request.url),
        method=request.method,
        status_code=exc.status_code,
        detail=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled Exception",
        path=str(request.url),
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
