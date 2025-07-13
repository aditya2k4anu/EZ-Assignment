import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, chunks):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = [c["text"] for c in chunks]
        self.cids = [c["cid"] for c in chunks]

        embs = self.model.encode(self.texts, convert_to_numpy=True).astype("float32")
        self.index = faiss.IndexFlatL2(embs.shape[1])
        self.index.add(embs)

    def query(self, query, k=3):
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        D, I = self.index.search(q_emb, k)
        return [{
            "cid": self.cids[i],
            "text": self.texts[i],
            "score": float(D[0][rank])
        } for rank, i in enumerate(I[0])]
