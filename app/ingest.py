from pathlib import Path
from pypdf import PdfReader

def extract_text_from_file(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        from io import BytesIO
        pdf = PdfReader(BytesIO(content))
        out = []
        for page in pdf.pages:
            try:
                out.append(page.extract_text() or "")
            except Exception:
                pass
        return "\n".join(out)
    elif suffix in {".txt", ".md"}:
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")
    else:
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")
