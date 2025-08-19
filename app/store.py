from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from . import config

def _chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk.strip())
        i += max(1, chunk_size - overlap)
    return [c for c in chunks if c]

class VectorIndex:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.data_dir / "index.faiss"
        self.meta_path = self.data_dir / "meta.json"
        self.model_name = config.EMBEDDING_MODEL
        self._model = None
        self._dim = None
        self.meta: List[Dict[str, Any]] = []
        self._id_counter = 0
        self._index = None
        self._load_or_init()

    def _embedder(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
            self._dim = self._model.get_sentence_embedding_dimension()
        return self._model

    def _new_index(self):
        dim = self._embedder().get_sentence_embedding_dimension()
        self._dim = dim
        self._index = faiss.IndexFlatIP(dim)  # cosine via normalized dot product

    def _load_or_init(self):
        if self.meta_path.exists() and self.index_path.exists():
            try:
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                self.meta = payload.get("meta", [])
                self._id_counter = payload.get("id_counter", len(self.meta))
                self.model_name = payload.get("model_name", self.model_name)
                self._index = faiss.read_index(str(self.index_path))
                if self._dim is None:
                    self._dim = self._embedder().get_sentence_embedding_dimension()
                return
            except Exception:
                pass
        self._new_index()
        self.meta = []
        self._id_counter = 0

    def save(self):
        if self._index is not None:
            faiss.write_index(self._index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "meta": self.meta,
                "id_counter": self._id_counter,
                "model_name": self.model_name
            }, f, ensure_ascii=False, indent=2)

    def add_document(self, title: str, text: str, chunk_size: int = 700, overlap: int = 120) -> int:
        chunks = _chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        if not chunks:
            return 0
        emb = self._embedder().encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        if self._index is None or self._index.d != emb.shape[1]:
            self._new_index()
        self._index.add(emb.astype(np.float32))
        for i, c in enumerate(chunks):
            self.meta.append({
                "id": self._id_counter,
                "title": title,
                "chunk_index": i,
                "text": c
            })
            self._id_counter += 1
        self.save()
        return len(chunks)

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if self._index is None or self._index.ntotal == 0:
            return []
        qv = self._embedder().encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
        scores, idxs = self._index.search(qv, min(k, self._index.ntotal))
        idxs = idxs[0].tolist()
        scores = scores[0].tolist()
        out = []
        for rank, (i, s) in enumerate(zip(idxs, scores), start=1):
            if i < 0 or i >= len(self.meta):
                continue
            m = self.meta[i]
            out.append({
                "rank": rank,
                "score": float(s),
                "title": m["title"],
                "chunk_index": m["chunk_index"],
                "text": m["text"]
            })
        return out
