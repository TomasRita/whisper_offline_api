from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.transcriber import transcribe_audio
import shutil
import os
import uuid
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".mp4", ".mpeg"}

def cleanup_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    language: str | None = None,
    task: str = "transcribe"
):
    file_ext = Path(audio.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado: {file_ext}"
        )

    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        if language in (None, "", "auto"):
            text = transcribe_audio(str(file_path), None, task)
            language_response = "auto"
        else:
            text = transcribe_audio(str(file_path), language, task)
            language_response = language

        background_tasks.add_task(cleanup_file, str(file_path))

        return {
            "success": True,
            "text": text,
            "language": language_response,
            "task": task,
            "filename": audio.filename
        }

    except Exception as e:
        cleanup_file(str(file_path))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
