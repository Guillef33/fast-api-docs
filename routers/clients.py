from fastapi import APIRouter, HTTPException, Depends, Request 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

# Importamos la configuración de la DB
from database import get_db 
from models import ClientDB 
from schemas import Client, ClientCreate, ClientUpdate

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# --- CREATE (POST) ---
@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):

    new_client = ClientDB(**client.dict())
    
    db.add(new_client)
    db.commit()
    db.refresh(new_client) 
    
    return new_client

# --- READ ALL (GET) ---
@router.get("/", response_model=List[Client])
def get_clients(db: Session = Depends(get_db)):
    # Query directo a la tabla
    return db.query(ClientDB).all()

# --- READ ONE (GET) ---
@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    # Buscamos por ID
    client = db.query(ClientDB).filter(ClientDB.id == client_id).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

# --- UPDATE (PUT) ---
@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    # 1. Buscar
    client_query = db.query(ClientDB).filter(ClientDB.id == client_id)
    client = client_query.first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # 2. Actualizar solo los campos enviados
    update_data = data.dict(exclude_unset=True) 
    
    client_query.update(update_data, synchronize_session=False)
    
    # 3. Guardar cambios
    db.commit()
    db.refresh(client)
    
    return client

# --- DELETE (DELETE) ---
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientDB).filter(ClientDB.id == client_id).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(client)
    db.commit()
    
    return {"message": "Cliente eliminado"}

# --- SEED (Opcional) ---
@router.post("/seed-clients/")
def seed_clients(db: Session = Depends(get_db)):
    # Verifica si ya hay datos para no duplicar
    if db.query(ClientDB).count() > 0:
         return {"message": "La base de datos ya tiene datos"}

    sample_clients = [
        {"name": "Juan Pérez", "email": "juan@example.com", "phone": "123-456-7890"},
        {"name": "María García", "email": "maria@example.com", "phone": "987-654-3210"}
    ]
    
    for client_data in sample_clients:
        new_client = ClientDB(**client_data)
        db.add(new_client)
    
    db.commit()
    return {"message": "Clientes de ejemplo añadidos a Neon DB"}


