import whisper
import torch
from typing import Optional
import warnings
import subprocess
import uuid
import os

# Cache do modelo
_model_cache = None

def get_model(model_size: str = "base"):
    """Carrega o modelo Whisper (cacheado)"""
    global _model_cache
    if _model_cache is None:
        _model_cache = whisper.load_model(model_size)
    return _model_cache


def transcribe_audio(
    file_path: str,
    language: Optional[str] = None,
    task: str = "transcribe"
) -> str:
    """
    Transcreve arquivo de áudio usando Whisper
    (com conversão automática para WAV 16kHz mono)
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    model = get_model()
    wav_path = f"/tmp/{uuid.uuid4()}.wav"

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", file_path,
                "-ac", "1",
                "-ar", "16000",
                wav_path
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        options = {
            "task": task,
            "fp16": torch.cuda.is_available()
        }

        if language:
            options["language"] = language

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = model.transcribe(wav_path, **options)

        return result.get("text", "").strip()

    except subprocess.CalledProcessError:
        raise RuntimeError("Falha ao converter áudio")

    except Exception as e:
        raise RuntimeError(str(e))

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
