"""Correlation ID middleware for request tracing (ADR-001)"""

import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation ID to requests"""

    async def dispatch(self, request: Request, call_next):
        request.state.correlation_id = str(uuid.uuid4())

        response = await call_next(request)

        response.headers["X-Correlation-ID"] = request.state.correlation_id

        return response
