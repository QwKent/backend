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
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preview_image = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExperimentImage(Base):
    __tablename__ = "experiment_images"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String, ForeignKey("experiments.id"), nullable=False)
    image_url = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(Experiment).count() == 0:
            experiments = [
                Experiment(id="coulombs_law", name="Coulomb's law", preview_image="/uploads/coulombs_law_preview.png"),
                Experiment(id="doppler_effect", name="Doppler effect", preview_image="/uploads/doppler_effect_preview.png"),
                Experiment(id="free_fall", name="Free fall", preview_image="/uploads/free_fall_preview.png"),
                Experiment(id="harmonic_vibrations", name="Harmonic vibrations", preview_image="/uploads/harmonic_vibrations_preview.png"),
                Experiment(id="joule_lenz", name="Joule-Lenz law", preview_image="/uploads/joule_lenz_preview.png"),
                Experiment(id="pendulum", name="Pendulum", preview_image="/uploads/pendulum_preview.png"),
                Experiment(id="physical_pendulum", name="Physical pendulum", preview_image="/uploads/physical_pendulum_preview.png"),
                Experiment(id="projectile_motion", name="Projectile motion", preview_image="/uploads/projectile_motion_preview.png"),
                Experiment(id="radioactive_decay", name="Radioactive decay", preview_image="/uploads/radioactive_decay_preview.png"),
                Experiment(id="spring_pendulum", name="Spring pendulum", preview_image="/uploads/spring_pendulum_preview.png"),
            ]
            db.add_all(experiments)
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()