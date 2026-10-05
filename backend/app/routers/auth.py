from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.app.models.auth import Usuario, db_auth
from backend.app.schemas.auth import (
    UsuarioRegisterRequest,
    UsuarioResponse,
    LoginRequest,
    LoginResponse,
    MFASetupResponse,
    MFAEnableRequest,
    MFAVerifyRequest,
    MFADisableRequest,
    TokenResponse,
    LogoutResponse,
    EstadoSesionResponse,
)
from backend.app.services.auth_service import auth_service

router = APIRouter(prefix="/api/auth", tags=["Autenticación y Sesiones Seguras"])
security_scheme = HTTPBearer(auto_error=False)

def get_current_user_and_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> tuple[Usuario, str]:
    """Dependencia para validar token Bearer y obtener usuario autenticado con sesión activa."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere encabezado Authorization: Bearer <token>"
        )
    token = credentials.credentials
    sesion_info = auth_service.validar_sesion_activa(token)
    usuario = db_auth.obtener_por_id(sesion_info.id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado."
        )
    return usuario, token

def get_current_user(data: tuple[Usuario, str] = Depends(get_current_user_and_token)) -> Usuario:
    return data[0]

@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario con contraseña cifrada bajo el estándar RN-004."
)
def registrar_usuario(data: UsuarioRegisterRequest):
    return auth_service.registrar_usuario(data)

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Inicio de sesión (Paso 1)",
    description="Valida credenciales. Si el usuario tiene MFA habilitado, retorna un mfa_token temporal (5 min). Si no, entrega la sesión definitiva (8 horas)."
)
def login(data: LoginRequest):
    return auth_service.login_paso1(correo=data.correo, contrasena=data.contrasena)

@router.post(
    "/mfa/setup",
    response_model=MFASetupResponse,
    status_code=status.HTTP_200_OK,
    summary="Generar configuración MFA (TOTP + QR + Códigos de Respaldo)",
    description="Requiere sesión activa. Genera el secreto TOTP, URI otpauth, imagen QR en Base64 y 5 códigos de respaldo."
)
def mfa_setup(usuario: Usuario = Depends(get_current_user)):
    return auth_service.setup_mfa(usuario)

@router.post(
    "/mfa/enable",
    status_code=status.HTTP_200_OK,
    summary="Activar MFA con código de prueba",
    description="Confirma la posesión del dispositivo validando el primer código de 6 dígitos emitido por Google Authenticator."
)
def mfa_enable(data: MFAEnableRequest, usuario: Usuario = Depends(get_current_user)):
    return auth_service.enable_mfa(usuario, data.codigo_totp)

@router.post(
    "/mfa/verify",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar desafío MFA (Paso 2)",
    description="Valida el código TOTP o un código de respaldo junto al mfa_token para emitir la sesión final definitiva."
)
def mfa_verify(data: MFAVerifyRequest):
    return auth_service.verify_mfa_paso2(mfa_token=data.mfa_token, codigo=data.codigo)

@router.post(
    "/mfa/disable",
    status_code=status.HTTP_200_OK,
    summary="Desactivar MFA",
    description="Desactiva el segundo factor requiriendo confirmación de contraseña."
)
def mfa_disable(data: MFADisableRequest, usuario: Usuario = Depends(get_current_user)):
    return auth_service.disable_mfa(usuario, data.contrasena)

@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Cerrar sesión y revocar token",
    description="Revoca de forma inmediata el JWT actual añadiendo su JTI a la lista negra."
)
def logout(data: tuple[Usuario, str] = Depends(get_current_user_and_token)):
    _, token = data
    return auth_service.logout(token)

@router.get(
    "/me",
    response_model=EstadoSesionResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario autenticado y sesión",
    description="Retorna el perfil del usuario autenticado y el tiempo restante de expiración de la sesión activa."
)
def obtener_perfil(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado.")
    return auth_service.validar_sesion_activa(credentials.credentials)

@router.get(
    "/sessions",
    status_code=status.HTTP_200_OK,
    summary="Listar sesiones del usuario",
    description="Muestra el historial y estado de revocación de las sesiones asociadas al usuario."
)
def listar_sesiones(usuario: Usuario = Depends(get_current_user)):
    sesiones = [
        {
            "id_sesion": s.id_sesion,
            "jti": s.jti,
            "creado_en": s.creado_en.isoformat(),
            "expira_en": s.expira_en.isoformat(),
            "revocado": s.revocado
        }
        for s in db_auth.sesiones_por_jti.values()
        if s.id_usuario == usuario.id_usuario
    ]
    return {"sesiones": sesiones}
