import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path
from insightface.app import FaceAnalysis
from app.core.utils import resize_if_large

MODEL_PATH = Path("onnx_models/glint360k_r100.onnx")
session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

# pake InsightFace buat deteksi dan align wajah
insight_app = FaceAnalysis(name="buffalo_l")
insight_app.prepare(ctx_id=0, det_size=(640, 640))

INPUT_SIZE = (112, 112)

def detect_and_align(image: np.ndarray) -> np.ndarray | None:
    # resize kalau terlalu besar
    image = resize_if_large(image)

    faces = insight_app.get(image)
    if len(faces) > 0 and faces[0].aligned is not None:
        return faces[0].aligned  # output InsightFace sudah RGB + 112x112

    # fallback ke haarcascade
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    bboxes = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(bboxes) > 0:
        x, y, w, h = bboxes[0]
        face = image[y:y+h, x:x+w]
        return cv2.resize(face, (112, 112))

    return None

def get_embedding_from_image(image: np.ndarray) -> np.ndarray | None:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    aligned = detect_and_align(image_rgb)
    if aligned is None:
        return None

    face = aligned.astype(np.float32)
    face = (face - 127.5) / 128.0
    face = np.transpose(face, (2, 0, 1))
    face = np.expand_dims(face, axis=0)

    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: face})
    embedding = outputs[0][0]

    if embedding is None or np.isnan(embedding).any():
        return None

    return embedding / np.linalg.norm(embedding)
