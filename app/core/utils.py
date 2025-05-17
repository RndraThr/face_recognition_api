import base64
import cv2
import numpy as np

def image_to_base64(image: np.ndarray) -> str:
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")

def base64_to_image(base64_str: str) -> np.ndarray:
    image_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def resize_if_large(image: np.ndarray, max_size=1024) -> np.ndarray:
    if max(image.shape[:2]) > max_size:
        h, w = image.shape[:2]
        scale = max_size / max(h, w)
        return cv2.resize(image, (int(w * scale), int(h * scale)))
    return image