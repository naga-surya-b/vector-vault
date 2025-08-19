# VectorVault Pro — Private, Offline Document Q&A (FAISS) with Reranker + On‑Device LLM

## Quickstart (one-app run)
```bash
cd frontend
npm install
npm run build
cd ..
# Windows
run.bat
# macOS/Linux
./run.sh
# open http://127.0.0.1:8000
```

## Options (env vars)
- `ENABLE_RERANK=1` → rerank top-k with cross-encoder (`VV_RERANK_MODEL` to change)
- `ENABLE_LLM=1` → synthesize short answer from retrieved passages (`VV_LLM_MODEL` to change)
- `VV_TOP_K=8` → change number of results
- `VV_DATA_DIR=...` → custom data directory
Prefetch models for offline use: `python prefetch_models.py`

## API
- `POST /api/ingest` (file upload) — pdf/txt/md
- `POST /api/ingest-text` — { title, text }
- `GET  /api/search?q=...&k=5`
- `GET  /api/answer?q=...&k=5` (requires `ENABLE_LLM=1`)

## Docker
```bash
# build UI first (see Quickstart), then:
docker build -t vectorvault-pro:latest .
docker run -p 8000:8000 -v $(pwd)/data:/app/data vectorvault-pro:latest
```

## Windows EXE (PyInstaller)
- Local: run `build_exe.ps1` in PowerShell (after building frontend)
- CI: pushing a tag like `v0.3.0` triggers GitHub Actions to build an EXE artifact

## Evals
```bash
python evals/eval_rag.py
```

## Push to GitHub
```bash
git init
git add .
git commit -m "Initial: VectorVault Pro"
git branch -M main
git remote add origin https://github.com/<YOU>/<REPO>.git
git push -u origin main
```
