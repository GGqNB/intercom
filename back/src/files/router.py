from src.auth import get_api_key
from fastapi.security.api_key import APIKey
from fastapi.responses import FileResponse
from pathlib import Path    
from fastapi import APIRouter, FastAPI, UploadFile, File, HTTPException, Depends
import os
import json 

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
APK_DIR = STATIC_DIR / "apk"
VIDEO_DIR = STATIC_DIR/ "video"

APK_DIR.mkdir(parents=True, exist_ok=True)

router_files = APIRouter(
    prefix="/files",
    tags=["Работа с файлами"]
)

@router_files.post("/upload_video")
async def upload_video(
    file: UploadFile = File(...),
    version: str = "",
    api_key: APIKey = Depends(get_api_key)
):
    filename = f"video_v{version}.mp4"
    save_path = VIDEO_DIR / filename

    with open(save_path, "wb") as f:
        f.write(await file.read())

    update_info = {
        "version": version,
        "file_name": filename
    }

    with open("video_updates.json", "w") as f:
        json.dump(update_info, f)

    return {"message": "Video uploaded", "version": version}


@router_files.get("/video/{filename}")
async def download_video(filename: str,  api_key: APIKey = Depends(get_api_key)):
    file_path = VIDEO_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )


@router_files.get("/latest_video")
async def latest_video( api_key: APIKey = Depends(get_api_key)):
    if not os.path.exists("video_updates.json"):
        return {"version": "0.0.0", "file_name": ""}

    with open("video_updates.json") as f:
        return json.load(f)

@router_files.post("/upload_apk")
async def upload_apk(
    file: UploadFile = File(...),
    version: str = "",
    api_key: APIKey = Depends(get_api_key)
):
    os.makedirs("static/apk", exist_ok=True)

    filename = f"DoorManView_v{version}.apk"
    save_path = APK_DIR / f"DoorManView_v{version}.apk"

    with open(save_path, "wb") as f:
        f.write(await file.read())

    update_info = {
        "version": version,
        "file_name": f"{filename}"
    }

    with open("updates.json", "w") as f:
        json.dump(update_info, f)

    return {"message": "APK uploaded", "version": version}

@router_files.get("/apk/{filename}")
async def download_apk(
    filename: str,
    api_key: APIKey = Depends(get_api_key)
):
    file_path = APK_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="APK not found")

    return FileResponse(
        path=file_path,
        media_type="application/vnd.android.package-archive",
        filename=filename
    )
@router_files.get("/latest_version")
async def latest_version(api_key: APIKey = Depends(get_api_key)):
    if not os.path.exists("updates.json"):
        return {"version": "0.0.0", "file_name": ""}
    with open("updates.json") as f:
        return {
            'data' : json.load(f),
            'status' : 'success'
        }