from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from app.config import config

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key


async def optional_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key and api_key == config.API_KEY:
        return True
    return False
