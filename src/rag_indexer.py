## Indexers (parse → chunk → embed → FAISS)
## Walk a folder (PDF/TXT/JSON), extract text, chunk, embed, and build FAISS.
from pathlib import Path
import json
from typing import Iterable, List, Dict
from src.config import settings
from src.pdf_parser import extract_pdf_to_db
from src.chunking import chunk_text
from src.embeddings import embed_texts
from src.vectorstore import SimpleFAISS

RAW = Path(settings.data_dir) / "raw"
IDX = Path("src/indexes")

def _read_textish(p: Path) -> str:
    if p.suffix.lower() in {".txt", ".md", ".html"}:
        return p.read_text(errors="ignore")
    if p.suffix.lower() == ".json":
        try:
            j = json.loads(p.read_text(errors="ignore"))
            return json.dumps(j, indent=2)
        except Exception:
            return p.read_text(errors="ignore")
    return ""

def _extract_any(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        return extract_pdf_to_db(p, doc_id=f"file:{p}", kind="permit")
    return _read_textish(p)

def build_index_for_folder(folder: Path, index_name: str):
    folder = Path(folder)
    texts, metas = [], []

    for p in folder.rglob("*"):
        if not p.is_file(): continue
        if p.suffix.lower() not in {".pdf", ".txt", ".md", ".json", ".html"}:
            continue
        try:
            raw = _extract_any(p)
            if not raw:
                continue
            chunks = chunk_text(raw, max_len=1100)
            for i, ch in enumerate(chunks):
                texts.append(ch["text"])
                metas.append({"path": str(p), "chunk": i, "citations": ch.get("citations", [])})
        except Exception as e:
            print(f"⚠️ Skipped {p}: {e}")

    if not texts:
        print("No indexable text found.")
        return

    vecs = embed_texts(texts)
    store = SimpleFAISS(IDX / f"{index_name}.faiss")
    store.build(vecs, metas)
    store.save()
    print(f"✓ Built index: {index_name} with {len(texts)} chunks")

def demo_build_all_indexes():
    # Build separate indexes so you can target retrieval:
    build_index_for_folder(RAW / "echo", "echo_docs")
    build_index_for_folder(RAW / "cedri", "cedri_docs")
    build_index_for_folder(RAW / "rblc", "rblc_docs")
    build_index_for_folder(RAW / "cfr", "cfr_docs")
    build_index_for_folder(RAW / "webfire", "webfire_docs")
