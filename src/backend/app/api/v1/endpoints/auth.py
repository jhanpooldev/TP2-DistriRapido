import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.login_attempts import intentos_login
from app.core.security import hash_password, verify_password, create_access_token, revocar_token
from app.models import Usuario, Rol
from app.schemas import UsuarioCreate, UsuarioResponse, Token
from app.api.v1.endpoints.dependencies import get_current_user, get_current_admin, security

router = APIRouter()
logger = logging.getLogger(__name__)

ROL_POR_DEFECTO = "Operador Logístico"


def resolver_id_rol(db: Session, id_rol: Optional[int]) -> int:
    """RF-002: usa el rol indicado o 'Operador Logístico' si se omite."""
    if id_rol is not None:
        if not db.query(Rol).filter(Rol.id_rol == id_rol).first():
            raise HTTPException(status_code=400, detail="Rol no existe")
        return id_rol
    rol = db.query(Rol).filter(Rol.nombre == ROL_POR_DEFECTO).first()
    if rol is None:
        raise HTTPException(
            status_code=500,
            detail=f"Rol por defecto '{ROL_POR_DEFECTO}' no configurado",
        )
    return rol.id_rol


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
        raise HTTPException(status_code=400, detail="El correo electrónico ya se encuentra registrado")
    id_rol = resolver_id_rol(db, user.id_rol)
    hashed = hash_password(user.password)
    db_user = Usuario(nombre=user.nombre, correo=user.correo, contrasena_hash=hashed, id_rol=id_rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(correo: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    clave = intentos_login.normalizar_clave(correo)
    bloqueado, restante = intentos_login.consultar(clave)
    if bloqueado:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Intenta nuevamente en {restante} segundos.",
            headers={"Retry-After": str(restante)},
        )

    user = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.correo == correo)
        .first()
    )
    if not user or not verify_password(password, user.contrasena_hash):
        # RN-002: a partir del tercer fallo consecutivo la clave queda
        # bloqueada 15 minutos incluso si la contraseña llega a ser correcta.
        intentos_login.registrar_fallo(clave)
        # Se registra el intento sin incluir la contrasena. El correo se limpia
        # de saltos de linea para evitar inyeccion de lineas en el log.
        correo_registrado = correo.replace("\r", " ").replace("\n", " ")[:120]
        logger.warning("Inicio de sesion fallido para correo=%s", correo_registrado)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    intentos_login.reiniciar(clave)
    token = create_access_token({"sub": str(user.id_usuario), "rol": user.rol.nombre})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    current_user: Usuario = Depends(get_current_user),
):
    """RF-014: cierra la sesión revocando el token usado en la petición."""
    if credentials is None or not revocar_token(credentials.credentials):
        raise HTTPException(status_code=400, detail="No se pudo revocar la sesión")
    return {"mensaje": "Sesión cerrada correctamente"}


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user
