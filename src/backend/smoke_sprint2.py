"""Smoke test de Sprint 2 contra la API en ejecucion (puerto 8001)."""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = f"http://127.0.0.1:{sys.argv[1] if len(sys.argv) > 1 else '8001'}/api/v1"
EMAIL = "operador@distrirapido.com"
PASSWORD = "operador123"

fallos = []


def check(nombre, condicion, detalle=""):
    print(f"{'OK   ' if condicion else 'FALLA'} {nombre}{' -> ' + str(detalle) if detalle else ''}")
    if not condicion:
        fallos.append(nombre)


def call(method, path, token=None, body=None, params=None, form=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = None
    headers = {}
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


status, datos = call("POST", "/auth/login", form={"correo": EMAIL, "password": PASSWORD})
if status != 200:
    print(f"FALLA login -> {status}: {datos}")
    sys.exit(1)
token = datos["access_token"]

# --- US-007: filtros -------------------------------------------------------
status, hoy = call("GET", "/rutas", token)
check("Listado de rutas responde 200", status == 200, status)
check("Listado devuelve lista", isinstance(hoy, list), len(hoy) if isinstance(hoy, list) else hoy)

status, vacio = call(
    "GET", "/rutas", token,
    params={"desde": "2020-01-01", "hasta": "2020-01-02"},
)
check("Rango sin coincidencias devuelve 200", status == 200, status)
check("Rango sin coincidencias devuelve lista vacia", vacio == [], vacio)

status, mal = call("GET", "/rutas", token, params={"desde": "ayer"})
check("Fecha invalida devuelve 400", status == 400, status)
check("Fecha invalida explica el formato", "YYYY-MM-DD" in json.dumps(mal), mal)

status, iso = call("GET", "/rutas", token, params={"desde": "2020-01-01T00:00:00"})
check("Filtro acepta ISO completo", status == 200, status)

status, por_estado = call("GET", "/rutas", token, params={"estado": "Confirmada"})
check("Filtro por estado responde 200", status == 200, status)
check(
    "Filtro por estado solo trae Confirmada",
    all(r["estado"] == "Confirmada" for r in por_estado),
)

# El smoke test se autoprovisiona: si el operador no tiene rutas, crea una con
# puntos propios. Depender de una ruta preexistente hacia el script irrepetible,
# porque al final borra la ruta que ejercita.
smoke_puntos = []
if not hoy:
    print("\nNo hay rutas guardadas: se crea una ruta propia para la prueba.")

    smoke_veh = None
    status, vehs = call("GET", "/vehiculos", token)
    if status == 200 and isinstance(vehs, list) and vehs:
        smoke_veh = vehs[0]["id_vehiculo"]

    for i, (lat, lng) in enumerate([(-12.0430, -77.0200), (-12.0600, -76.9900), (-12.0100, -77.0350)]):
        status, creado = call("POST", "/puntos-entrega", token, body={
            "direccion": f"Punto smoke base #{i+1}",
            "latitud": lat, "longitud": lng,
            "peso_kg": 2.5, "destinatario": "Smoke",
        })
        check(f"Crear punto base #{i+1}", status == 201, status)
        if status == 201:
            smoke_puntos.append(creado["id_punto"])

    if smoke_veh and len(smoke_puntos) >= 3:
        status, creada = call("POST", "/rutas", token, body={
            "id_vehiculo": smoke_veh, "punto_ids": smoke_puntos,
        })
        check("Crear ruta propia para la prueba", status == 201, creada if status != 201 else "")
        if status == 201:
            status, hoy = call("GET", "/rutas", token)
            check("Ruta propia aparece en el listado", status == 200 and len(hoy) > 0, len(hoy))

if not hoy:
    print("\nNo se pudo obtener una ruta; se omite la prueba de edicion/borrado.")
    sys.exit(1 if fallos else 0)

ruta = hoy[-1]
print(f"\nUsando ruta {ruta['id_ruta']}")

# --- US-004: indicadores ambientales ---------------------------------------
for campo in ("ahorro_co2_kg", "ahorro_co2_pct", "ahorro_distancia_pct", "sin_reduccion_significativa"):
    check(f"Campo {campo} presente", campo in ruta, ruta.get(campo))

check(
    "Ahorro nunca negativo",
    ruta["ahorro_co2_pct"] >= 0 and ruta["ahorro_co2_kg"] >= 0,
    (ruta["ahorro_co2_pct"], ruta["ahorro_co2_kg"]),
)
check(
    "Distancia optimizada <= sin optimizar",
    ruta["distancia_total_km"] <= ruta["distancia_sin_optimizar_km"] + 0.001,
    (ruta["distancia_total_km"], ruta["distancia_sin_optimizar_km"]),
)
check(
    "CO2 optimizado <= sin optimizar",
    ruta["co2_estimado_kg"] <= ruta["co2_sin_optimizar_kg"] + 0.001,
)

# El factor de emision pertenece al vehiculo (RN-017): se leen sus parametros
# reales en lugar de fijar un valor, de modo que la comprobacion valida la regla de
# negocio y no una constante del propio script.
status, veh_ruta = call("GET", f"/vehiculos/{ruta['id_vehiculo']}", token)
check("Se pudo leer el vehiculo de la ruta", status == 200, status)
if status == 200 and isinstance(veh_ruta, dict):
    factor = float(veh_ruta.get("factor_emision_co2", 0)) * float(veh_ruta.get("consumo_litros_km", 0))
    esperado = (ruta["distancia_sin_optimizar_km"] - ruta["distancia_total_km"]) * factor
    check(
        "kg CO2 usa el factor de emision del vehiculo",
        abs(ruta["ahorro_co2_kg"] - esperado) < 0.05,
        f"{ruta['ahorro_co2_kg']} vs {esperado:.3f} (factor {factor})",
    )
else:
    check("kg CO2 usa el factor de emision del vehiculo", False, "no se pudo leer el vehiculo")

status, resumen = call("GET", f"/rutas/{ruta['id_ruta']}/resumen", token)
check("Resumen incluye ahorro_co2_pct", status == 200 and "ahorro_co2_pct" in resumen, status)

# --- US-002: editar --------------------------------------------------------
# Se crean puntos nuevos para no chocar con RN-009 (los puntos existentes
# ya pertenecen a rutas guardadas).
nuevos = []
for i, (lat, lng) in enumerate([(-12.0430, -77.0200), (-12.0600, -76.9900), (-12.0100, -77.0350)]):
    status, creado = call("POST", "/puntos-entrega", token, body={
        "direccion": f"Punto smoke sprint2 #{i+1}",
        "latitud": lat,
        "longitud": lng,
        "peso_kg": 3.0,
        "destinatario": f"Smoke {i+1}",
    })
    check(f"Crear punto de prueba #{i+1}", status == 201, status)
    if status == 201:
        nuevos.append(creado)

if len(nuevos) >= 3:
    cuerpo = {"id_vehiculo": ruta["id_vehiculo"], "punto_ids": [p["id_punto"] for p in nuevos]}
    status, antes = call("GET", "/rutas", token)
    status, ed = call("PUT", f"/rutas/{ruta['id_ruta']}", token, body=cuerpo)
    check("PUT /rutas/{id} responde 200", status == 200, ed if status != 200 else "")

    if status == 200:
        status, despues = call("GET", "/rutas", token)
        check(
            "Editar NO crea una ruta nueva",
            len(despues) == len(antes),
            f"{len(antes)} -> {len(despues)}",
        )
        check("Mismo id_ruta tras editar", ed["id_ruta"] == ruta["id_ruta"])
        check("Puntos actualizados a 3", len(ed["puntos"]) == 3, len(ed["puntos"]))
        check(
            "Orden de entrega renumerado 1..n",
            [p["orden"] for p in ed["puntos"]] == [1, 2, 3],
            [p["orden"] for p in ed["puntos"]],
        )
        check("CO2 recalculado y positivo", ed["co2_estimado_kg"] > 0, ed["co2_estimado_kg"])
        check(
            "Baseline RN-018 recalculada en la edicion",
            ed["distancia_sin_optimizar_km"] > 0 and ed["co2_sin_optimizar_kg"] > 0,
        )
        check(
            "Orden optimizado <= orden de ingreso",
            ed["distancia_total_km"] <= ed["distancia_sin_optimizar_km"] + 0.001,
            (ed["distancia_total_km"], ed["distancia_sin_optimizar_km"]),
        )

        status, puntos_ruta = call("GET", f"/rutas/{ruta['id_ruta']}/puntos", token)
        check(
            "GET /puntos refleja la edicion",
            status == 200 and len(puntos_ruta) == 3,
            len(puntos_ruta) if status == 200 else status,
        )

    # Validacion: editar con un solo punto debe fallar
    status, mala = call("PUT", f"/rutas/{ruta['id_ruta']}", token, body={
        "id_vehiculo": ruta["id_vehiculo"],
        "punto_ids": [nuevos[0]["id_punto"]],
    })
    check("Editar con 1 punto se rechaza", status in (400, 422), status)

# --- RN-009: reusar punto de otra ruta -------------------------------------
status, todas = call("GET", "/rutas", token)
otras = [r for r in todas if r["id_ruta"] != ruta["id_ruta"] and r["puntos"]]
if otras and len(nuevos) >= 3:
    cuerpo = {
        "id_vehiculo": ruta["id_vehiculo"],
        "punto_ids": [otras[0]["puntos"][0]["id_punto"], nuevos[0]["id_punto"], nuevos[1]["id_punto"]],
    }
    status, r9 = call("PUT", f"/rutas/{ruta['id_ruta']}", token, body=cuerpo)
    check("RN-009 bloquea reasignar punto de otra ruta", status == 400, status)
else:
    print("AVISO  sin segunda ruta; RN-009 no verificado en ejecucion")

# --- US-002: eliminar ------------------------------------------------------
status, antes = call("GET", "/rutas", token)
status, cuerpo_del = call("DELETE", f"/rutas/{ruta['id_ruta']}", token)
check("DELETE responde 204", status == 204, status)
status, despues = call("GET", "/rutas", token)
check("Ruta eliminada del listado", len(despues) == len(antes) - 1, f"{len(antes)} -> {len(despues)}")
status, _ = call("GET", f"/rutas/{ruta['id_ruta']}", token)
check("Ruta eliminada ya no responde", status == 404, status)
status, puntos_ruta = call("GET", f"/rutas/{ruta['id_ruta']}/puntos", token)
check("No quedan puntos huerfanos", status == 404, status)

# --- Limpieza de los puntos creados por el smoke --------------------------
for p in nuevos:
    status, _ = call("DELETE", f"/puntos-entrega/{p['id_punto']}", token)
    check(f"Eliminar punto de prueba {p['id_punto'][:8]}", status == 204, status)

# Los puntos base solo se crean cuando no habia ninguna ruta; se liberan al borrar
# la ruta que los consumio, asi que ahora deben eliminarse.
for id_punto in smoke_puntos:
    status, _ = call("DELETE", f"/puntos-entrega/{id_punto}", token)
    check(f"Eliminar punto base {id_punto[:8]}", status == 204, status)

print("\n" + ("TODO OK" if not fallos else f"FALLOS ({len(fallos)}): {fallos}"))
sys.exit(1 if fallos else 0)