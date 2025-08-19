from typing import List, Dict, Any
from . import config
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_tok = None
_m = None

def _load():
    global _tok, _m
    if _tok is None or _m is None:
        _tok = AutoTokenizer.from_pretrained(config.LLM_MODEL)
        _m = AutoModelForSeq2SeqLM.from_pretrained(config.LLM_MODEL)
    return _tok, _m

def answer_from_passages(question: str, passages: List[Dict[str, Any]], max_tokens: int = 256) -> str:
    if not passages:
        return "No supporting passages found."
    ctx = "\n\n".join([f"- {p['text']}" for p in passages[:5]])
    prompt = f"""You are a helpful assistant. Using ONLY the context below, answer the question concisely.
If the answer is not in the context, say 'I don't know'. Include no extra text.

Context:
{ctx}

Question: {question}
Answer:"""
    tok, model = _load()
    inp = tok(prompt, return_tensors="pt", truncation=True, max_length=1024)
    out = model.generate(**inp, max_new_tokens=max_tokens, do_sample=False)
    return tok.decode(out[0], skip_special_tokens=True).strip()
