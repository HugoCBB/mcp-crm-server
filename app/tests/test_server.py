import pytest
import time
from sqlalchemy.orm import Session
from modules.database.database import SessionLocal, init_db
from modules.database.models import User

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield


def test_create_user(setup_db):
    from server import create_user
    
    unique_email = f"teste_{int(time.time())}@domain.com"
    
    result = create_user(
        name="TesteUser",
        email=unique_email,
        description="Forte conhecimento em Inteligencia Artificial."
    )
    
    assert isinstance(result, int)
    assert result > 0
    
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == unique_email).first()
        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def test_create_user_invalid_email(setup_db):
    from server import create_user
    
    with pytest.raises(ValueError, match="E-mail inválido"):
        create_user(name="Teste", email="email-invalido", description="Teste.")


def test_get_user(setup_db):
    from server import get_user
    result = get_user(1)
    
    assert isinstance(result, dict)


def test_get_user_not_found(setup_db):
    from server import get_user
    result = get_user(99999)
    
    assert isinstance(result, dict)
    assert "error" in result


def test_search_users(setup_db):
    from server import search_users
    
    results = search_users("Quem conhece inteligencia?", top_k=2)
    assert isinstance(results, list)
