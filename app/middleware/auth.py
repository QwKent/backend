from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.services.token_service import verify_device_token
import secrets

def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or not secrets.compare_digest(api_key, settings.API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API Key")

def verify_device_auth(request: Request):
    device_token = request.headers.get("Authorization")
    if not device_token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    if device_token.startswith("Bearer "):
        device_token = device_token[7:]
    
    db = SessionLocal()
    try:
        if not verify_device_token(db, device_token):
            raise HTTPException(status_code=401, detail="Invalid or expired device token")
    finally:
        db.close()

class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/static"):
            return await call_next(request)

        if request.method == "GET" and request.url.path.startswith("/media-temp"):
            return await call_next(request)

        if request.url.path == "/" or request.url.path == "/health":
            return await call_next(request)

        if request.url.path == "/register-device":
            return await call_next(request)

        if request.url.path.startswith("/swagger") or request.url.path.startswith("/redoc"):
            return await call_next(request)

        if request.url.path.startswith("/openapi.json"):
            return await call_next(request)

        try:
            verify_device_auth(request)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

        return await call_next(request)