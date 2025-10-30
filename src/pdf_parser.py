from pathlib import Path
import pdfplumber
from src.storage import upsert_doc, SessionLocal

def extract_pdf_to_db(pdf_path: Path, doc_id: str, kind: str = "permit"):
    """
    Extracts text from a PDF and stores it in the database.
    """
    print(f"Extracting text from: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    session = SessionLocal()
    upsert_doc(session, doc_id=doc_id, kind=kind, title=pdf_path.name,
               text=text, meta={"path": str(pdf_path)})
    session.close()
    print(f"✅ Stored {doc_id} ({kind}) in DB.")
    return text
