from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv


load_dotenv()

# CONFIGURACIÓN
SECRET_KEY = os.getenv("DATABASE_URL") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto de encriptación (usamos bcrypt, el estándar de oro)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. Función para verificar si la contraseña escrita coincide con el hash guardado
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 2. Función para encriptar la contraseña antes de guardarla
def get_password_hash(password):
    return pwd_context.hash(password)

# 3. Función para crear el Token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt