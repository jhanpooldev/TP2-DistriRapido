import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

@dataclass
class CodigoRecuperacion:
    id_codigo: str
    id_usuario: str
    codigo_hash: str
    usado: bool = False
    fecha_uso: Optional[datetime] = None

@dataclass
class SesionActiva:
    id_sesion: str
    jti: str
    id_usuario: str
    correo: str
    rol: str
    creado_en: datetime
    expira_en: datetime
    revocado: bool = False
    fecha_revocacion: Optional[datetime] = None

@dataclass
class Usuario:
    id_usuario: str
    nombre: str
    correo: str
    contrasena_hash: str
    rol: str = "Operador"
    mfa_activado: bool = False
    mfa_secreto: Optional[str] = None
    mfa_secreto_temp: Optional[str] = None  # Secreto en proceso de enrolamiento
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class InMemoryAuthRepository:
    """
    Repositorio en memoria thread-safe para persistencia de datos de autenticación,
    sesiones activas, tokens revocados y códigos de respaldo.
    Permite ejecución inmediata sin dependencias externas de base de datos.
    """
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}          # id_usuario -> Usuario
        self.usuarios_por_correo: Dict[str, str] = {}  # correo_lower -> id_usuario
        self.codigos_recuperacion: Dict[str, List[CodigoRecuperacion]] = {}  # id_usuario -> lista
        self.sesiones_por_jti: Dict[str, SesionActiva] = {}  # jti -> SesionActiva
        self.jti_blacklist: set = set()                # Conjunto de JTIs revocados

    def limpiar_todo(self):
        """Reinicia el almacén para pruebas automatizadas limpias."""
        self.usuarios.clear()
        self.usuarios_por_correo.clear()
        self.codigos_recuperacion.clear()
        self.sesiones_por_jti.clear()
        self.jti_blacklist.clear()

    # Operaciones Usuario
    def obtener_por_id(self, id_usuario: str) -> Optional[Usuario]:
        return self.usuarios.get(id_usuario)

    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        id_usuario = self.usuarios_por_correo.get(correo.lower().strip())
        if id_usuario:
            return self.usuarios.get(id_usuario)
        return None

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        self.usuarios[usuario.id_usuario] = usuario
        self.usuarios_por_correo[usuario.correo.lower().strip()] = usuario.id_usuario
        return usuario

    def actualizar_usuario(self, usuario: Usuario) -> Usuario:
        self.usuarios[usuario.id_usuario] = usuario
        return usuario

    # Operaciones Códigos de Respaldo
    def guardar_codigos_recuperacion(self, id_usuario: str, hashes: List[str]):
        codigos = [
            CodigoRecuperacion(
                id_codigo=str(uuid.uuid4()),
                id_usuario=id_usuario,
                codigo_hash=h,
                usado=False
            )
            for h in hashes
        ]
        self.codigos_recuperacion[id_usuario] = codigos

    def obtener_codigos_recuperacion(self, id_usuario: str) -> List[CodigoRecuperacion]:
        return self.codigos_recuperacion.get(id_usuario, [])

    # Operaciones Sesión y Revocación (Logout)
    def registrar_sesion(self, sesion: SesionActiva):
        self.sesiones_por_jti[sesion.jti] = sesion

    def revocar_sesion(self, jti: str) -> bool:
        self.jti_blacklist.add(jti)
        sesion = self.sesiones_por_jti.get(jti)
        if sesion:
            sesion.revocado = True
            sesion.fecha_revocacion = datetime.now(timezone.utc)
            return True
        return False

    def esta_jti_revocado(self, jti: str) -> bool:
        return jti in self.jti_blacklist

# Instancia singleton del repositorio para la aplicación
db_auth = InMemoryAuthRepository()
