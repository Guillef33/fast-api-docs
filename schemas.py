from pydantic import BaseModel

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

