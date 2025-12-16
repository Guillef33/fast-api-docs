from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class ClientDB(Base):
    __tablename__ = "clients"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)

    documents = relationship("DocumentDB", back_populates="client")
    inheritances = relationship("InheritanceDB", back_populates="client")

class DocumentDB(Base):
    __tablename__ = "documents"  

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

# La Carpeta de Sucesión (El trámite)
class InheritanceDB(Base):
    __tablename__ = "inheritances"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="Borrador") # Borrador, Finalizado
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con el Cliente (El fallecido/causante)
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("ClientDB", back_populates="inheritances")

    # Relación con Herederos y Bienes (Uno a Muchos)
    heirs = relationship("HeirDB", back_populates="inheritance")
    assets = relationship("AssetDB", back_populates="inheritance")


# Tabla de Herederos
class HeirDB(Base):
    __tablename__ = "heirs"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    dni = Column(String, nullable=True)
    kinship = Column(String) 
    address = Column(String, nullable=True)
    
    # Vinculación con la Sucesión
    inheritance_id = Column(Integer, ForeignKey("inheritances.id"))
    inheritance = relationship("InheritanceDB", back_populates="heirs")


# Tabla de Bienes (Activos)
class AssetDB(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)   # Inmueble, Automotor, Cuenta Bancaria
    name = Column(String)   # "Casa Calle 123" o "Ford Focus"
    detail = Column(String) # Matrícula, Nomenclatura Catastral, CBU
    valuation = Column(Float, default=0.0)
    
    # Vinculación con la Sucesión
    inheritance_id = Column(Integer, ForeignKey("inheritances.id"))
    inheritance = relationship("InheritanceDB", back_populates="assets")