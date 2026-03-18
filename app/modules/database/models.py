from sqlalchemy import Column, Integer, String
from .database import Base
from pgvector.sqlalchemy import Vector

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    embedding = Column(Vector(384))


