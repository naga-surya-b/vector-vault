from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from typing import Optional
import uvicorn

from .store import VectorIndex
from .ingest import extract_text_from_file
from . import config
from . import rerank as rr
from . import llm as llm_mod

APP_ROOT = Path(__file__).parent.parent
FRONTEND_DIST = APP_ROOT / "frontend" / "dist"
DATA_DIR = config.DATA_DIR

app = FastAPI(title="VectorVault Pro", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX = VectorIndex(DATA_DIR)

@app.get("/api/health")
def health():
    return {"status": "ok", "enable_rerank": config.ENABLE_RERANK, "enable_llm": config.ENABLE_LLM}

@app.post("/api/ingest")
async def ingest_file(file: UploadFile = File(...), title: Optional[str] = Form(None)):
    content = await file.read()
    text = extract_text_from_file(file.filename, content)
    doc_title = title or file.filename
    n_chunks = INDEX.add_document(doc_title, text)
    INDEX.save()
    return {"ok": True, "title": doc_title, "chunks": n_chunks}

@app.post("/api/ingest-text")
async def ingest_text(payload: dict):
    title = payload.get("title") or "pasted-text"
    text = payload.get("text") or ""
    if not text.strip():
        return JSONResponse({"ok": False, "error": "text required"}, status_code=400)
    n_chunks = INDEX.add_document(title, text)
    INDEX.save()
    return {"ok": True, "title": title, "chunks": n_chunks}

@app.get("/api/search")
def search(q: str, k: int = None):
    k = k or config.TOP_K
    results = INDEX.search(q, k=k)
    if config.ENABLE_RERANK:
        results = rr.rerank(q, results, top_k=k)
    return {"query": q, "k": k, "results": results}

@app.get("/api/answer")
def answer(q: str, k: int = None):
    k = k or config.TOP_K
    results = INDEX.search(q, k=k)
    if config.ENABLE_RERANK:
        results = rr.rerank(q, results, top_k=k)
    ans = None
    if config.ENABLE_LLM:
        try:
            ans = llm_mod.answer_from_passages(q, results)
        except Exception as e:
            ans = f"LLM error: {e}"
    return {"query": q, "k": k, "results": results, "answer": ans}

# Serve built React UI if present
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
    @app.get("/")
    def index():
        return FileResponse(FRONTEND_DIST / "index.html")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
