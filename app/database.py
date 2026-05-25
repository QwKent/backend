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

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    device_name = Column(String, nullable=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Integer, default=1)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(Experiment).count() == 0:
            experiments = [
                Experiment(id="coulombs_law", name="Coulomb's law", preview_image="/static/experiments/previews/coulombs_law.webp"),
                Experiment(id="doppler_effect", name="Doppler effect", preview_image="/static/experiments/previews/doppler_effect.webp"),
                Experiment(id="free_fall", name="Free fall", preview_image="/static/experiments/previews/free_fall.webp"),
                Experiment(id="harmonic_vibrations", name="Harmonic vibrations", preview_image="/static/experiments/previews/harmonic_vibrations.webp"),
                Experiment(id="joule_lenz", name="Joule-Lenz law", preview_image="/static/experiments/previews/joule_lenz.webp"),
                Experiment(id="pendulum", name="Pendulum", preview_image="/static/experiments/previews/pendulum.webp"),
                Experiment(id="physical_pendulum", name="Physical pendulum", preview_image="/static/experiments/previews/physical_pendulum.webp"),
                Experiment(id="projectile_motion", name="Projectile motion", preview_image="/static/experiments/previews/projectile_motion.webp"),
                Experiment(id="radioactive_decay", name="Radioactive decay", preview_image="/static/experiments/previews/radioactive_decay.webp"),
                Experiment(id="spring_pendulum", name="Spring pendulum", preview_image="/static/experiments/previews/spring_pendulum.webp"),
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