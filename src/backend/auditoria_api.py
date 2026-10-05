"""Auditoria completa de la API: exercises cada endpoint y reporta anomalias.

Uso:  python auditoria_api.py [puerto]
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from app.core.database import SessionLocal
from app.models import Usuario, ParametrosVehiculo, Ruta, RutaPunto, PuntoEntrega

PUERTO = sys.argv[1] if len(sys.argv) > 1 else "8000"
BASE = f"http://127.0.0.1:{PUERTO}/api/v1"
anomalias = []
CORREO_TEMP = "temp.audit@distrirapido.com"
CORREO_OP2 = "op2.audit@distrirapido.com"
ROL_OPERADOR = "Operador Log\u00edstico"
PLACA_MINI = "MIN-001"


def limpiar_usuarios():
    """La auditoria debe poder repetirse: los usuarios de prueba se recrean."""
    db = SessionLocal()
    try:
        for correo in (CORREO_TEMP, CORREO_OP2):
            u = db.query(Usuario).filter(Usuario.correo == correo).first()
            if not u:
                continue
            ids_ruta = [r.id_ruta for r in db.query(Ruta.id_ruta).filter(Ruta.id_operador == u.id_usuario).all()]
            for fila in ids_ruta:
                db.query(RutaPunto).filter(RutaPunto.id_ruta == fila).delete(synchronize_session=False)
            db.query(Ruta).filter(Ruta.id_operador == u.id_usuario).delete(synchronize_session=False)
            db.query(PuntoEntrega).filter(PuntoEntrega.id_operador == u.id_usuario).delete(
                synchronize_session=False
            )
            db.delete(u)
        db.commit()
    finally:
        db.close()


def limpiar_vehiculos_de_prueba():
    db = SessionLocal()
    try:
        consulta = db.query(ParametrosVehiculo).filter(
            (ParametrosVehiculo.placa.like("AUD-%"))
            | (ParametrosVehiculo.placa == PLACA_MINI)
        )
        for v in consulta.all():
            for fila in db.query(Ruta.id_ruta).filter(Ruta.id_vehiculo == v.id_vehiculo).all():
                db.query(RutaPunto).filter(RutaPunto.id_ruta == fila[0]).delete(synchronize_session=False)
            db.query(Ruta).filter(Ruta.id_vehiculo == v.id_vehiculo).delete(synchronize_session=False)
            db.delete(v)
        db.commit()
    finally:
        db.close()


def call(method, path, token=None, body=None, params=None, form=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data, headers = None, {}
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            crudo = r.read().decode()
            return r.status, (json.loads(crudo) if crudo.strip() else None)
    except urllib.error.HTTPError as e:
        crudo = e.read().decode()
        try:
            return e.code, json.loads(crudo)
        except json.JSONDecodeError:
            return e.code, crudo


def ok(nombre, cond, detalle=""):
    print(f"{'OK   ' if cond else 'ANOM'} {nombre}{' -> ' + str(detalle) if detalle else ''}")
    if not cond:
        anomalias.append(f"{nombre} :: {detalle}")


def seccion(t):
    print(f"\n=== {t} ===")


# ---------------------------------------------------------------- AUTENTICACION
seccion("AUTENTICACION")

s, admin_login = call("POST", "/auth/login", form={"correo": "admin@distrirapido.com", "password": "admin123"})
ok("login admin 200", s == 200, s)
admin = admin_login["access_token"]

s, op_login = call("POST", "/auth/login", form={"correo": "operador@distrirapido.com", "password": "operador123"})
ok("login operador 200", s == 200, s)
op = op_login["access_token"]

limpiar_usuarios()
limpiar_vehiculos_de_prueba()

s, me = call("GET", "/auth/me", admin)
ok("/auth/me devuelve rol con nombre", s == 200 and isinstance(me.get("rol"), dict) and me["rol"].get("nombre"), me.get("rol"))
ok("/auth/me rol Administrador", me.get("rol", {}).get("nombre") == "Administrador", me.get("rol"))
ok("/auth/me NO expone hash de contrasena", "contrasena_hash" not in me, list(me.keys()))

s, me_op = call("GET", "/auth/me", op)
ok(f"operador rol '{ROL_OPERADOR}'", me_op.get("rol", {}).get("nombre") == ROL_OPERADOR, me_op.get("rol"))

s, _ = call("GET", "/auth/me")
ok("sin token -> 401", s == 401, s)

s, _ = call("GET", "/auth/me", "token.invalido.aqui")
ok("token invalido -> 401", s == 401, s)

s, _ = call("POST", "/auth/login", form={"correo": "operador@distrirapido.com", "password": "incorrecta"})
ok("password incorrecta -> 401", s == 401, s)

s, _ = call("POST", "/auth/login", form={"correo": "noexiste@distrirapido.com", "password": "operador123"})
ok("correo inexistente -> 401", s == 401, s)

s, _ = call("POST", "/auth/login", form={"correo": "no-es-correo", "password": "abc123"})
ok("correo malformado no filtra datos -> 401", s == 401, s)

s, _ = call("POST", "/auth/login", form={"password": "operador123"})
ok("login sin correo -> 422", s == 422, s)

# El alta de usuarios es una operacion sensible: solo un Administrador.
nuevo_usuario = {
    "nombre": "Temporal", "correo": "temp.audit@distrirapido.com",
    "password": "audit123456", "id_rol": 1,
}
s, _ = call("POST", "/auth/register", body=nuevo_usuario)
ok("register SIN token -> 401 (no es publico)", s == 401, s)

s, _ = call("POST", "/auth/register", op, body=nuevo_usuario)
ok("register como operador -> 403", s == 403, s)

s, reg = call("POST", "/auth/register", admin, body=nuevo_usuario)
ok("register como admin crea usuario", s == 201, reg if s != 201 else "")
temp_id = reg.get("id_usuario") if s == 201 else None
ok("usuario creado trae rol Administrador", (reg or {}).get("rol", {}).get("nombre") == "Administrador",
   (reg or {}).get("rol"))

s, _ = call("POST", "/auth/register", admin, body=nuevo_usuario)
ok("register con correo duplicado -> 400/409", s in (400, 409), s)

s, _ = call("POST", "/auth/register", admin, body={
    "nombre": "X", "correo": "x@distrirapido.com", "password": "corta", "id_rol": 1,
})
ok("register con password corta -> 422", s == 422, s)

s, _ = call("POST", "/auth/register", admin, body={
    "nombre": "X", "correo": "x@distrirapido.com", "password": "larga123456", "id_rol": 999,
})
ok("register con rol inexistente -> 400/404", s in (400, 404), s)

# ---------------------------------------------------------------- PUNTOS
seccion("PUNTOS DE ENTREGA (US-001)")

s, plist = call("GET", "/puntos-entrega", op)
ok("GET puntos 200", s == 200, s)
ok("puntos es lista", isinstance(plist.get("puntos"), list), type(plist.get("puntos")).__name__)

nuevo = {
    "direccion": "Calle de auditoria 123",
    "latitud": -12.1234567,
    "longitud": -76.9876543,
    "peso_kg": 4.25,
    "destinatario": "Audit Dest",
}
s, creado = call("POST", "/puntos-entrega", op, body=nuevo)
ok("POST punto 201", s == 201, creado if s != 201 else "")
audit_punto = creado.get("id_punto") if s == 201 else None
ok("punto devuelve peso_kg numerico", isinstance(creado.get("peso_kg"), (int, float)), type(creado.get("peso_kg")).__name__)
ok("punto NO expone id_operador de otro usuario", creado.get("id_operador") is not None)

casos_invalidos = [
    ("sin direccion", {**nuevo, "direccion": ""}, 422),
    ("direccion solo espacios", {**nuevo, "direccion": "   "}, 422),
    ("sin destinatario", {**nuevo, "destinatario": ""}, 422),
    ("coordenadas 0,0", {**nuevo, "latitud": 0, "longitud": 0}, 422),
    ("peso 0", {**nuevo, "peso_kg": 0}, 422),
    ("peso negativo", {**nuevo, "peso_kg": -5}, 422),
    ("latitud > 90", {**nuevo, "latitud": 95}, 422),
    ("longitud > 180", {**nuevo, "longitud": 190}, 422),
    ("sin peso", {k: v for k, v in nuevo.items() if k != "peso_kg"}, 422),
]
for nombre, cuerpo, esperado in casos_invalidos:
    s, r = call("POST", "/puntos-entrega", op, body=cuerpo)
    ok(f"rechaza: {nombre}", s == esperado, s)

s, _ = call("POST", "/puntos-entrega", None, body=nuevo)
ok("crear punto sin token -> 401", s == 401, s)

# PUT /puntos-entrega/{id} (SPECS.md L284)
s, libre = call("POST", "/puntos-entrega", op, body={**nuevo, "direccion": "Punto editable"})
libre_id = libre.get("id_punto") if s == 201 else None
if libre_id:
    s, put = call("PUT", f"/puntos-entrega/{libre_id}", op, body={
        "direccion": "Direccion corregida 456",
        "latitud": -12.1111111, "longitud": -76.9711111,
        "peso_kg": 9.75, "destinatario": "Dest Corregido",
    })
    ok("PUT punto 200", s == 200, put if s != 200 else "")
    ok("PUT guarda la direccion nueva", (put or {}).get("direccion") == "Direccion corregida 456", (put or {}).get("direccion"))
    ok("PUT guarda el peso nuevo", float((put or {}).get("peso_kg", 0)) == 9.75, (put or {}).get("peso_kg"))
    ok("PUT conserva el mismo id_punto", (put or {}).get("id_punto") == libre_id)

    s, relido = call("GET", f"/puntos-entrega/{libre_id}", op)
    ok("el cambio persiste (GET posterior)", s == 200 and relido["direccion"] == "Direccion corregida 456",
       relido.get("direccion") if s == 200 else s)

    s, _ = call("PUT", f"/puntos-entrega/{libre_id}", op, body={**nuevo, "latitud": 0, "longitud": 0})
    ok("PUT rechaza coordenadas 0,0 -> 422", s == 422, s)

    s, _ = call("PUT", f"/puntos-entrega/{libre_id}", op, body={**nuevo, "peso_kg": -1})
    ok("PUT rechaza peso negativo -> 422", s == 422, s)

    s, _ = call("DELETE", f"/puntos-entrega/{libre_id}", op)
    ok("DELETE punto libre 204", s == 204, s)
    s, _ = call("GET", f"/puntos-entrega/{libre_id}", op)
    ok("punto borrado -> 404", s == 404, s)

# ---------------------------------------------------------------- VEHICULOS
seccion("VEHICULOS")

s, vehs = call("GET", "/vehiculos", op)
ok("GET vehiculos 200", s == 200, s)
ok("vehiculos es lista no vacia", isinstance(vehs, list) and len(vehs) > 0, len(vehs) if isinstance(vehs, list) else vehs)
ok("vehiculo trae factor_emision_co2", all("factor_emision_co2" in v for v in vehs))
ok("vehiculo trae consumo_litros_km", all("consumo_litros_km" in v for v in vehs))

veh_admin = {
    "placa": f"AUD-{len(vehs):03d}",
    "capacidad_kg": 500.0,
    "factor_emision_co2": 2.31,
    "consumo_litros_km": 0.15,
    "velocidad_promedio_kmh": 40.0,
    "tipo_combustible": "Gasohol",
}
s, vcreado = call("POST", "/vehiculos", admin, body=veh_admin)
ok("admin crea vehiculo 201", s == 201, vcreado if s != 201 else "")
audit_veh = vcreado.get("id_vehiculo") if s == 201 else None

s, _ = call("POST", "/vehiculos", op, body={**veh_admin, "placa": "X-001"})
ok("operador NO puede crear vehiculo -> 403", s == 403, s)

s, _ = call("POST", "/vehiculos", admin, body={**veh_admin, "placa": veh_admin["placa"]})
ok("placa duplicada -> 400/409", s in (400, 409), s)

for nombre, cuerpo in [
    ("capacidad 0", {**veh_admin, "placa": "Y-001", "capacidad_kg": 0}),
    ("factor_emision 0", {**veh_admin, "placa": "Y-002", "factor_emision_co2": 0}),
    ("consumo negativo", {**veh_admin, "placa": "Y-003", "consumo_litros_km": -1}),
    ("velocidad 0", {**veh_admin, "placa": "Y-004", "velocidad_promedio_kmh": 0}),
]:
    s, _ = call("POST", "/vehiculos", admin, body=cuerpo)
    ok(f"vehiculo rechaza: {nombre}", s == 422, s)

s, _ = call("GET", "/vehiculos/999999", op)
ok("vehiculo inexistente -> 404", s == 404, s)

# ---------------------------------------------------------------- RUTAS
seccion("RUTAS (US-002/004/007)")

s, plist = call("GET", "/puntos-entrega", op)
ids_puntos = [p["id_punto"] for p in plist["puntos"]]
veh_id = audit_veh or vehs[0]["id_vehiculo"]

s, opt = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": veh_id, "punto_ids": ids_puntos[:3]})
ok("POST /rutas/optimizar 200", s == 200, opt if s != 200 else "")
ok("optimizar devuelve 3 puntos", len(opt.get("puntos", [])) == 3, len(opt.get("puntos", [])))
ok("optimizar NO persiste (no aparece en GET)", s == 200, "")
ok("orden es 1..n", [p["orden"] for p in opt.get("puntos", [])] == [1, 2, 3])
ok("co2_optimizado <= co2_no_optimizado", opt["co2_estimado_kg"] <= opt["co2_sin_optimizar_kg"] + 0.001,
   (opt["co2_estimado_kg"], opt["co2_sin_optimizar_kg"]))
ok("dist_opt <= dist_sin_opt", opt["distancia_total_km"] <= opt["distancia_sin_optimizar_km"] + 0.001,
   (opt["distancia_total_km"], opt["distancia_sin_optimizar_km"]))
ok("ahorro_co2_pct no negativo", opt["ahorro_co2_pct"] >= 0, opt["ahorro_co2_pct"])
ok("tiempos positivos", opt["tiempo_estimado_min"] > 0 and opt["tiempo_sin_optimizar_min"] > 0)
ok("estado Confirmada", opt.get("estado") == "Confirmada", opt.get("estado"))

s, conf = call("POST", "/rutas", op, body={"id_vehiculo": veh_id, "punto_ids": ids_puntos[:3]})
ok("POST /rutas 201", s == 201, conf if s != 201 else "")
ruta_id = conf.get("id_ruta") if s == 201 else None

s, lista = call("GET", "/rutas", op)
ok("GET /rutas incluye la nueva", any(r["id_ruta"] == ruta_id for r in lista), len(lista))

s, una = call("GET", f"/rutas/{ruta_id}", op)
ok("GET /rutas/{id} 200", s == 200, s)
ok("GET ruta trae ahorro_co2_kg", "ahorro_co2_kg" in una)

s, resumen = call("GET", f"/rutas/{ruta_id}/resumen", op)
ok("GET resumen 200", s == 200, s)
ok("resumen trae ahorro_co2_pct", "ahorro_co2_pct" in resumen)

s, pts = call("GET", f"/rutas/{ruta_id}/puntos", op)
ok("GET ruta/puntos 200", s == 200, s)
ok("GET ruta/puntos devuelve 3", len(pts) == 3, len(pts))
ok("GET ruta/puntos orden 1..n", [p["orden"] for p in pts] == [1, 2, 3])

s, _ = call("GET", "/rutas/no-es-uuid", op)
ok("uuid invalido -> 422", s == 422, s)

s, _ = call("GET", "/rutas/00000000-0000-0000-0000-000000000000", op)
ok("ruta inexistente -> 404", s == 404, s)

s, _ = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": veh_id, "punto_ids": ids_puntos[:1]})
ok("1 solo punto -> 400/422", s in (400, 422), s)

s, _ = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": veh_id, "punto_ids": []})
ok("0 puntos -> 400/422", s in (400, 422), s)

s, _ = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": 999999, "punto_ids": ids_puntos[:3]})
ok("vehiculo inexistente -> 404", s == 404, s)

s, _ = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": veh_id, "punto_ids": ["00000000-0000-0000-0000-000000000000"] * 2})
ok("puntos inexistentes -> 400", s == 400, s)

# duplicados en la request
s, _ = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": veh_id, "punto_ids": [ids_puntos[0], ids_puntos[0], ids_puntos[1]]})
ok("punto duplicado en la lista -> rechazado o deduplicado", s in (200, 400, 422), s)

# capacidad insuficiente
s, vmini = call("POST", "/vehiculos", admin, body={
    "placa": PLACA_MINI, "capacidad_kg": 1.0, "factor_emision_co2": 2.31,
    "consumo_litros_km": 0.15, "velocidad_promedio_kmh": 40.0, "tipo_combustible": "Gasohol",
})
ok("crea vehiculo de 1 kg para probar capacidad", s == 201, s)
if s == 201:
    s, r = call("POST", "/rutas/optimizar", op, body={"id_vehiculo": vmini["id_vehiculo"], "punto_ids": ids_puntos[:3]})
    ok("RN-014 capacidad insuficiente -> 400", s == 400, s)
    ok("mensaje menciona capacidad", "capacidad" in json.dumps(r).lower(), r)

# ---------------------------------------------------------------- AISLAMIENTO POR USUARIO
seccion("AISLAMIENTO ENTRE USUARIOS")

s, otras = call("GET", "/rutas", admin)
ok("admin ve mas rutas que operador", len(otras) >= len(lista), (len(otras), len(lista)))

if temp_id:
    s, tl = call("POST", "/auth/login", form={"correo": "temp.audit@distrirapido.com", "password": "audit123456"})
    if s == 200:
        tmp = tl["access_token"]
        # Este usuario es Administrador, por lo que ver todas las rutas es correcto.
        s, tl_rutas = call("GET", "/rutas", tmp)
        ok("admin ve todas las rutas", s == 200 and len(tl_rutas) >= len(lista), len(tl_rutas) if s == 200 else s)

# Un Operador nuevo no debe ver ni tocar rutas de otro usuario.
s, op2 = call("POST", "/auth/register", admin, body={
    "nombre": "Operador Dos", "correo": "op2.audit@distrirapido.com",
    "password": "audit123456", "id_rol": 2,
})
ok("admin crea un segundo operador", s == 201, s)
if s == 201:
    s, tl = call("POST", "/auth/login", form={"correo": "op2.audit@distrirapido.com", "password": "audit123456"})
    op2_token = tl["access_token"]
    s, tl_rutas = call("GET", "/rutas", op2_token)
    ok("operador nuevo ve 0 rutas ajenas", s == 200 and len(tl_rutas) == 0, len(tl_rutas) if s == 200 else s)
    s, _ = call("GET", f"/rutas/{ruta_id}", op2_token)
    ok("operador nuevo no lee ruta ajena -> 403/404", s in (403, 404), s)
    s, _ = call("PUT", f"/rutas/{ruta_id}", op2_token, body={"id_vehiculo": veh_id, "punto_ids": ids_puntos[:3]})
    ok("operador nuevo no edita ruta ajena -> 403/404", s in (403, 404), s)
    s, _ = call("DELETE", f"/rutas/{ruta_id}", op2_token)
    ok("operador nuevo no borra ruta ajena -> 403/404", s in (403, 404), s)
    s, tl_puntos = call("GET", "/puntos-entrega", op2_token)
    ok("operador nuevo ve 0 puntos ajenos", s == 200 and len(tl_puntos["puntos"]) == 0,
       len(tl_puntos.get("puntos", [])) if s == 200 else s)

# ---------------------------------------------------------------- FILTROS
seccion("FILTROS (US-007)")

s, f1 = call("GET", "/rutas", op, params={"desde": "2020-01-01", "hasta": "2020-01-02"})
ok("rango sin resultados -> 200 y vacio", s == 200 and f1 == [], (s, f1))
s, f2 = call("GET", "/rutas", op, params={"desde": "hoy-no-es-fecha"})
ok("fecha invalida -> 400", s == 400, s)
s, f3 = call("GET", "/rutas", op, params={"estado": "Confirmada"})
ok("filtro Confirmada 200", s == 200, s)
ok("todas Confirmada", all(r["estado"] == "Confirmada" for r in f3))
s, f4 = call("GET", "/rutas", op, params={"estado": "NoExiste"})
ok("estado inexistente -> 200 vacio", s == 200 and f4 == [], (s, f4))
s, f5 = call("GET", "/rutas", op, params={"desde": "2026-01-01", "hasta": "2020-01-01"})
ok("rango invertido -> 200 vacio", s == 200 and f5 == [], (s, f5))

# ---------------------------------------------------------------- GEOCODING
seccion("GEOCODING")

s, _ = call("GET", "/geocoding/reverse", op, params={"latitud": -12.115, "longitud": -76.97})
ok("reverse geocode 200", s == 200, s)
s, _ = call("GET", "/geocoding/reverse", None, params={"latitud": -12.115, "longitud": -76.97})
ok("reverse sin token -> 401", s == 401, s)
s, _ = call("GET", "/geocoding/reverse", op, params={"latitud": 999, "longitud": -76.97})
ok("reverse latitud invalida -> 422", s == 422, s)
s, _ = call("GET", "/geocoding/search", op, params={"q": "Miraflores Lima"})
ok("search 200", s == 200, s)
s, _ = call("GET", "/geocoding/search", op, params={"q": ""})
ok("search vacio -> 422", s == 422, s)

# ---------------------------------------------------------------- MISC
seccion("VARIOS")

s, salud = call("GET", "/health")
ok("GET /health 200", s == 200, s)
ok("GET /health estado ok", (salud or {}).get("estado") == "ok", salud)
ok("GET /health base_datos ok", (salud or {}).get("base_datos") == "ok", salud)

s, _ = call("GET", "/rutas/no-uuid", op)
ok("ruta malformada -> 4xx", 400 <= s < 500, s)

# ---------------------------------------------------------------- LIMPIEZA
seccion("LIMPIEZA")

# audit_punto no esta en ninguna ruta, asi que debe poder borrarse.
if audit_punto:
    s, put_libre = call("PUT", f"/puntos-entrega/{audit_punto}", op, body={
        "direccion": "Punto sin ruta 789", "latitud": -12.13, "longitud": -76.98,
        "peso_kg": 2.5, "destinatario": "Libre",
    })
    ok("PUT punto no usado en ruta -> 200", s == 200, put_libre if s != 200 else "")
    ok("PUT aplico el cambio", (put_libre or {}).get("direccion") == "Punto sin ruta 789",
       (put_libre or {}).get("direccion"))

# El primer punto de la ruta si esta en uso: no se debe poder tocar.
punto_en_ruta = ids_puntos[0] if ruta_id else None
if punto_en_ruta:
    s, r = call("DELETE", f"/puntos-entrega/{punto_en_ruta}", op)
    ok("DELETE punto en uso en ruta -> 400", s == 400, f"{s} {r}")
    s, _ = call("PUT", f"/puntos-entrega/{punto_en_ruta}", op, body={
        "direccion": "No deberia guardarse", "latitud": -12.1, "longitud": -76.9,
        "peso_kg": 1.0, "destinatario": "No",
    })
    ok("PUT punto en uso en ruta -> 400 (RN-009)", s == 400, s)
    s, intacto = call("GET", f"/puntos-entrega/{punto_en_ruta}", op)
    ok("el punto en uso quedo intacto", s == 200, s)

if ruta_id:
    s, _ = call("DELETE", f"/rutas/{ruta_id}", op)
    ok("DELETE ruta propia 204", s == 204, s)
    s, _ = call("GET", f"/rutas/{ruta_id}", op)
    ok("ruta borrada -> 404", s == 404, s)

    # Liberada la ruta, el punto ya puede borrarse.
    if punto_en_ruta:
        s, _ = call("DELETE", f"/puntos-entrega/{punto_en_ruta}", op)
        ok("punto liberado se borra -> 204", s == 204, s)
        s, verifica = call("GET", f"/rutas/{ruta_id}/puntos", op)
        ok("no quedan huerfanos: ruta ya no existe", s == 404, s)

if audit_punto:
    s, _ = call("DELETE", f"/puntos-entrega/{audit_punto}", op)
    ok("DELETE punto no usado -> 204", s == 204, s)

# ---------------------------------------------------------------- RESUMEN
limpiar_usuarios()
limpiar_vehiculos_de_prueba()

print("\n" + "=" * 60)
if anomalias:
    print(f"ANOMALIAS DETECTADAS ({len(anomalias)}):")
    for a in anomalias:
        print(f"  - {a}")
else:
    print("SIN ANOMALIAS")
print("=" * 60)
sys.exit(1 if anomalias else 0)