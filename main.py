from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from database import engine, Base, get_db
from models import ClientDB, DocumentDB, User, InheritanceDB, HeirDB, AssetDB     
from routers import clients, auth, documents, inheritances
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dependencies import get_current_user, LoginRequired 

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine) 

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Importamos la dependencia y la excepción
from dependencies import get_current_user, LoginRequired

app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(
    inheritances.router, 
    prefix="/inheritances", 
    tags=["inheritances"],
    dependencies=[Depends(get_current_user)] 
)
app.include_router(auth.router, tags=["auth"])

@app.exception_handler(LoginRequired) 
async def login_required_handler(request: Request, exc: LoginRequired):
    return RedirectResponse(url="/login")


@app.get("/") 
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/clients") 
def clients_list(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    clients_list = db.query(ClientDB).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "clients": clients_list,
        "user": user
    })
