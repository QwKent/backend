import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webm", ".mp4"}
    MAX_FILE_SIZE: int = 100 * 1024 * 1024
    DATABASE_URL: str = "sqlite:///./media.db"
    API_KEY: str = "supersecretapikey123"

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)