import pytest
import time
import json
from server import mcp
from sqlalchemy.orm import Session
from modules.database.database import SessionLocal, init_db
from modules.database.models import User
import os

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield


def test_create_user(setup_db, monkeypatch):
    from server import create_user
    
    unique_email = f"teste_{int(time.time())}@domain.com"
    
    result_raw = create_user(
        name="TesteUser",
        email=unique_email,
        description="Forte conhecimento em Inteligencia Artificial."
    )
    result = json.loads(result_raw)["id"]
    
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

def test_get_user(setup_db):
    from server import get_user
    result_raw = get_user(1)
    result = json.loads(result_raw)
    
    assert isinstance(result, (dict, int))

def test_search_users(setup_db):
    from server import search_users
    
    results_raw = search_users("Quem conhece inteligencia?", top_k=2)
    results = json.loads(results_raw)
    assert isinstance(results, list)
