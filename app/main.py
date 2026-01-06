from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Offline Whisper Transcription API",
    description="API para transcrição de áudio offline usando Whisper",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção substitua pelos domínios reais
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api/v1")

# Criar diretório de uploads na inicialização
os.makedirs("uploads", exist_ok=True)

# --- Handlers globais de exceção ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc)}
    )
