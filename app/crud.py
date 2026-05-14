from sqlalchemy.orm import Session
from app import models, schemas


def get_experiment(db: Session, experiment_id: str):
    return db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()


def get_experiments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Experiment).offset(skip).limit(limit).all()


def create_experiment(db: Session, experiment: schemas.ExperimentBase):
    db_experiment = models.Experiment(
        id=experiment.id,
        name=experiment.name,
        category=experiment.category,
        description=experiment.description
    )
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


def get_run(db: Session, run_id: int):
    return db.query(models.Run).filter(models.Run.id == run_id).first()


def get_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).order_by(models.Run.created_at.desc()).offset(skip).limit(limit).all()


def create_run(db: Session, experiment_id: str):
    db_run = models.Run(experiment_id=experiment_id)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def delete_run(db: Session, run_id: int):
    db_run = db.query(models.Run).filter(models.Run.id == run_id).first()
    if db_run:
        db.delete(db_run)
        db.commit()
        return True
    return False


def get_run_media(db: Session, run_id: int):
    return db.query(models.Media).filter(models.Media.run_id == run_id).all()


def create_media(db: Session, run_id: int, filename: str, original_name: str, mime_type: str, size_bytes: int):
    db_media = models.Media(
        run_id=run_id,
        filename=filename,
        original_name=original_name,
        mime_type=mime_type,
        size_bytes=size_bytes
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def delete_media(db: Session, media_id: int):
    db_media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if db_media:
        db.delete(db_media)
        db.commit()
        return True
    return False
