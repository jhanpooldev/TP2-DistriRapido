"""Pruebas de regresión para RF-002, RN-002 y RF-014."""
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import jwt
import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints.auth import resolver_id_rol
from app.api.v1.endpoints.dependencies import get_current_admin
from app.core import security
from app.core.config import get_settings
from app.core.database import get_db
from app.core.login_attempts import ControladorIntentosLogin, intentos_login
from app.core.security import create_access_token, decode_token, hash_password
from app.main import app
from app.models import Rol, Usuario
from app.schemas import UsuarioCreate

settings = get_settings()
CORREO = "operador@distrirapido.com"


class _FakeQuery:
    def __init__(self, resultado):
        self.resultado = resultado

    def options(self, *_args):
        return self

    def filter(self, *_args):
        return self

    def first(self):
        return self.resultado


class _FakeDB:
    """Sustituye la sesión sin base de datos: devuelve el resultado por modelo."""

    def __init__(self, resultados=None):
        self.resultados = resultados or {}

    def query(self, modelo):
        return _FakeQuery(self.resultados.get(modelo))

    def add(self, _obj):
        pass

    def commit(self):
        pass

    def refresh(self, obj):
        # La BD asignaría estos valores al hacer flush; el fake los completa
        # para que la serialización de UsuarioResponse sea equivalente.
        obj.id_usuario = obj.id_usuario or uuid.uuid4()
        obj.rol = obj.rol or Rol(id_rol=2, nombre="Operador Logístico")
        obj.fecha_creacion = datetime.now(timezone.utc)


def _usuario_valido():
    return SimpleNamespace(
        id_usuario=uuid.uuid4(),
        nombre="Operador Demo",
        correo=CORREO,
        id_rol=2,
        contrasena_hash=hash_password("clave123"),
        fecha_creacion=datetime.now(timezone.utc),
        rol=SimpleNamespace(id_rol=2, nombre="Operador Logístico", descripcion=None),
    )


@pytest.fixture(autouse=True)
def estado_limpio():
    intentos_login.reiniciar(CORREO)
    security._revoked_tokens.clear()
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


# --- RF-002 -----------------------------------------------------------------

def test_schema_permite_omitir_rol():
    usuario = UsuarioCreate(nombre="Nuevo", correo="nuevo@distrirapido.com", password="secreto123")
    assert usuario.id_rol is None


def test_resolver_id_rol_usa_operador_logistico_por_defecto():
    db = _FakeDB({Rol: SimpleNamespace(id_rol=2, nombre="Operador Logístico")})
    assert resolver_id_rol(db, None) == 2


def test_resolver_id_rol_respeta_rol_explicito():
    db = _FakeDB({Rol: SimpleNamespace(id_rol=1, nombre="Administrador")})
    assert resolver_id_rol(db, 1) == 1


def test_registro_sin_rol_crea_operador_y_mensaje_de_correo_duplicado():
    db = _FakeDB({Rol: Rol(id_rol=2, nombre="Operador Logístico")})
    app.dependency_overrides[get_current_admin] = lambda: SimpleNamespace(rol=SimpleNamespace(nombre="Administrador"))

    def obtener_db():
        yield db

    app.dependency_overrides[get_db] = obtener_db
    client = TestClient(app)

    respuesta = client.post(
        "/api/v1/auth/register",
        json={"nombre": "Nuevo", "correo": "nuevo@distrirapido.com", "password": "secreto123"},
    )
    assert respuesta.status_code == 201
    assert respuesta.json()["id_rol"] == 2

    db.resultados[Usuario] = SimpleNamespace(correo="nuevo@distrirapido.com")
    respuesta = client.post(
        "/api/v1/auth/register",
        json={"nombre": "Otro", "correo": "nuevo@distrirapido.com", "password": "secreto123"},
    )
    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El correo electrónico ya se encuentra registrado"


# --- RN-002 -----------------------------------------------------------------

