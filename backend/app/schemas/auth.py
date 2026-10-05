from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class UsuarioRegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    contrasena: str = Field(..., min_length=8, description="Contraseña de al menos 8 caracteres")
    rol: Optional[str] = Field("Operador", description="Rol del usuario (Administrador, Operador, Gerente)")

class UsuarioResponse(BaseModel):
    id_usuario: str
    nombre: str
    correo: str
    rol: str
    mfa_activado: bool
    fecha_creacion: datetime

class LoginRequest(BaseModel):
    correo: EmailStr = Field(..., description="Correo electrónico del usuario")
    contrasena: str = Field(..., description="Contraseña del usuario")

class LoginResponse(BaseModel):
    mfa_required: bool
    mfa_token: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    usuario: Optional[UsuarioResponse] = None
    mensaje: str

class MFASetupResponse(BaseModel):
    secreto_base32: str
    otpauth_uri: str
    qr_code_base64: str
    codigos_respaldo: List[str]
    instrucciones: str

class MFAEnableRequest(BaseModel):
    codigo_totp: str = Field(..., pattern=r"^\d{6}$", description="Código de 6 dígitos de la app autenticadora")

class MFAVerifyRequest(BaseModel):
    mfa_token: str = Field(..., description="Token efímero de desafío recibido en el paso 1")
    codigo: str = Field(..., min_length=6, max_length=12, description="Código TOTP de 6 dígitos o código de respaldo")

class MFADisableRequest(BaseModel):
    contrasena: str = Field(..., description="Contraseña para confirmar la desactivación del segundo factor")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
    mensaje: str

class LogoutResponse(BaseModel):
    success: bool
    mensaje: str

class EstadoSesionResponse(BaseModel):
    id_usuario: str
    nombre: str
    correo: str
    rol: str
    mfa_activado: bool
    jti: str
    expira_en: datetime
