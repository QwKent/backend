from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("/", response_model=list[schemas.Experiment], dependencies=[Security(verify_api_key)])
def list_experiments(db: Session = Depends(get_db)):
    return crud.get_experiments(db)


@router.get("/{experiment_id}", response_model=schemas.Experiment, dependencies=[Security(verify_api_key)])
def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    experiment = crud.get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment
