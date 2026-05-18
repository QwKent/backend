from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaFile(BaseModel):
    id: str
    filename: str
    url: str
    size: int
    created_at: datetime
    experiment_id: Optional[int] = None

class UploadRequest(BaseModel):
    experiment_id: Optional[int] = None