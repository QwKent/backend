from fastapi import FastAPI
from app.routes.media import router

app = FastAPI(title="Media API", docs_url="/swagger")
app.include_router(router)