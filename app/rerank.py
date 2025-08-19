from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
from . import config

_ce = None

def _model() -> CrossEncoder:
    global _ce
    if _ce is None:
        _ce = CrossEncoder(config.RERANK_MODEL)
    return _ce

def rerank(query: str, passages: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    if not passages:
        return []
    pairs = [(query, p["text"]) for p in passages]
    scores = _model().predict(pairs).tolist()
    for p, s in zip(passages, scores):
        p["rerank_score"] = float(s)
    passages.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
    for i, p in enumerate(passages[:top_k], start=1):
        p["rank"] = i
    return passages[:top_k]
