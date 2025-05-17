from fastapi import FastAPI
from app.api.face import router as face_router

app = FastAPI(
    title="Face Recognition API",
    version="1.0"
)

app.include_router(face_router)
