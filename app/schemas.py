from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ExperimentBase(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None


class Experiment(ExperimentBase):
    created_at: datetime

    class Config:
        from_attributes = True


class MediaBase(BaseModel):
    id: int
    filename: str
    original_name: str
    mime_type: str
    size_bytes: int
    url: str


class Media(MediaBase):
    created_at: datetime

    class Config:
        from_attributes = True


class RunBase(BaseModel):
    id: int
    experiment_id: str
    created_at: datetime


class Run(RunBase):
    media_files: List[Media] = []

    class Config:
        from_attributes = True


class RunCreate(BaseModel):
    experiment_id: str


class RunResponse(BaseModel):
    run_id: int
    experiment_id: str
    created_at: datetime
    media: List[Media] = []
