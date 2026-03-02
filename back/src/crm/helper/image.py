import io
import os
from PIL import Image
import uuid
from pathlib import Path

MAX_SIZE_MB = 1
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parents[1]   # это папка src
CAMERA_DIR = SRC_DIR / "files" / "camera"

def compress_image_to_1mb(file_bytes: bytes) -> bytes:

    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")  # важно для jpeg

    quality = 95
    output = io.BytesIO()

    image.save(output, format="JPEG", quality=quality, optimize=True)

    while output.tell() > MAX_SIZE_BYTES and quality > 10:
        quality -= 5
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)

    return output.getvalue()

def save_image(file_bytes: bytes) -> str:
    CAMERA_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}.jpg"
    filepath = CAMERA_DIR / filename

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    print("Saved to:", filepath)  # для проверки

    return f"camera/{filename}"

def delete_old_photos(days: int = 1):
    from pathlib import Path
    from datetime import datetime, timedelta

    CAMERA_DIR = Path("src/files/camera")
    now = datetime.utcnow()
    expire_time = timedelta(days=days)

    for file_path in CAMERA_DIR.iterdir():
        if file_path.is_file():
            modified_time = datetime.utcfromtimestamp(file_path.stat().st_mtime)
            if now - modified_time > expire_time:
                file_path.unlink()
                print(f"Удалён файл: {file_path}")