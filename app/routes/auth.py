from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.token_service import register_device

router = APIRouter()

class RegisterDeviceRequest(BaseModel):
    device_id: str
    device_name: Optional[str] = None

class RegisterDeviceResponse(BaseModel):
    token: str
    token_type: str
    expires_days: int

@router.post("/register-device", response_model=RegisterDeviceResponse)
async def register_device_endpoint(
    request: RegisterDeviceRequest,
    db: Session = Depends(get_db)
):
    if not request.device_id or len(request.device_id.strip()) < 3:
        raise HTTPException(status_code=400, detail="Invalid device_id")
    
    token = register_device(db, request.device_id, request.device_name)
    
    from app.config import settings
    return RegisterDeviceResponse(
        token=token,
        token_type="Bearer",
        expires_days=settings.DEVICE_TOKEN_EXPIRE_DAYS
    )