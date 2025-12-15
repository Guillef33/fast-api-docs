from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ClientDB(Base):
    __tablename__ = "clients"  # Nombre de la tabla en Neon

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)

    documents = relationship("DocumentDB", back_populates="client")

class DocumentDB(Base):
    __tablename__ = "documents"  # Nombre de la tabla en Neon

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    city = Column(String, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id")) 
    
    client = relationship("ClientDB", back_populates="documents")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)