def test_tres_fallos_bloquean_y_el_bloqueo_expira():
    reloj = {"valor": 1000.0}
    control = ControladorIntentosLogin(reloj=lambda: reloj["valor"], segundos_bloqueo=900)

    assert control.consultar(CORREO) == (False, 0)
    for _ in range(2):
        assert control.registrar_fallo(CORREO) == (False, 0)
    bloqueado, restante = control.registrar_fallo(CORREO)
    assert bloqueado is True
    assert restante == 900

    reloj["valor"] += 899
    assert control.consultar(CORREO)[0] is True
    reloj["valor"] += 1
    assert control.consultar(CORREO) == (False, 0)


def test_clave_normalizada_y_reinicio_tras_exito():
    control = ControladorIntentosLogin()
    control.registrar_fallo("  OPERADOR@Distrirapido.com ")
    control.registrar_fallo(CORREO)
    assert control.consultar(CORREO)[0] is False
    control.registrar_fallo(CORREO)
    assert control.consultar(CORREO)[0] is True
    control.reiniciar(CORREO)
    assert control.consultar(CORREO) == (False, 0)


def test_login_rechaza_contrasena_correcta_durante_bloqueo():
    usuario = _usuario_valido()
    app.dependency_overrides[get_db] = lambda: _FakeDB({Usuario: usuario})
    client = TestClient(app)
    datos = {"correo": CORREO, "password": "clave123"}

    for _ in range(3):
        respuesta = client.post("/api/v1/auth/login", data={**datos, "password": "incorrecta"})
        assert respuesta.status_code == 401
        assert respuesta.json()["detail"] == "Credenciales inválidas"

    respuesta = client.post("/api/v1/auth/login", data=datos)
    assert respuesta.status_code == 429
    assert "Demasiados intentos fallidos" in respuesta.json()["detail"]
    assert int(respuesta.headers["Retry-After"]) > 0


def test_login_correcto_reinicia_contador():
    usuario = _usuario_valido()
    app.dependency_overrides[get_db] = lambda: _FakeDB({Usuario: usuario})
    client = TestClient(app)
    datos = {"correo": CORREO, "password": "clave123"}

    client.post("/api/v1/auth/login", data={**datos, "password": "incorrecta"})
    respuesta = client.post("/api/v1/auth/login", data=datos)
    assert respuesta.status_code == 200
    assert intentos_login.consultar(CORREO) == (False, 0)


# --- RF-014 -----------------------------------------------------------------

def test_token_incluye_jti_y_puede_revocarse():
    token = create_access_token({"sub": str(uuid.uuid4())})
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("jti")

    assert security.revocar_token(token) is True
    assert decode_token(token) is None


def test_revocar_un_token_deja_otras_sesiones_activas():
    primero = create_access_token({"sub": "uno"})
    segundo = create_access_token({"sub": "dos"})
    security.revocar_token(primero)
    assert decode_token(primero) is None
    assert decode_token(segundo) is not None


def test_revocar_token_forjado_devuelve_false():
    forjado = jwt.encode({"sub": "x"}, "clave-del-atacante", algorithm="HS256")
    assert security.revocar_token(forjado) is False


def test_logout_invalida_el_token_en_siguiente_peticion():
    usuario = _usuario_valido()
    app.dependency_overrides[get_db] = lambda: _FakeDB({Usuario: usuario})
    client = TestClient(app)
    token = client.post("/api/v1/auth/login", data={"correo": CORREO, "password": "clave123"}).json()["access_token"]
    cabecera = {"Authorization": f"Bearer {token}"}

    assert client.get("/api/v1/auth/me", headers=cabecera).status_code == 200
    respuesta = client.post("/api/v1/auth/logout", headers=cabecera)
    assert respuesta.status_code == 200
    assert client.get("/api/v1/auth/me", headers=cabecera).status_code == 401


def test_logout_sin_token_devuelve_401():
    assert TestClient(app).post("/api/v1/auth/logout").status_code == 401
