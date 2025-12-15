from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta

# Importamos todo lo que construimos antes
from database import get_db
from models import User
from security import verify_password, get_password_hash, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- RUTAS GET (Para mostrar los formularios HTML) ---

@router.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# --- RUTAS POST (Para procesar los datos) ---

@router.post("/register")
def register_user(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 1. Verificar si el usuario ya existe
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        # Si existe, devolvemos error (idealmente mostrarlo en el HTML, por ahora simple)
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # 2. Encriptar contraseña y guardar
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    
    # 3. Redirigir al Login
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 1. Buscar usuario
    user = db.query(User).filter(User.email == email).first()
    
    # 2. Validar contraseña
    if not user or not verify_password(password, user.hashed_password):
        # Podríamos devolver el HTML con un mensaje de error
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Credenciales inválidas"
        })

    # 3. Crear Token
    access_token = create_access_token(data={"sub": user.email})

    # 4. Crear respuesta con Cookie
    response = RedirectResponse(url="/clients", status_code=status.HTTP_303_SEE_OTHER)
    
    # Guardamos el token en una cookie segura HttpOnly
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True  # Importante para seguridad (JS no puede leerla)
    )
    
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response