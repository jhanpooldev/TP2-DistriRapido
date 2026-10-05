from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models import Usuario, Rol
from app.schemas import UsuarioCreate, UsuarioResponse, Token
from app.api.v1.endpoints.dependencies import get_current_user, get_current_admin

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(
    user: UsuarioCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Alta de usuarios. Solo un Administrador puede crearlos.

    Antes este endpoint era publico y permitia elegir cualquier id_rol, con lo
    que cualquiera podia auto-asignarse el rol de Administrador.
    """
    if db.query(Usuario).filter(Usuario.correo == user.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    if not db.query(Rol).filter(Rol.id_rol == user.id_rol).first():
        raise HTTPException(status_code=400, detail="Rol no existe")
    hashed = hash_password(user.password)
    db_user = Usuario(nombre=user.nombre, correo=user.correo, contrasena_hash=hashed, id_rol=user.id_rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(correo: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not user or not verify_password(password, user.contrasena_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id_usuario), "rol": user.rol.nombre})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user