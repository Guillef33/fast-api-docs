from fastapi import FastAPI
from routers import clients

app = FastAPI()

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Hola FastAPI!"}

# Registrar router de clientes
app.include_router(clients.router, prefix="/clients", tags=["clients"])
