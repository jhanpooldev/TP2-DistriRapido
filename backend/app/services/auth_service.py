import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
import jwt

from backend.app.core.config import settings
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_mfa_token,
    decode_token,
)
from backend.app.core.mfa import (
    generate_totp_secret,
    get_totp_uri,
    generate_qr_code_data_url,
    verify_totp_code,
    hash_recovery_code,
    generate_backup_recovery_codes,
)
from backend.app.models.auth import (
    Usuario,
    SesionActiva,
    db_auth,
)
from backend.app.schemas.auth import (
    UsuarioRegisterRequest,
    UsuarioResponse,
    LoginResponse,
    MFASetupResponse,
    TokenResponse,
    LogoutResponse,
    EstadoSesionResponse,
)

class AuthService:
    def __init__(self, repo=db_auth):
        self.repo = repo

    def registrar_usuario(self, data: UsuarioRegisterRequest) -> UsuarioResponse:
        """Registra un nuevo usuario en el sistema con contraseña cifrada (RN-004)."""
        if self.repo.obtener_por_correo(data.correo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        nuevo_usuario = Usuario(
            id_usuario=str(uuid.uuid4()),
            nombre=data.nombre.strip(),
            correo=data.correo.lower().strip(),
            contrasena_hash=get_password_hash(data.contrasena),
            rol=data.rol or "Operador",
            mfa_activado=False,
            mfa_secreto=None
        )
        guardado = self.repo.crear_usuario(nuevo_usuario)
        return UsuarioResponse(
            id_usuario=guardado.id_usuario,
            nombre=guardado.nombre,
            correo=guardado.correo,
            rol=guardado.rol,
            mfa_activado=guardado.mfa_activado,
            fecha_creacion=guardado.fecha_creacion
        )

    def login_paso1(self, correo: str, contrasena: str) -> LoginResponse:
        """
        Paso 1 del inicio de sesión (RF-001-A).
        Valida credenciales, comprueba regla de bloqueo RN-002,
        y determina si emite sesión directa o desafío MFA.
        """
        usuario = self.repo.obtener_por_correo(correo)
        now = datetime.now(timezone.utc)

        # Si el usuario existe, verificar si está bloqueado por RN-002
        if usuario:
            if usuario.bloqueado_hasta and usuario.bloqueado_hasta > now:
                minutos_restantes = max(1, int((usuario.bloqueado_hasta - now).total_seconds() / 60))
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail=f"Cuenta bloqueada temporalmente por {minutos_restantes} minuto(s) debido a intentos fallidos (RN-002)."
                )
            elif usuario.bloqueado_hasta and usuario.bloqueado_hasta <= now:
                # El bloqueo ya expiró, restablecer contador
                usuario.bloqueado_hasta = None
                usuario.intentos_fallidos = 0
                self.repo.actualizar_usuario(usuario)

        # Validación de credenciales
        if not usuario or not verify_password(contrasena, usuario.contrasena_hash):
            if usuario:
                usuario.intentos_fallidos += 1
                if usuario.intentos_fallidos >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                    usuario.bloqueado_hasta = now + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
                    self.repo.actualizar_usuario(usuario)
                    raise HTTPException(
                        status_code=status.HTTP_423_LOCKED,
                        detail="Cuenta bloqueada temporalmente por 15 minutos debido a 3 intentos fallidos consecutivos (RN-002)."
                    )
                self.repo.actualizar_usuario(usuario)
            # Mensaje genérico para evitar enumeración de usuarios
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas."
            )

        # Credenciales correctas: resetear intentos fallidos
        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None
        self.repo.actualizar_usuario(usuario)

        # Si tiene MFA activo, generar token efímero de desafío
        if usuario.mfa_activado:
            mfa_token = create_mfa_token(usuario.id_usuario, usuario.correo)
            return LoginResponse(
                mfa_required=True,
                mfa_token=mfa_token,
                mensaje="Segundo factor requerido. Ingrese el código TOTP o código de respaldo."
            )

        # Si NO tiene MFA, emitir sesión definitiva (8 horas - RN-005)
        access_token = create_access_token(usuario.id_usuario, usuario.rol, usuario.correo)
        payload = decode_token(access_token)
        
        # Registrar sesión activa con jti para posibilitar revocación
        sesion = SesionActiva(
            id_sesion=str(uuid.uuid4()),
            jti=payload["jti"],
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            rol=usuario.rol,
            creado_en=now,
            expira_en=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        )
        self.repo.registrar_sesion(sesion)

        return LoginResponse(
            mfa_required=False,
            access_token=access_token,
            token_type="bearer",
            usuario=UsuarioResponse(
                id_usuario=usuario.id_usuario,
                nombre=usuario.nombre,
                correo=usuario.correo,
                rol=usuario.rol,
                mfa_activado=usuario.mfa_activado,
                fecha_creacion=usuario.fecha_creacion
            ),
            mensaje="Inicio de sesión exitoso."
        )

    def setup_mfa(self, usuario: Usuario) -> MFASetupResponse:
        """
        Genera secreto TOTP, URI, Código QR y 5 códigos de respaldo (RF-001-B).
        No activa el MFA hasta que el usuario envíe un código de prueba exitoso.
        """
        secreto = generate_totp_secret()
        uri = get_totp_uri(secreto, usuario.correo)
        qr_b64 = generate_qr_code_data_url(uri)
        plain_codes, hashed_codes = generate_backup_recovery_codes(count=5)

        # Guardar secreto temporalmente en el usuario
        usuario.mfa_secreto_temp = secreto
        self.repo.actualizar_usuario(usuario)
        self.repo.guardar_codigos_recuperacion(usuario.id_usuario, hashed_codes)

        return MFASetupResponse(
            secreto_base32=secreto,
            otpauth_uri=uri,
            qr_code_base64=qr_b64,
            codigos_respaldo=plain_codes,
            instrucciones="Escanee el código QR con Google Authenticator o ingrese la clave secreta manualmente, luego confirme enviando su código de 6 dígitos a /api/auth/mfa/enable."
        )

    def enable_mfa(self, usuario: Usuario, codigo_totp: str) -> Dict[str, Any]:
        """
        Confirma y activa definitivamente el MFA tras validar el primer código (RF-001-B).
        """
        if not usuario.mfa_secreto_temp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay un proceso de configuración MFA pendiente. Ejecute /api/auth/mfa/setup primero."
            )

        if not verify_totp_code(usuario.mfa_secreto_temp, codigo_totp):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de autenticación inválido o fuera de tiempo."
            )

        usuario.mfa_secreto = usuario.mfa_secreto_temp
        usuario.mfa_secreto_temp = None
        usuario.mfa_activado = True
        self.repo.actualizar_usuario(usuario)

        return {
            "success": True,
            "mensaje": "Autenticación multifactor activada exitosamente."
        }

    def verify_mfa_paso2(self, mfa_token: str, codigo: str) -> TokenResponse:
        """
        Verifica el segundo factor en el login (TOTP o código de respaldo) (RF-001-C).
        Aplica también la regla de reintentos fallidos RN-002.
        """
        try:
            payload = decode_token(mfa_token)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de desafío MFA inválido o expirado."
            )

        if payload.get("scope") != "mfa_pending":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token proporcionado no corresponde a un desafío MFA."
            )

        id_usuario = payload.get("sub")
        usuario = self.repo.obtener_por_id(id_usuario)
        if not usuario or not usuario.mfa_activado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o configuración MFA no encontrados."
            )

        now = datetime.now(timezone.utc)
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta > now:
            minutos = max(1, int((usuario.bloqueado_hasta - now).total_seconds() / 60))
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Cuenta bloqueada temporalmente por {minutos} minuto(s) por intentos fallidos."
            )

        codigo_limpio = codigo.strip().upper()
        es_valido = False
        es_backup = False
        codigo_backup_obj = None

        # Intento 1: Verificar si es código TOTP de 6 dígitos
        if len(codigo_limpio) == 6 and codigo_limpio.isdigit():
            es_valido = verify_totp_code(usuario.mfa_secreto, codigo_limpio)

        # Intento 2: Verificar si es código de respaldo
        if not es_valido:
            hash_ingresado = hash_recovery_code(codigo_limpio)
            codigos_guardados = self.repo.obtener_codigos_recuperacion(usuario.id_usuario)
            for c in codigos_guardados:
                if not c.usado and c.codigo_hash == hash_ingresado:
                    es_valido = True
                    es_backup = True
                    codigo_backup_obj = c
                    break

        if not es_valido:
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                usuario.bloqueado_hasta = now + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
                self.repo.actualizar_usuario(usuario)
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Cuenta bloqueada temporalmente por 15 minutos debido a 3 intentos fallidos consecutivos (RN-002)."
                )
            self.repo.actualizar_usuario(usuario)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Código de verificación o respaldo inválido."
            )

        # Código válido: quemar código de respaldo si fue usado
        if es_backup and codigo_backup_obj:
            codigo_backup_obj.usado = True
            codigo_backup_obj.fecha_uso = now

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None
        self.repo.actualizar_usuario(usuario)

        # Emitir sesión definitiva (8 horas)
        access_token = create_access_token(usuario.id_usuario, usuario.rol, usuario.correo)
        token_payload = decode_token(access_token)
        sesion = SesionActiva(
            id_sesion=str(uuid.uuid4()),
            jti=token_payload["jti"],
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            rol=usuario.rol,
            creado_en=now,
            expira_en=datetime.fromtimestamp(token_payload["exp"], tz=timezone.utc)
        )
        self.repo.registrar_sesion(sesion)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            usuario=UsuarioResponse(
                id_usuario=usuario.id_usuario,
                nombre=usuario.nombre,
                correo=usuario.correo,
                rol=usuario.rol,
                mfa_activado=usuario.mfa_activado,
                fecha_creacion=usuario.fecha_creacion
            ),
            mensaje="Autenticación MFA completada exitosamente."
        )

    def disable_mfa(self, usuario: Usuario, contrasena: str) -> Dict[str, Any]:
        """Desactiva el segundo factor requiriendo confirmación de contraseña."""
        if not verify_password(contrasena, usuario.contrasena_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta. No se puede desactivar MFA."
            )
        usuario.mfa_activado = False
        usuario.mfa_secreto = None
        self.repo.actualizar_usuario(usuario)
        return {"success": True, "mensaje": "Autenticación multifactor desactivada."}

    def logout(self, token: str) -> LogoutResponse:
        """
        Revoca inmediatamente el token de sesión (RF-001-D).
        Añade el JTI a la lista negra para impedir llamadas posteriores.
        """
        try:
            payload = decode_token(token)
            jti = payload.get("jti")
            if jti:
                self.repo.revocar_sesion(jti)
            return LogoutResponse(success=True, mensaje="Sesión cerrada y token revocado exitosamente.")
        except jwt.PyJWTError:
            return LogoutResponse(success=True, mensaje="Sesión cerrada.")

    def validar_sesion_activa(self, token: str) -> EstadoSesionResponse:
        """
        Valida que el token JWT sea válido, no haya expirado y no se encuentre revocado.
        """
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La sesión ha expirado (RN-005)."
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorización inválido."
            )

        jti = payload.get("jti")
        if not jti or self.repo.esta_jti_revocado(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revocado. La sesión fue cerrada previamente."
            )

        if payload.get("scope") != "access_token":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token sin privilegios de acceso a la aplicación."
            )

        id_usuario = payload.get("sub")
        usuario = self.repo.obtener_por_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario de la sesión no encontrado."
            )

        return EstadoSesionResponse(
            id_usuario=usuario.id_usuario,
            nombre=usuario.nombre,
            correo=usuario.correo,
            rol=usuario.rol,
            mfa_activado=usuario.mfa_activado,
            jti=jti,
            expira_en=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        )

auth_service = AuthService()
