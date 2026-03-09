import os
import json
import faiss
import numpy as np
from pathlib import Path
from typing import List
from backend.rag.embedder import Embedder

# Paths
BASE_DIR = Path(__file__).resolve().parent
KB_DIR = BASE_DIR / "knowledege_base"
SAVE_DIR = Path("data/vector_index")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 400
OVERLAP = 50


def load_markdown_files() -> List[dict]:
    documents = []
    for file in KB_DIR.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "source": file.name,
            "content": text
        })

    return documents


def chunk_text(text: str) -> List[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), CHUNK_SIZE - OVERLAP):
        chunk = words[i:i + CHUNK_SIZE]
        chunks.append(" ".join(chunk))

    return chunks


def build_index():
    embedder = Embedder()
    documents = load_markdown_files()

    all_chunks = []
    metadata = []

    print("Chunking documents...")

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "source": doc["source"],
                "text": chunk
            })

    print(f"Total chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    embeddings = embedder.embed_batch(all_chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)

    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, str(SAVE_DIR / "math_index.faiss"))

    # Save metadata
    with open(SAVE_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Index built and saved successfully.")


if __name__ == "__main__":
    build_index()