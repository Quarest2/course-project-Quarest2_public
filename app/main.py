from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.features import router as features_router
from app.core.exceptions import (
    ApiError,
    api_error_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.middleware.correlation import CorrelationMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.xss_sanitizer import XSSSanitizerMiddleware

app = FastAPI(
    title="Feature Votes API",
    description="API для голосования за фичи",
)

app.add_middleware(CorrelationMiddleware)
app.add_middleware(XSSSanitizerMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(ApiError, api_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(features_router)

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}