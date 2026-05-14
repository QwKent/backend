import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import experiments_router, runs_router, media_router
from app.config import config

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhysicsExps Media API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_ROOT = Path(config.MEDIA_ROOT)
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
(MEDIA_ROOT / "experiments").mkdir(parents=True, exist_ok=True)
(MEDIA_ROOT / "runs").mkdir(parents=True, exist_ok=True)

app.mount("/media", StaticFiles(directory=str(MEDIA_ROOT)), name="media")

app.include_router(experiments_router)
app.include_router(runs_router)
app.include_router(media_router)


@app.get("/")
def root():
    return {"message": "PhysicsExps Media API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)