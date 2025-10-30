## Indexers (parse → chunk → embed → FAISS)
## Walk a folder (PDF/TXT/JSON), extract text, chunk, embed, and build FAISS.
from pathlib import Path
import json
from typing import Iterable, List, Dict
from bs4 import BeautifulSoup
from src.config import settings
from src.chunking import chunk_text
from src.embeddings import embed_texts
from src.vectorstore import SimpleFAISS
from src.pdf_parser import extract_pdf_to_db

RAW = Path(settings.data_dir) / "raw"
IDX = Path("src/indexes")

# --- helper to extract text from different formats ---
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
    if p.suffix.lower() == ".xml" and "title40" in p.name:
        return _parse_cfr_xml(p)
    return _read_textish(p)

# --- parse CFR XML into section text ---
def _parse_cfr_xml(xml_path: Path) -> str:
    soup = BeautifulSoup(xml_path.read_text(encoding="utf-8", errors="ignore"), "xml")
    sections = []
    for sec in soup.find_all("SECTION"):
        secno = (sec.find("SECTNO") or {}).get_text(strip=True) if sec.find("SECTNO") else ""
        subj = (sec.find("SUBJECT") or {}).get_text(strip=True) if sec.find("SUBJECT") else ""
        body = sec.get_text(" ", strip=True)
        if secno:
            sections.append(f"{secno} - {subj}\n{body}")
    return "\n\n".join(sections)

# --- generic builder for folder ---
def build_index_for_folder(folder: Path, index_name: str):
    folder = Path(folder)
    texts, metas = [], []

    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".pdf", ".txt", ".md", ".json", ".html", ".xml"}:
            continue
        try:
            raw = _extract_any(p)
            if not raw:
                continue
            chunks = chunk_text(raw, max_len=1100)
            for i, ch in enumerate(chunks):
                texts.append(ch["text"])
                metas.append({
                    "path": str(p),
                    "chunk": i,
                    "citations": ch.get("citations", []),
                })
        except Exception as e:
            print(f"⚠️ Skipped {p}: {e}")

    if not texts:
        print(f"⚠️ No indexable text found in {folder}")
        return

    vecs = embed_texts(texts)
    store = SimpleFAISS(IDX / f"{index_name}.faiss")
    store.build(vecs, metas)
    store.save()
    print(f"✓ Built index: {index_name} with {len(texts)} chunks")

# --- new index builder that includes CFR sections ---
def build_all_indexes():
    # ordinary text sets
    build_index_for_folder(RAW / "echo", "echo_docs")
    build_index_for_folder(RAW / "cedri", "cedri_docs")
    build_index_for_folder(RAW / "rblc", "rblc_docs")
    build_index_for_folder(RAW / "webfire", "webfire_docs")
    # CFR: two separate indexes — one for JSON (structure) and one for XML sections
    build_index_for_folder(RAW / "cfr", "cfr_docs")
    build_index_for_folder(RAW / "cfr", "cfr_sections")

# --- CLI runner ---
if __name__ == "__main__":
    build_all_indexes()
