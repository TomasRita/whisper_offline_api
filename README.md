
---

# 📝 Offline Whisper Transcription API

## Descrição

API de transcrição de áudio **offline** usando Whisper.
Permite enviar arquivos de áudio para transcrição ou tradução, suportando múltiplos formatos.

---

## Instalação

1. Clone o projeto ou baixe os arquivos.
2. Crie e ative um ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Rodar a API

### Via uvicorn direto:

```bash
# Com host acessível na rede local
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Apenas localhost
uvicorn app.main:app --reload
```

### Via script `run.py`:

```bash
python run.py
```

> O servidor estará disponível em `http://localhost:8000` ou pelo IP da máquina na rede.

---

## Endpoints

### POST `/transcribe`

Transcreve ou traduz um arquivo de áudio para texto.

**Parâmetros:**

| Parâmetro | Tipo | Obrigatório | Descrição                                                                                  |
| --------- | ---- | ----------- | ------------------------------------------------------------------------------------------ |
| audio     | file | sim         | Arquivo de áudio (mp3, wav, m4a, ogg, flac, mp4, mpeg)                                     |
| language  | str  | sim         | Idioma do áudio ('pt', 'en', 'es').             |
| task      | str  | não         | Tipo de tarefa: 'transcribe' (transcrição) ou 'translate' (tradução). Padrão: 'transcribe' |

**Exemplo de requisição com `curl`:**

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@/caminho/do/arquivo/audio.mp3" \
  -F "language=pt" \
  -F "task=transcribe"
```

**Exemplo de resposta:**

```json
{
  "success": true,
  "text": "Aqui vai o texto transcrito do áudio...",
  "language": "pt",
  "task": "transcribe",
  "filename": "audio.mp3"
}
```

---

### GET `/health`

Verificação de saúde da API.

**Exemplo de requisição:**

```bash
curl http://localhost:8000/health
```

**Exemplo de resposta:**

```json
{
  "status": "healthy",
  "service": "whisper-transcription-api"
}
```

---

## Observações

* Os arquivos de áudio enviados são armazenados temporariamente em `uploads/` e removidos automaticamente após o processamento.
* Extensões suportadas: `.mp3, .wav, .m4a, .ogg, .flac, .mp4, .mpeg`.
* Caso o arquivo tenha formato inválido, a API retorna erro `400`.



