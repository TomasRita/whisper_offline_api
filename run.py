import uvicorn
import os
import sys

# Adicionar a pasta raiz ao PYTHONPATH para evitar erros de import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # caminho para a sua aplicação FastAPI
        host="0.0.0.0",
        port=8000,
        reload=True
    )
