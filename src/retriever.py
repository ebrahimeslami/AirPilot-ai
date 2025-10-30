## Simple helper to query any FAISS index.
from pathlib import Path
from typing import List, Dict
import numpy as np
from src.embeddings import embed_texts
from src.vectorstore import SimpleFAISS

def search_index(index_path: Path, query: str, k: int = 5) -> List[Dict]:
    qvec = embed_texts([query])
    store = SimpleFAISS(index_path)
    store.load()
    return store.search(qvec, k=k)
