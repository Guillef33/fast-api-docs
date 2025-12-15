from fastapi import FastAPI, Request, Depends
from database import engine, Base, get_db
from models import ClientDB       
from routers import clients
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine) 

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.include_router(clients.router, prefix="/clients", tags=["clients"])

@app.get("/") 
def read_root(request: Request, db: Session = Depends(get_db)):
    clients_list = db.query(ClientDB).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "clients": clients_list
    })

