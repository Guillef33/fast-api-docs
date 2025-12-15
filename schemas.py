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
