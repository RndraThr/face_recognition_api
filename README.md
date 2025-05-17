# Face Recognition API

Sistem Face Recognition ini dibangun menggunakan **FastAPI**, **PostgreSQL**, dan **ONNX InsightFace (Glint360k R100)**. Sistem ini mampu melakukan deteksi wajah, ekstraksi fitur (embedding), pencocokan wajah, serta menyimpan/mengelola data wajah yang sudah dikenali.

---

## Teknologi yang Digunakan
- **Python 3.10**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL (via Docker)**
- **InsightFace (buffalo_l)**
- **ONNX Runtime**
- **Docker + Docker Compose**

---

## Struktur Folder
face_recognition_api/
├── app/
│ ├── api/
│ │ └── face.py # Endpoint API utama
│ ├── core/
│ │ ├── config.py # Konfigurasi environment
│ │ └── utils.py # Fungsi bantu (resize, base64, dll)
│ ├── models/
│ │ └── face_model.py # Model SQLAlchemy
│ ├── schemas/
│ │ └── face_schema.py # Schema untuk request & response
│ ├── services/
│ │ └── face_service.py # Logika deteksi & embedding wajah
│ ├── main.py # Entry point FastAPI
├── onnx_models/
│ └── glint360k_r100.onnx # Akan otomatis terunduh saat build
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml


---

## Konfigurasi Environment

Edit file `.env`:
```env
DATABASE_URL=postgresql://postgres:admin@db:5432/facerecognition
THRESHOLD=0.4


Cara Menjalankan:

1. Clone repo
    git clone https://github.com/RndraThr/face_recognition_api.git
    cd face-recognition-api

    Setelah masuk ke folder project selanjutnya jalankan docker.


2. Jalankan Docker
    docker-compose up --build
    Model glint360k_r100.onnx akan otomatis diunduh dari Google Drive dan diletakkan ke folder onnx_models/.

    Setelah Build dan Upload Docker sudah berhasil dan server sudah berjalan, selanjutnya tinggal buka browser dan masuk ke dokumentasi Swagger.

    Buka browser ke:
    http://localhost:8000/docs

    Nah setelah sudah masuk, bisa TryOut semua APInya.

    Misalkan:
    Disini saya coba untuk mengupload Gambar wajah
    
Endpoint API
[GET] /api/face
Menampilkan semua data wajah yang tersimpan.
________________________________________
[POST] /api/face/register
Mendaftarkan wajah baru.
Form-Data:
•	name: nama
•	file: file gambar
________________________________________
[POST] /api/face/recognize
Cocokkan wajah dari gambar terhadap database.
Form-Data:
•	file: file gambar
________________________________________
[DELETE] /api/face/{id}
Hapus wajah berdasarkan ID.

