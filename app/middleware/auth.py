from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
import secrets

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "GET" and request.url.path.startswith("/uploads"):
            return await call_next(request)
        
        if request.url.path == "/" or request.url.path == "/health":
            return await call_next(request)
        
        if request.url.path.startswith("/swagger") or request.url.path.startswith("/redoc"):
            return await call_next(request)
        
        if request.url.path.startswith("/openapi.json"):
            return await call_next(request)
        
        api_key = request.headers.get("X-API-Key")
        
        if not api_key or not secrets.compare_digest(api_key, settings.API_KEY):
            raise HTTPException(status_code=403, detail="Invalid API Key")
        
        return await call_next(request)