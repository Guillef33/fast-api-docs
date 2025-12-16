from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

class Client(ClientBase):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True 

class DocumentBase(BaseModel):
    type: str
    city: str | None = None

class DocumentCreate(DocumentBase):
    client_id: int

class DocumentUpdate(BaseModel):
    type: str | None = None
    city: str | None = None

class Document(DocumentBase):
    id: int
    client_id: int
    client: Client 
    
    class Config:
        from_attributes = True


# --- HEREDEROS ---
class HeirBase(BaseModel):
    full_name: str
    dni: str | None = None
    relationship: str
    address: str | None = None

class HeirCreate(HeirBase):
    inheritance_id: int # Necesitamos saber a qué trámite pertenece

class Heir(HeirBase):
    id: int
    class Config:
        from_attributes = True

# --- BIENES ---
class AssetBase(BaseModel):
    type: str
    name: str
    detail: str
    valuation: float = 0.0

class AssetCreate(AssetBase):
    inheritance_id: int

class Asset(AssetBase):
    id: int
    class Config:
        from_attributes = True

# --- SUCESIÓN (INHERITANCE) ---
class InheritanceBase(BaseModel):
    status: str = "Borrador"

class InheritanceCreate(InheritanceBase):
    client_id: int

class Inheritance(InheritanceBase):
    id: int
    client_id: int
    created_at: datetime
    # Opcional: Si queremos ver la lista completa al pedir la sucesión
    heirs: List[Heir] = [] 
    assets: List[Asset] = []

    class Config:
        from_attributes = True
