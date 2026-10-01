import pyotp
import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Verifica que el servicio esté activo y reportando estado saludable."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "RN-002" in data["lockout_policy"]

def test_registro_exitoso(client: TestClient):
    """Verifica el registro de un nuevo usuario con hash de contraseña seguro (RN-004)."""
    payload = {
        "nombre": "Jhanpool Flores",
        "correo": "jhanpool@distrirapido.pe",
        "contrasena": "ClaveSegura2026*",
        "rol": "Operador"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["correo"] == "jhanpool@distrirapido.pe"
    assert data["nombre"] == "Jhanpool Flores"
    assert data["rol"] == "Operador"
    assert data["mfa_activado"] is False
    assert "contrasena" not in data

def test_registro_correo_duplicado(client: TestClient):
    """Verifica que no se permita registrar dos usuarios con el mismo correo."""
    payload = {
        "nombre": "Usuario Uno",
        "correo": "duplicado@distrirapido.pe",
        "contrasena": "ClaveSegura2026*",
        "rol": "Operador"
    }
    r1 = client.post("/api/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/auth/register", json=payload)
    assert r2.status_code == 400
    assert "ya se encuentra registrado" in r2.json()["detail"]

def test_login_sin_mfa_exitoso(client: TestClient):
    """Verifica login directo cuando el usuario no tiene MFA habilitado (RF-001-A)."""
    # 1. Registrar usuario
    client.post("/api/auth/register", json={
        "nombre": "Ricardo Tucto",
        "correo": "ricardo@distrirapido.pe",
        "contrasena": "ClaveSegura2026*",
        "rol": "Operador"
    })

    # 2. Login
    response = client.post("/api/auth/login", json={
        "correo": "ricardo@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["mfa_required"] is False
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    assert data["usuario"]["correo"] == "ricardo@distrirapido.pe"

def test_login_credenciales_invalidas(client: TestClient):
    """Verifica rechazo con código 401 sin exponer qué campo falló (OWASP)."""
    client.post("/api/auth/register", json={
        "nombre": "Jhunior Cosme",
        "correo": "jhunior@distrirapido.pe",
        "contrasena": "ClaveSegura2026*",
        "rol": "Administrador"
    })

    response = client.post("/api/auth/login", json={
        "correo": "jhunior@distrirapido.pe",
        "contrasena": "clave_equivocada"
    })
    assert response.status_code == 401
    assert "Credenciales incorrectas" in response.json()["detail"]

def test_bloqueo_tres_intentos_fallidos_rn002(client: TestClient):
    """Verifica que tras 3 intentos fallidos consecutivos la cuenta se bloquee por 15 min (RN-002)."""
    client.post("/api/auth/register", json={
        "nombre": "Andrew Vega",
        "correo": "andrew@distrirapido.pe",
        "contrasena": "ClaveSegura2026*",
        "rol": "Operador"
    })

    # Intento 1
    r1 = client.post("/api/auth/login", json={"correo": "andrew@distrirapido.pe", "contrasena": "error1"})
    assert r1.status_code == 401

    # Intento 2
    r2 = client.post("/api/auth/login", json={"correo": "andrew@distrirapido.pe", "contrasena": "error2"})
    assert r2.status_code == 401

    # Intento 3: debe disparar bloqueo HTTP 423 Locked
    r3 = client.post("/api/auth/login", json={"correo": "andrew@distrirapido.pe", "contrasena": "error3"})
    assert r3.status_code == 423
    assert "Cuenta bloqueada temporalmente por 15 minutos" in r3.json()["detail"]

    # Intento 4 aun con clave correcta: debe seguir bloqueado
    r4 = client.post("/api/auth/login", json={"correo": "andrew@distrirapido.pe", "contrasena": "ClaveSegura2026*"})
    assert r4.status_code == 423
    assert "Cuenta bloqueada" in r4.json()["detail"]

def test_setup_mfa_exitoso(client: TestClient):
    """Verifica generación de secreto TOTP Base32, URI otpauth, QR y 5 códigos de respaldo (RF-001-B)."""
    client.post("/api/auth/register", json={
        "nombre": "Operador Uno",
        "correo": "operador1@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    login_res = client.post("/api/auth/login", json={
        "correo": "operador1@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = login_res.json()["access_token"]

    response = client.post(
        "/api/auth/mfa/setup",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["secreto_base32"]) == 32
    assert "otpauth://totp/" in data["otpauth_uri"]
    assert data["qr_code_base64"].startswith("data:image/png;base64,")
    assert len(data["codigos_respaldo"]) == 5

def test_enable_mfa_con_codigo_invalido(client: TestClient):
    """Verifica que no se active MFA si el código de 6 dígitos es incorrecto."""
    client.post("/api/auth/register", json={
        "nombre": "Operador Dos",
        "correo": "operador2@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    login_res = client.post("/api/auth/login", json={
        "correo": "operador2@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = login_res.json()["access_token"]

    client.post("/api/auth/mfa/setup", headers={"Authorization": f"Bearer {token}"})

    # Intentar activar con código erróneo
    response = client.post(
        "/api/auth/mfa/enable",
        headers={"Authorization": f"Bearer {token}"},
        json={"codigo_totp": "000000"}
    )
    assert response.status_code == 400
    assert "Código de autenticación inválido" in response.json()["detail"]

def test_enable_mfa_y_flujo_completo_dos_pasos(client: TestClient):
    """
    Verifica el flujo completo de activación de MFA y posterior login en 2 pasos:
    1. Login devuelve mfa_required=True y mfa_token
    2. /mfa/verify valida TOTP y emite sesión definitiva
    """
    client.post("/api/auth/register", json={
        "nombre": "Operador MFA",
        "correo": "mfa_user@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    login_res = client.post("/api/auth/login", json={
        "correo": "mfa_user@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = login_res.json()["access_token"]

    # 1. Setup MFA
    setup_res = client.post("/api/auth/mfa/setup", headers={"Authorization": f"Bearer {token}"})
    secret = setup_res.json()["secreto_base32"]

    # 2. Generar código válido usando pyotp
    totp = pyotp.TOTP(secret)
    valid_code = totp.now()

    # 3. Confirmar activación
    enable_res = client.post(
        "/api/auth/mfa/enable",
        headers={"Authorization": f"Bearer {token}"},
        json={"codigo_totp": valid_code}
    )
    assert enable_res.status_code == 200
    assert enable_res.json()["success"] is True

    # 4. Probar nuevo login: Paso 1 debe requerir MFA
    step1_res = client.post("/api/auth/login", json={
        "correo": "mfa_user@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    assert step1_res.status_code == 200
    step1_data = step1_res.json()
    assert step1_data["mfa_required"] is True
    assert step1_data["access_token"] is None
    mfa_token = step1_data["mfa_token"]
    assert mfa_token is not None

    # 5. Paso 2: Verificar con código TOTP actual
    current_code = totp.now()
    step2_res = client.post("/api/auth/mfa/verify", json={
        "mfa_token": mfa_token,
        "codigo": current_code
    })
    assert step2_res.status_code == 200
    step2_data = step2_res.json()
    assert step2_data["access_token"] is not None
    final_token = step2_data["access_token"]

    # 6. Usar el nuevo token para consultar /api/auth/me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {final_token}"})
    assert me_res.status_code == 200
    assert me_res.json()["correo"] == "mfa_user@distrirapido.pe"
    assert me_res.json()["mfa_activado"] is True

def test_recuperacion_con_codigo_respaldo_un_solo_uso(client: TestClient):
    """
    Verifica que un código de respaldo permita acceder si no se dispone del teléfono,
    y que dicho código quede quemado (usado) para prevenir repetición.
    """
    client.post("/api/auth/register", json={
        "nombre": "Operador Respaldo",
        "correo": "backup@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = client.post("/api/auth/login", json={
        "correo": "backup@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    }).json()["access_token"]

    # Setup MFA y activación
    setup_res = client.post("/api/auth/mfa/setup", headers={"Authorization": f"Bearer {token}"})
    secret = setup_res.json()["secreto_base32"]
    backup_codes = setup_res.json()["codigos_respaldo"]
    un_codigo_respaldo = backup_codes[0]

    totp = pyotp.TOTP(secret)
    client.post("/api/auth/mfa/enable", headers={"Authorization": f"Bearer {token}"}, json={"codigo_totp": totp.now()})

    # Login Paso 1
    mfa_token = client.post("/api/auth/login", json={
        "correo": "backup@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    }).json()["mfa_token"]

    # Login Paso 2 usando el código de respaldo
    res_verify = client.post("/api/auth/mfa/verify", json={
        "mfa_token": mfa_token,
        "codigo": un_codigo_respaldo
    })
    assert res_verify.status_code == 200
    assert res_verify.json()["access_token"] is not None

    # Intentar REUTILIZAR el mismo código de respaldo: debe ser rechazado
    mfa_token2 = client.post("/api/auth/login", json={
        "correo": "backup@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    }).json()["mfa_token"]

    res_reuse = client.post("/api/auth/mfa/verify", json={
        "mfa_token": mfa_token2,
        "codigo": un_codigo_respaldo
    })
    assert res_reuse.status_code == 401
    assert "Código de verificación o respaldo inválido" in res_reuse.json()["detail"]

def test_logout_y_revocacion_de_sesion(client: TestClient):
    """
    Verifica que el logout revoque el token JTI de forma inmediata (RF-001-D).
    Cualquier uso subsiguiente del token debe retornar HTTP 401.
    """
    client.post("/api/auth/register", json={
        "nombre": "Sesion Test",
        "correo": "sesion@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = client.post("/api/auth/login", json={
        "correo": "sesion@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    }).json()["access_token"]

    # 1. Verificar acceso activo
    r_me1 = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r_me1.status_code == 200

    # 2. Ejecutar Logout
    r_logout = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert r_logout.status_code == 200
    assert r_logout.json()["success"] is True

    # 3. Intentar volver a usar el mismo token post-logout: debe ser rechazado
    r_me2 = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r_me2.status_code == 401
    assert "Token revocado" in r_me2.json()["detail"]

def test_desactivar_mfa(client: TestClient):
    """Verifica que el usuario pueda desactivar MFA mediante confirmación de su contraseña."""
    client.post("/api/auth/register", json={
        "nombre": "Desactivar MFA",
        "correo": "desactivar@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    })
    token = client.post("/api/auth/login", json={
        "correo": "desactivar@distrirapido.pe",
        "contrasena": "ClaveSegura2026*"
    }).json()["access_token"]

    # Setup y activar
    setup_data = client.post("/api/auth/mfa/setup", headers={"Authorization": f"Bearer {token}"}).json()
    totp = pyotp.TOTP(setup_data["secreto_base32"])
    client.post("/api/auth/mfa/enable", headers={"Authorization": f"Bearer {token}"}, json={"codigo_totp": totp.now()})

    # Desactivar con clave errónea
    r_bad = client.post(
        "/api/auth/mfa/disable",
        headers={"Authorization": f"Bearer {token}"},
        json={"contrasena": "clave_falsa"}
    )
    assert r_bad.status_code == 401

    # Desactivar con clave correcta
    r_ok = client.post(
        "/api/auth/mfa/disable",
        headers={"Authorization": f"Bearer {token}"},
        json={"contrasena": "ClaveSegura2026*"}
    )
    assert r_ok.status_code == 200
    assert r_ok.json()["success"] is True

    # Comprobar en perfil que mfa_activado es False
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json()
    assert me["mfa_activado"] is False
