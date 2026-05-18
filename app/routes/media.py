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