from src.embeddings import embed_texts
from src.vectorstore import SimpleFAISS
from pathlib import Path
import numpy as np

texts = [
    "This permit includes monitoring and recordkeeping per 40 CFR 70.6.",
    "BACT determination for NOx control using SCR technology."
]
vecs = embed_texts(texts)
store = SimpleFAISS(Path("src/indexes/demo.faiss"))
store.build(vecs, [{"text": t} for t in texts])
store.save()

# Search test
query = embed_texts(["NOx control using SCR"])
store.load()
res = store.search(query, k=2)
print(res)
