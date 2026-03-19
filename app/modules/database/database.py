import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from utils.paths import DATABASE_FILE

load_dotenv()

DEFAULT_SQLITE = f"sqlite:///{DATABASE_FILE}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from . import models
    try:
        Base.metadata.create_all(bind=engine)
        print(f"Banco de dados SQLite inicializado em: {DATABASE_URL}", file=sys.stderr)
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}", file=sys.stderr)
