import os
from pathlib import Path

DATA_DIR = Path(os.getenv("VV_DATA_DIR", "data"))
EMBEDDING_MODEL = os.getenv("VV_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

ENABLE_RERANK = os.getenv("ENABLE_RERANK", "0") == "1"
RERANK_MODEL = os.getenv("VV_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

ENABLE_LLM = os.getenv("ENABLE_LLM", "0") == "1"
LLM_MODEL = os.getenv("VV_LLM_MODEL", "google/flan-t5-small")

TOP_K = int(os.getenv("VV_TOP_K", "5"))
