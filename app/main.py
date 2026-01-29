from fastapi import FastAPI

from app.api.predict import router as predict_router
from app.storage.db import engine
from app.storage.schemas import Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Silent Failure Detection System")

app.include_router(predict_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "silent-failure-detection-system"}