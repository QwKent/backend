from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preview_image = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExperimentImage(Base):
    __tablename__ = "experiment_images"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    image_url = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(Experiment).count() == 0:
            experiments = [
                Experiment(id=1, name="Эксперимент 1", preview_image="/uploads/exp1_preview.jpg"),
                Experiment(id=2, name="Эксперимент 2", preview_image="/uploads/exp2_preview.jpg"),
                Experiment(id=3, name="Эксперимент 3", preview_image="/uploads/exp3_preview.jpg"),
            ]
            db.add_all(experiments)
            db.flush()
            
            images = [
                ExperimentImage(experiment_id=1, image_url="/uploads/exp1_img1.jpg", sort_order=1),
                ExperimentImage(experiment_id=1, image_url="/uploads/exp1_img2.jpg", sort_order=2),
                ExperimentImage(experiment_id=1, image_url="/uploads/exp1_img3.jpg", sort_order=3),
                ExperimentImage(experiment_id=2, image_url="/uploads/exp2_img1.jpg", sort_order=1),
                ExperimentImage(experiment_id=2, image_url="/uploads/exp2_img2.jpg", sort_order=2),
                ExperimentImage(experiment_id=3, image_url="/uploads/exp3_img1.jpg", sort_order=1),
                ExperimentImage(experiment_id=3, image_url="/uploads/exp3_img2.jpg", sort_order=2),
                ExperimentImage(experiment_id=3, image_url="/uploads/exp3_img3.jpg", sort_order=3),
                ExperimentImage(experiment_id=3, image_url="/uploads/exp3_img4.jpg", sort_order=4),
            ]
            db.add_all(images)
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()