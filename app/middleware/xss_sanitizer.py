"""XSS sanitization middleware (S06-03)

Note: FastAPI serializes Pydantic models automatically, so we need to intercept
at the response level. This middleware works with JSONResponse by reading
the rendered body and sanitizing it.
"""

import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.xss_protection import sanitize_response_data

class XSSSanitizerMiddleware(BaseHTTPMiddleware):
    """Sanitize JSON responses to prevent XSS attacks"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if isinstance(response, JSONResponse):
            try:
                await response.render()

                if hasattr(response, "body") and response.body:
                    body_str = response.body.decode("utf-8")
                    data = json.loads(body_str)

                    sanitized_data = sanitize_response_data(data)

                    return JSONResponse(
                        content=sanitized_data,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type,
                    )
            except (
                json.JSONDecodeError,
                UnicodeDecodeError,
                AttributeError,
                TypeError,
            ):
                pass

        return response
