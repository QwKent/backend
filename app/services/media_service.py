import os
import shutil
from app.config import UPLOAD_DIR
from fastapi import UploadFile

def save_file(file: UploadFile, file_id: str) -> str:
    extension = os.path.splitext(file.filename)[1]
    filename = f"{file_id}{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return f"/uploads/{filename}"

def get_file_path(file_id: str) -> str:
    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(file_id):
            return os.path.join(UPLOAD_DIR, filename)
    return None

def delete_file(file_id: str) -> bool:
    file_path = get_file_path(file_id)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def get_experiment_files(experiment_id: int) -> list:
    experiment_files = []
    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(f"exp{experiment_id}"):
            experiment_files.append(f"/uploads/{filename}")
    return experiment_files