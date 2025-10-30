from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading SentenceTransformer model (MiniLM-L6-v2)...")
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_texts(texts):
    model = get_model()
    print(f"Embedding {len(texts)} chunks ...")
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return np.array(vecs, dtype="float32")
