"""Security headers middleware (S06-06)"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all HTTP responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        csp_policy = (
            "default-src 'self'; script-src 'none'; style-src 'none'; "
            "img-src 'self' data:; font-src 'self'; connect-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp_policy

        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=()"
        )

        return response
