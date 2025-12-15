from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import DocumentDB, ClientDB, User
from schemas import Document, DocumentCreate, DocumentUpdate
from dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --- 2. CREAR (POST /) ---
# Esta ruta recibe JSON desde el Javascript
@router.post("/", response_model=Document)
def create_document(
    doc: DocumentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificamos que el cliente exista
    client = db.query(ClientDB).filter(ClientDB.id == doc.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    new_doc = DocumentDB(
        client_id=doc.client_id,
        type=doc.type,
        city=doc.city
    )
    
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


# --- 1. RUTA PRINCIPAL (GET /) ---
@router.get("/", include_in_schema=False)
def view_documents(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Consultamos documentos para la tabla
    documents = db.query(DocumentDB).all()
    clients_list = db.query(ClientDB).all()

    # Debug: imprimir para verificar
    print(f"Clientes encontrados: {len(clients_list)}")
    for client in clients_list:
        print(f"- {client.name}")
    
    return templates.TemplateResponse("documents.html", {
        "request": request,
        "documents": documents,
        "clients": clients_list,   
        "user": current_user
    })


# --- 3. ACTUALIZAR (PUT /{id}) ---
@router.put("/{doc_id}", response_model=Document)
def update_document(
    doc_id: int, 
    doc_update: DocumentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    update_data = doc_update.dict(exclude_unset=True)
    
    # Validación de cliente si viene en el update
    if 'client_id' in update_data:
         if not db.query(ClientDB).filter(ClientDB.id == update_data['client_id']).first():
             raise HTTPException(status_code=404, detail="Cliente inválido")

    for key, value in update_data.items():
        # Evitamos error si intentan actualizar 'name' que no existe en DB
        if hasattr(db_doc, key):
            setattr(db_doc, key, value)

    db.commit()
    db.refresh(db_doc)
    return db_doc

# --- 4. ELIMINAR (DELETE /{id}) ---
@router.delete("/{doc_id}")
def delete_document(
    doc_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    db.delete(db_doc)
    db.commit()
    return {"message": "Eliminado"}