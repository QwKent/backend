import uuid
import mimetypes
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Security
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.config import config
from app.auth import verify_api_key

router = APIRouter(tags=["media"])
MEDIA_ROOT = Path(config.MEDIA_ROOT)
RUNS_MEDIA_ROOT = MEDIA_ROOT / "runs"


@router.post("/experiment_runs/{run_id}/media", dependencies=[Security(verify_api_key)])
async def upload_media(
    run_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    run = crud.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run_dir = RUNS_MEDIA_ROOT / str(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    
    ext = Path(file.filename).suffix.lower()
    file_key = f"{uuid.uuid4().hex}{ext}"
    file_path = run_dir / file_key
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    mime_type = mimetypes.guess_type(file.filename)[0] or file.content_type or "application/octet-stream"
    
    media = crud.create_media(
        db=db,
        run_id=run_id,
        filename=file_key,
        original_name=file.filename,
        mime_type=mime_type,
        size_bytes=len(content)
    )
    
    return {
        "id": media.id,
        "filename": file_key,
        "original_name": media.original_name,
        "mime_type": media.mime_type,
        "size_bytes": media.size_bytes,
        "url": f"/media/runs/{run_id}/{file_key}",
        "created_at": media.created_at
    }


@router.delete("/experiment_runs/{run_id}/media/{media_id}", dependencies=[Security(verify_api_key)])
def delete_media(run_id: int, media_id: int, db: Session = Depends(get_db)):
    run = crud.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    media = crud.get_run_media(db, run_id)
    media_to_delete = next((m for m in media if m.id == media_id), None)
    
    if not media_to_delete:
        raise HTTPException(status_code=404, detail="Media not found")
    
    file_path = RUNS_MEDIA_ROOT / str(run_id) / media_to_delete.filename
    file_path.unlink(missing_ok=True)
    
    if not crud.delete_media(db, media_id):
        raise HTTPException(status_code=404, detail="Media not found")
    
    return {"ok": True}


@router.get("/media/runs/{run_id}/{filename}")
def get_media_file(run_id: int, filename: str):
    file_path = RUNS_MEDIA_ROOT / str(run_id) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
