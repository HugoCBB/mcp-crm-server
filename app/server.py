from fastmcp import FastMCP
from sqlalchemy.orm import Session
from modules.database.database import init_db, SessionLocal
from modules.database.models import User
from dotenv import load_dotenv
from domain.user import CreateUserInput

load_dotenv()

mcp = FastMCP("crm-assistente")

init_db()

@mcp.tool
def create_user( input: CreateUserInput):
    """Registra um novo usuario no sistema"""
    db: Session = SessionLocal()
    try:
        newUser = User(
            name=input.name,
            email=input.email,
            description=input.description
        )
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return f"Usuario {newUser.name} criado com ID {newUser.id}"
    
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()