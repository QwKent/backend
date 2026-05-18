from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api")

class ExperimentResponse(BaseModel):
    id: int
    name: str
    preview_image_url: str

class ExperimentImagesResponse(BaseModel):
    experiment_id: int
    image_urls: List[str]

EXPERIMENTS = [
    {"id": 1, "name": "Эксперимент 1", "preview_image_url": "/uploads/exp1_preview.jpg"},
    {"id": 2, "name": "Эксперимент 2", "preview_image_url": "/uploads/exp2_preview.jpg"},
    {"id": 3, "name": "Эксперимент 3", "preview_image_url": "/uploads/exp3_preview.jpg"}
]

EXPERIMENT_IMAGES = {
    1: ["/uploads/exp1_img1.jpg", "/uploads/exp1_img2.jpg", "/uploads/exp1_img3.jpg"],
    2: ["/uploads/exp2_img1.jpg", "/uploads/exp2_img2.jpg"],
    3: ["/uploads/exp3_img1.jpg", "/uploads/exp3_img2.jpg", "/uploads/exp3_img3.jpg", "/uploads/exp3_img4.jpg"]
}

@router.get("/experiments", response_model=List[ExperimentResponse])
async def get_experiments():
    return EXPERIMENTS

@router.get("/experiments/{experiment_id}/images", response_model=ExperimentImagesResponse)
async def get_experiment_images(experiment_id: int):
    return {
        "experiment_id": experiment_id,
        "image_urls": EXPERIMENT_IMAGES.get(experiment_id, [])
    }
from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MEDIA_STORAGE: Dict[str, Dict[str, Dict]] = {}

class MediaResponse(BaseModel):
    media_id: str
    filename: str
    url: str

@router.post("/api/experiment_runs/{run_id}/media")
async def upload_media(run_id: str, fileName: str, file: UploadFile = File(...)):
    media_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    save_path = os.path.join(UPLOAD_DIR, f"{media_id}{extension}")
    
    with open(save_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    if run_id not in MEDIA_STORAGE:
        MEDIA_STORAGE[run_id] = {}
    
    MEDIA_STORAGE[run_id][media_id] = {
        "filename": fileName,
        "path": save_path,
        "url": f"/uploads/{media_id}{extension}"
    }
    
    return {"media_id": media_id, "filename": fileName, "url": f"/uploads/{media_id}{extension}"}

@router.delete("/api/experiment_runs/{run_id}/media/{media_id}")
async def delete_media(run_id: str, media_id: str):
    if run_id not in MEDIA_STORAGE or media_id not in MEDIA_STORAGE[run_id]:
        raise HTTPException(status_code=404, detail="Media not found")
    
    file_path = MEDIA_STORAGE[run_id][media_id]["path"]
    if os.path.exists(file_path):
        os.remove(file_path)
    
    del MEDIA_STORAGE[run_id][media_id]
    
    return {"message": "Media deleted successfully"}

@router.get("/api/experiment_runs/{run_id}/media")
async def get_run_media(run_id: str):
    if run_id not in MEDIA_STORAGE:
        return {"run_id": run_id, "media": []}
    
    media_list = [
        {"media_id": mid, "filename": data["filename"], "url": data["url"]}
        for mid, data in MEDIA_STORAGE[run_id].items()
    ]
    
    return {"run_id": run_id, "media": media_list}
