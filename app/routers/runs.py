from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/experiment_runs", tags=["runs"])


@router.get("/", response_model=list[schemas.Run], dependencies=[Security(verify_api_key)])
def list_runs(db: Session = Depends(get_db)):
    return crud.get_runs(db)


@router.get("/{run_id}", response_model=schemas.Run, dependencies=[Security(verify_api_key)])
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = crud.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    run.media_files = crud.get_run_media(db, run_id)
    return run


@router.post("/", response_model=schemas.Run, dependencies=[Security(verify_api_key)])
def create_run(run_data: schemas.RunCreate, db: Session = Depends(get_db)):
    experiment = crud.get_experiment(db, run_data.experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return crud.create_run(db, run_data.experiment_id)


@router.delete("/{run_id}", dependencies=[Security(verify_api_key)])
def delete_run(run_id: int, db: Session = Depends(get_db)):
    if not crud.delete_run(db, run_id):
        raise HTTPException(status_code=404, detail="Run not found")
    return {"ok": True}
