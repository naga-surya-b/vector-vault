import json, sys
from pathlib import Path
from app.store import VectorIndex
from app.config import DATA_DIR

def contains_any(text, keywords):
    t = text.lower()
    return any(k.lower() in t for k in keywords)

def main():
    data_path = Path("evals/samples.jsonl")
    if not data_path.exists():
        print("Missing evals/samples.jsonl")
        sys.exit(1)
    index = VectorIndex(DATA_DIR)
    with open(data_path, "r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    total = len(rows); hits = 0
    for row in rows:
        q = row["q"]; terms = row["answer_contains"]
        docs = index.search(q, k=5)
        found = any(contains_any(d["text"], terms) for d in docs)
        hits += 1 if found else 0
        print(f"Q: {q}\nHit: {found}\n")
    print(f"Hit@5: {hits}/{total} = {hits/total if total else 0:.2f}")

if __name__ == "__main__":
    main()
