import sys
from sqlalchemy.orm import Session
from modules.database.database import init_db, SessionLocal
from modules.database.models import User
from modules.llm.embeddings import generate_embedding
from modules.llm.vector_store import VectorStore

def seed():
    print("Iniciando semeadura do banco de dados...", file=sys.stderr)
    init_db()
    
    db: Session = SessionLocal()
    vector_store = VectorStore(dimension=384) 
    
    sample_users = [
        {
            "name": "Alice Souza",
            "email": "alice@tech.com",
            "description": "Especialista em inteligência artificial e aprendizado de máquina com 10 anos de experiência."
        },
        {
            "name": "Bob Ferreira",
            "email": "bob@dev.com",
            "description": "Desenvolvedor Full Stack focado em React, Node.js e arquitetura de microsserviços."
        },
        {
            "name": "Carlos Mendes",
            "email": "carlos@vendas.com",
            "description": "Gerente de vendas com foco em CRM e expansão de mercado na América Latina."
        },
        {
            "name": "Daniela Lima",
            "email": "daniela@data.com",
            "description": "Cientista de dados apaixonada por visualização de dados e análise estatística complexa."
        },
        {
            "name": "Eduardo Rocha",
            "email": "eduardo@infra.com",
            "description": "Engenheiro de DevOps especializado em Kubernetes, Docker e automação de infraestrutura."
        }
    ]
    
    try:
        for user_data in sample_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"Usuário {user_data['email']} já existe. Pulando...", file=sys.stderr)
                continue
                
            new_user = User(
                name=user_data["name"],
                email=user_data["email"],
                description=user_data["description"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"Gerando embedding para {new_user.name}...", file=sys.stderr)
            emb = generate_embedding(new_user.description)
            vector_store.add_embedding(new_user.id, emb)
            
        print("Semeadura concluída com sucesso!", file=sys.stderr)
        
    except Exception as e:
        print(f"Erro durante a semeadura: {e}", file=sys.stderr)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
