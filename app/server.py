import sys
from email_validator import validate_email, EmailNotValidError
from fastmcp import FastMCP
from sqlalchemy.orm import Session
from modules.database.database import init_db, SessionLocal
from modules.database.models import User
from dotenv import load_dotenv

from modules.llm.embeddings import generate_embedding
from modules.llm.vector_store import VectorStore

load_dotenv()

mcp = FastMCP("crm-assistente")

init_db()

# Inicializa o índice vetorial
vector_store = VectorStore(dimension=384)

@mcp.tool
def create_user(name: str, email: str, description: str) -> int:
    """
    Cria um novo usuário no CRM.

    Args:
        name: Nome completo do usuário.
        email: E-mail único do usuário.
        description: Descrição ou bio do usuário (usada para busca semântica).

    Retorna o ID do usuário criado.
    """
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(f"E-mail inválido: {e}")

    db: Session = SessionLocal()
    try:
        new_user = User(name=name, email=email, description=description)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        try:
            emb = generate_embedding(new_user.description)
            vector_store.add_embedding(new_user.id, emb)
        except Exception as vec_err:
            print(f"Erro ao gerar/salvar vector: {vec_err}", file=sys.stderr)

        return new_user.id

    except Exception as e:
        db.rollback()
        print(e, file=sys.stderr)
        raise
    finally:
        db.close()


@mcp.tool
def search_users(query: str, top_k: int = 5) -> list[dict]:
    """
    Realiza uma busca semântica para encontrar usuários com descrições similares à consulta.

    Args:
        query: Texto da busca (ex: 'especialista em IA').
        top_k: Número máximo de resultados (padrão: 5).

    Retorna uma lista de usuários com score de similaridade.
    """
    query_emb = generate_embedding(query)
    ids, dists = vector_store.search(query_emb, top_k=top_k)

    if not ids:
        return []

    db: Session = SessionLocal()
    try:
        users = db.query(User).filter(User.id.in_(ids)).all()
        user_map = {u.id: u for u in users}

        results = []
        for uid, dist in zip(ids, dists):
            if uid in user_map:
                u = user_map[uid]
                results.append({
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "description": u.description,
                    "score": float(dist)
                })

        results.sort(key=lambda x: x["score"])
        return results
    except Exception as e:
        print(e, file=sys.stderr)
        return []
    finally:
        db.close()


@mcp.tool
def get_user(user_id: int) -> dict:
    """
    Busca um usuário pelo ID.

    Args:
        user_id: ID numérico do usuário.

    Retorna os dados do usuário ou erro se não existir.
    """
    db: Session = SessionLocal()
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u:
            return {"error": "Usuario nao encontrado"}

        return {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "description": u.description
        }
    except Exception as e:
        print(e, file=sys.stderr)
        return {"error": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
