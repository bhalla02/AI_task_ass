import json
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict
from backend.rag.embedder import Embedder


class Retriever:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.index_path = self.project_root / "data" / "vector_index" / "math_index.faiss"
        self.meta_path = self.project_root / "data" / "vector_index" / "metadata.json"

        if not self.index_path.exists():
            raise FileNotFoundError("FAISS index not found. Run build_index.py first.")

        self.index = faiss.read_index(str(self.index_path))

        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.embedder = Embedder()

    def retrieve(self, query: str, top_k: int = 3, score_threshold: float = 0.3) -> List[Dict]:
        """
        Returns top_k relevant chunks with similarity scores.
        """

        query_vector = self.embedder.embed_text(query).reshape(1, -1)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            if score < score_threshold:
                continue

            results.append({
                "text": self.metadata[idx]["text"],
                "source": self.metadata[idx]["source"],
                "score": float(score)
            })

        return results