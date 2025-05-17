from app.database import engine
from app.models.face_model import Base

print("Buat tabel di database...")
Base.metadata.create_all(bind=engine)
print("Tabel berhasil dibuat.")
