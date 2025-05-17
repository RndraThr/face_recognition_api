from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.face_model import Face
from app.schemas.face_schema import FaceOut, FaceRecognitionResponse
from app.services.face_service import get_embedding_from_image
from app.core.settings import settings
from scipy.spatial.distance import cosine
import numpy as np
import cv2

router = APIRouter()


@router.get("/api/face", response_model=list[FaceOut])
def get_all_faces(db: Session = Depends(get_db)):
    return db.query(Face).all()


@router.post("/api/face/register")
async def register_face(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    embedding = get_embedding_from_image(image)
    if embedding is None:
        raise HTTPException(status_code=400, detail="Wajah nggak ketemu")

    try:
        new_face = Face(name=name, embedding=embedding.tolist())
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal simpan ke database")

    return {"message": "Wajah berhasil ditambahin", "id": new_face.id}


@router.post("/api/face/recognize", response_model=FaceRecognitionResponse)
async def recognize_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    query_embedding = get_embedding_from_image(image)
    if query_embedding is None:
        raise HTTPException(status_code=400, detail="Wajah nggak ketemu")

    faces = db.query(Face).all()
    if not faces:
        raise HTTPException(status_code=404, detail="Belum ada wajah di database")

    best_match = None
    best_score = float("inf")

    for face in faces:
        score = cosine(query_embedding, face.embedding)
        if score < best_score:
            best_score = score
            best_match = face

    matched = best_score < settings.threshold

    return FaceRecognitionResponse(
        matched=matched,
        similarity=1.0 - best_score,
        matched_face=FaceOut.model_validate(best_match) if matched else None
    )


@router.delete("/api/face/{id}")
def delete_face(id: int, db: Session = Depends(get_db)):
    face = db.query(Face).filter(Face.id == id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Wajah nggak ditemukan")

    try:
        db.delete(face)
        db.commit()
        return {"message": f"Wajah dengan ID {id} berhasil dihapus"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal hapus dari database")
