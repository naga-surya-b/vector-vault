from app import config
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def main():
    print("Downloading embedding model:", config.EMBEDDING_MODEL)
    _ = SentenceTransformer(config.EMBEDDING_MODEL)
    if config.ENABLE_RERANK:
        print("Downloading rerank model:", config.RERANK_MODEL)
        _ = CrossEncoder(config.RERANK_MODEL)
    if config.ENABLE_LLM:
        print("Downloading LLM:", config.LLM_MODEL)
        _ = AutoTokenizer.from_pretrained(config.LLM_MODEL)
        _ = AutoModelForSeq2SeqLM.from_pretrained(config.LLM_MODEL)
    print("Done.")

if __name__ == "__main__":
    main()
