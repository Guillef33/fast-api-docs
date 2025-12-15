import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Obtener la URL de la base de datos
# Si estás probando en local, asegúrate de tener tu archivo .env o exportar la variable
DATABASE_URL = os.getenv("DATABASE_URL")

# AJUSTE IMPORTANTE: SQLAlchemy a veces falla si la URL dice "postgres://"
# en lugar de "postgresql://". Este pequeño hack lo arregla automáticamente:
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Crear el motor (engine)
# connect_args={"check_same_thread": False} SOLO se usa en SQLite, aquí lo quitamos para Postgres
engine = create_engine(DATABASE_URL)

# 3. Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Crear la clase Base para los modelos
Base = declarative_base()

# 5. Dependencia para obtener la DB en cada request (la usaremos en el router)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()