from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    """Carrega o modelo de embeddings se ainda não estiver carregado."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def generate_embedding(text: str) -> list[float]:
    """Gera um embedding para o texto fornecido."""
    model = get_model()
    embedding = model.encode(text)
    return embedding.tolist()
