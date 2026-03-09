from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class MemoryRetriever:

    def __init__(self):

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384
        self.index = faiss.IndexFlatIP(self.dimension)

        self.memory_texts = []

    def add_memory(self, text):

        embedding = self.embedder.encode([text])
        self.index.add(np.array(embedding).astype("float32"))

        self.memory_texts.append(text)

    def retrieve_similar(self, query, k=3):

        if len(self.memory_texts) == 0:
            return []

        query_vec = self.embedder.encode([query])

        scores, indices = self.index.search(
            np.array(query_vec).astype("float32"),
            k
        )

        results = []

        for idx in indices[0]:
            if idx < len(self.memory_texts):
                results.append(self.memory_texts[idx])

        return results