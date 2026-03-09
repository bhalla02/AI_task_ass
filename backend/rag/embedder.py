import numpy as np

from sentence_transformers import SentenceTransformer
from typing import List 

class Embedder:
    def __init__(self,model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)


    def embed_text(self,text:str)->np.ndarray:
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
            )
        
        return embedding
    def embed_batch(self,texts:List[str])->np.ndarray:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
            )
        
        return embeddings