import secrets
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Device

def generate_device_token() -> str:
    return secrets.token_urlsafe(32)

def generate_media_token(file_path: str, expires_at: int) -> str:
    message = f"{file_path}:{expires_at}"
    signature = hmac.new(
        settings.MEDIA_TOKEN_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_media_token(file_path: str, expires_at: int, token: str) -> bool:
    expected_token = generate_media_token(file_path, expires_at)
    current_time = int(time.time())
    if current_time > expires_at:
        return False
    return hmac.compare_digest(token, expected_token)

def register_device(db: Session, device_id: str, device_name: Optional[str] = None) -> str:
    existing_device = db.query(Device).filter(Device.device_id == device_id).first()
    if existing_device:
        if existing_device.is_active and existing_device.expires_at > datetime.utcnow():
            return existing_device.token
        db.delete(existing_device)
        db.commit()
    
    token = generate_device_token()
    expires_at = datetime.utcnow() + timedelta(days=settings.DEVICE_TOKEN_EXPIRE_DAYS)
    
    device = Device(
        device_id=device_id,
        device_name=device_name,
        token=token,
        expires_at=expires_at,
        is_active=1
    )
    db.add(device)
    db.commit()
    return token

def verify_device_token(db: Session, token: str) -> bool:
    device = db.query(Device).filter(
        Device.token == token,
        Device.is_active == 1,
        Device.expires_at > datetime.utcnow()
    ).first()
    return device is not None