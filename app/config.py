import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./runs.db")
    API_KEY = os.getenv("API_KEY", "")

config = Config()
