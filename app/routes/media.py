from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import List
import os
import uuid
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from app.database import get_db
from app.services import media_service
from app.middleware.auth import verify_api_key
from app.config import settings

router = APIRouter(prefix="/api", dependencies=[Depends(verify_api_key)])

class ExperimentResponse(BaseModel):
    id: str
    name: str
    preview_image_url: str

class ExperimentImagesResponse(BaseModel):
    experiment_id: str
    image_urls: List[str]

class MediaResponse(BaseModel):
    media_id: str
    filename: str
    url: str
    size: int
    created_at: datetime

def get_run_upload_dir(run_id: str) -> str:
    if not run_id or os.path.basename(run_id) != run_id or not media_service.validate_file_path(run_id):
        raise HTTPException(status_code=400, detail="Invalid run ID")

    return os.path.join(settings.UPLOAD_DIR, run_id)

def validate_media_id(media_id: str):
    if not media_id or os.path.basename(media_id) != media_id or not media_service.validate_file_path(media_id):
        raise HTTPException(status_code=400, detail="Invalid media ID")

@router.get("/experiments", response_model=List[ExperimentResponse])
async def get_experiments(db: Session = Depends(get_db)):
    return media_service.get_all_experiments(db)

@router.get("/experiments/{experiment_id}/images", response_model=ExperimentImagesResponse)
async def get_experiment_images(experiment_id: str, db: Session = Depends(get_db)):
    images = media_service.get_experiment_images(db, experiment_id)
    return {
        "experiment_id": experiment_id,
        "image_urls": images
    }

@router.post("/experiment_runs/{run_id}/media")
async def upload_media(
    run_id: str,
    fileName: str = Form(...),
    file: UploadFile = File(...)
):
    extension = os.path.splitext(file.filename)[1].lower()
    
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extension {extension} not allowed")
    
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    media_id = str(uuid.uuid4())
    filename = f"{media_id}{extension}"
    run_upload_dir = get_run_upload_dir(run_id)
    os.makedirs(run_upload_dir, exist_ok=True)
    file_path = os.path.join(run_upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return MediaResponse(
        media_id=media_id,
        filename=fileName,
        url=f"/uploads/{run_id}/{filename}",
        size=file_size,
        created_at=datetime.utcnow()
    )

@router.get("/experiment_runs/{run_id}/media")
async def get_run_media(run_id: str):
    run_files = []
    run_upload_dir = get_run_upload_dir(run_id)

    if not os.path.isdir(run_upload_dir):
        return {"run_id": run_id, "media": run_files}

    for filename in os.listdir(run_upload_dir):
        file_path = os.path.join(run_upload_dir, filename)
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            run_files.append({
                "media_id": filename.split(".")[0],
                "filename": filename,
                "url": f"/uploads/{run_id}/{filename}",
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime)
            })
    
    return {"run_id": run_id, "media": run_files}

@router.delete("/experiment_runs/{run_id}/media/{media_id}")
async def delete_media(run_id: str, media_id: str):
    run_upload_dir = get_run_upload_dir(run_id)
    validate_media_id(media_id)

    if not os.path.isdir(run_upload_dir):
        raise HTTPException(status_code=404, detail="Media not found")

    for filename in os.listdir(run_upload_dir):
        if os.path.splitext(filename)[0] == media_id:
            file_path = os.path.join(run_upload_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                return {"message": "Media deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Media not found")

@router.get("/files/{filename}")
async def download_file(filename: str):
    safe_path = media_service.get_safe_file_path(filename)
    if not safe_path or not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(safe_path, filename=filename)