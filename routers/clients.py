from fastapi import APIRouter, HTTPException
from schemas import Client, ClientCreate, ClientUpdate
from models import clients_db

router = APIRouter()
current_id = 1

@router.post("/", response_model=Client)
def create_client(client: ClientCreate):
    global current_id
    new_client = Client(id=current_id, **client.dict())
    clients_db.append(new_client)
    current_id += 1
    return new_client

@router.get("/", response_model=list[Client])
def get_clients():
    return clients_db

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int):
    for client in clients_db:
        if client.id == client_id:
            return client
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, data: ClientUpdate):
    for index, client in enumerate(clients_db):
        if client.id == client_id:
            updated_data = data.dict(exclude_unset=True)
            updated_client = client.copy(update=updated_data)
            clients_db[index] = updated_client
            return updated_client
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.delete("/{client_id}")
def delete_client(client_id: int):
    for index, client in enumerate(clients_db):
        if client.id == client_id:
            clients_db.pop(index)
            return {"message": "Cliente eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.post("/seed-clients/")
def seed_clients():
    global current_id
    sample_clients = [
        {"name": "Juan Pérez", "email": "juan@example.com", "phone": "123-456-7890"},
        {"name": "María García", "email": "maria@example.com", "phone": "98 7-654-3210"}
    ]
    for client_data in sample_clients:  
        new_client = Client(id=current_id, **client_data)
        clients_db.append(new_client)
        current_id += 1
    return {"message": "Clientes de ejemplo añadidos"}  