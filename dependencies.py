from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models import User
from security import SECRET_KEY, ALGORITHM

# 1. Creamos una "Señal" (Excepción) personalizada
class LoginRequired(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")

# 2. La función del "Portero"
def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Buscamos la cookie
    token = request.cookies.get("access_token")
    
    if not token:
        raise LoginRequired() # ¡Alarma! No hay cookie

    try:
        # La cookie viene como "Bearer laksjdflkasjd..."
        # Quitamos la palabra "Bearer "
        scheme, _, param = token.partition(" ")
        
        # Decodificamos el token
        payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise LoginRequired()
            
    except JWTError:
        raise LoginRequired() # ¡Alarma! Token falso o vencido

    # Buscamos al usuario en la DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise LoginRequired()

    return user