from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Imports del proyecto
from database import get_db
from models import InheritanceDB, ClientDB, User, HeirDB, AssetDB
from dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- 1. CREAR SUCESIÓN (INICIAR TRÁMITE) ---
# Esta ruta se llama desde el botón en la lista de clientes
@router.get("/create/{client_id}")
def create_inheritance(
    client_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verificar que el cliente existe
    client = db.query(ClientDB).filter(ClientDB.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2. Crear la "Carpeta" vacía
    new_inheritance = InheritanceDB(
        client_id=client_id,
        status="En Proceso"
    )
    db.add(new_inheritance)
    db.commit()
    db.refresh(new_inheritance)

    # 3. Redirigir al "Espacio de Trabajo" de esta sucesión
    return RedirectResponse(url=f"/inheritances/{new_inheritance.id}", status_code=303)


# --- 2. EL ESPACIO DE TRABAJO (DASHBOARD DE LA SUCESIÓN) ---
@router.get("/{inheritance_id}", include_in_schema=False)
def view_inheritance_detail(
    inheritance_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Traemos la sucesión y, gracias a las relaciones en models.py, 
    # también vendrán pegados el .client, .heirs y .assets
    inheritance = db.query(InheritanceDB).filter(InheritanceDB.id == inheritance_id).first()
    
    if not inheritance:
        raise HTTPException(status_code=404, detail="Sucesión no encontrada")

    return templates.TemplateResponse("inheritance_detail.html", {
        "request": request,
        "inheritance": inheritance,
        "user": current_user
    })