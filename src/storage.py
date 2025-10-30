## Implements a lightweight SQLite database for storing parsed text, metadata, and document links.
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import settings

# Initialize the database engine and session
engine = create_engine(settings.db_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Doc(Base):
    """Stores parsed document text and metadata."""
    __tablename__ = "docs"
    id = Column(Integer, primary_key=True)
    doc_id = Column(String, unique=True, index=True)  # e.g., echo:12345 or file path
    kind = Column(String)  # cfr, permit, rblc, cedri, etc.
    title = Column(String)
    text = Column(Text)  # raw text or extracted content
    meta = Column(JSON)

# Create the database schema
Base.metadata.create_all(engine)

def upsert_doc(session, doc_id: str, kind: str, title: str, text: str, meta: dict):
    """Insert or update a document record."""
    obj = session.query(Doc).filter_by(doc_id=doc_id).first()
    if obj:
        obj.kind = kind
        obj.title = title
        obj.text = text
        obj.meta = meta
    else:
        obj = Doc(doc_id=doc_id, kind=kind, title=title, text=text, meta=meta)
        session.add(obj)
    session.commit()
    return obj
