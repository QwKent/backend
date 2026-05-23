from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import Experiment, ExperimentImage
import os
from app.config import settings

def get_all_experiments(db: Session) -> List[Dict[str, Any]]:
    experiments = db.query(Experiment).all()
    return [
        {"id": exp.id, "name": exp.name, "preview_image_url": exp.preview_image}
        for exp in experiments
    ]

def get_experiment_by_id(db: Session, experiment_id: str) -> Dict[str, Any]:
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        return None
    return {"id": experiment.id, "name": experiment.name, "preview_image_url": experiment.preview_image}

def get_experiment_images(db: Session, experiment_id: str) -> List[str]:
    images = db.query(ExperimentImage).filter(
        ExperimentImage.experiment_id == experiment_id
    ).order_by(ExperimentImage.sort_order).all()
    return [img.image_url for img in images]

def validate_file_path(filename: str) -> bool:
    safe_path = os.path.normpath(filename)
    if safe_path.startswith("..") or os.path.isabs(safe_path):
        return False
    return True

def get_safe_file_path(filename: str) -> str:
    if not validate_file_path(filename):
        return None
    return os.path.join(settings.UPLOAD_DIR, os.path.basename(filename))