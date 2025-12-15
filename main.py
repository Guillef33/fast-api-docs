from fastapi import FastAPI
from database import engine, Base 
from models import ClientDB       
from routers import clients

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine) 


app = FastAPI()

app.include_router(clients.router, prefix="/clients", tags=["clients"])

@app.get("/")
def read_root():
    return {"message": "La API está conectada a Neon DB!"}
