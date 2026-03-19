import os
import sys
import faiss
import numpy as np
from utils.paths import FAISS_INDEX_PATH

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.index_path = FAISS_INDEX_PATH
        self.dimension = dimension
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self.index = self._load_or_create_index()

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            try:
                print(f"Carregando índice FAISS existente de {self.index_path}", file=sys.stderr)
                index = faiss.read_index(self.index_path)
                return index
            except Exception as e:
                print(f"Erro ao carregar índice FAISS: {e}, criando um novo.", file=sys.stderr)
                
        base_index = faiss.IndexFlatL2(self.dimension)
        index = faiss.IndexIDMap(base_index)
        return index

    def add_embedding(self, db_id: int, embedding: list[float]):
        """Adiciona um embedding e o mapeia para o ID do banco de dados SQLite."""
        vector = np.array([embedding], dtype=np.float32)
        ids = np.array([db_id], dtype=np.int64)
        
        self.index.add_with_ids(vector, ids)
        self.save_index()

    def search(self, query_embedding: list[float], top_k: int = 5):
        """Busca pelos embeddings mais próximos e retorna seus IDs e distâncias."""
        if self.index.ntotal == 0:
            return [], []
        vector = np.array([query_embedding], dtype=np.float32)
        k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(vector, k)
        return indices[0].tolist(), distances[0].tolist()
        
    def save_index(self):
        """Persiste o índice FAISS no disco."""
        faiss.write_index(self.index, self.index_path)

    def clear(self):
        """Limpa o índice em memória e no disco."""
        base_index = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIDMap(base_index)
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
