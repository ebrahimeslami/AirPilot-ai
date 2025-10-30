from pathlib import Path
import faiss
import numpy as np
import json

class SimpleFAISS:
    """A lightweight FAISS index wrapper."""

    def __init__(self, index_path: Path):
        self.index_path = Path(index_path)
        self.meta_path = self.index_path.with_suffix(".meta.json")
        self.index = None
        self.meta = []

    def build(self, embeddings: np.ndarray, metadatas: list):
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(d)
        self.index.add(embeddings)
        self.meta = metadatas

    def save(self):
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps(self.meta, indent=2))
        print(f"✅ FAISS index saved to {self.index_path}")

    def load(self):
        self.index = faiss.read_index(str(self.index_path))
        self.meta = json.loads(self.meta_path.read_text())

    def search(self, query_vec: np.ndarray, k: int = 5):
        D, I = self.index.search(query_vec, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            m = self.meta[idx]
            m["score"] = float(score)
            results.append(m)
        return results
