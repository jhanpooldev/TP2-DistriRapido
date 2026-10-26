"""Exportacion del resumen de una ruta (US-008).

El archivo se genera en el backend para que la descarga sea reproducible y
verificable con pruebas automatizadas. Se usa CSV porque es un formato abierto
que el operador puede abrir en Excel, Google Sheets o cualquier editor de texto.

Las celdas de texto se neutralizan contra inyeccion de formulas: Excel y otras
hojas de calculo interpretan como formula cualquier celda que empiece con
``=``, ``+``, ``-`` o ``@``. Un destinatario llamado ``=HYPERLINK(...)`` no debe
convertirse en una formula al abrir la exportacion.
"""
import csv
import io
from typing import Any

from app.schemas import ResumenRuta

# Prefijos que una hoja de calculo puede interpretar como inicio de formula.
_PREFIJOS_FORMULA = ("=", "+", "-", "@", "\t", "\r", "\n")


def celda_csv(valor: Any) -> Any:
    """Neutraliza los valores de texto peligrosos sin tocar los numeros.

    Las coordenadas negativas son datos legitimos y no deben recibir el
    apostrofo de proteccion; por eso solo se examinan las cadenas.
    """
    if not isinstance(valor, str):
        return valor

    if valor.startswith(_PREFIJOS_FORMULA) or valor.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + valor
    return valor


def _escribir_fila(writer: csv.writer, valores: list[Any]) -> None:
    writer.writerow([celda_csv(valor) for valor in valores])


def generar_csv_resumen(ruta, resumen: ResumenRuta) -> bytes:
    """Devuelve el CSV del resumen, codificado en UTF-8 con BOM.

    El BOM permite que Excel reconozca los acentos sin configuracion manual.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")

    _escribir_fila(writer, ["Resumen de ruta", str(resumen.id_ruta)])
    _escribir_fila(
        writer,
        ["Fecha de generacion", ruta.fecha_generacion.isoformat(sep=" ", timespec="seconds")],
    )
    _escribir_fila(writer, ["Estado", ruta.estado])

    _escribir_fila(writer, [])
    _escribir_fila(writer, ["Impacto estimado"])
    _escribir_fila(writer, ["Distancia optimizada (km)", resumen.distancia_total_km])
    _escribir_fila(writer, ["Tiempo estimado (min)", resumen.tiempo_estimado_min])
    _escribir_fila(writer, ["CO2 estimado (kg)", resumen.co2_estimado_kg])
    _escribir_fila(writer, ["Distancia sin optimizar (km)", resumen.distancia_sin_optimizar_km])
    _escribir_fila(writer, ["Tiempo sin optimizar (min)", resumen.tiempo_sin_optimizar_min])
    _escribir_fila(writer, ["CO2 sin optimizar (kg)", resumen.co2_sin_optimizar_kg])
    _escribir_fila(writer, ["Ahorro de CO2 (kg)", resumen.ahorro_co2_kg])
    _escribir_fila(writer, ["Ahorro de CO2 (%)", resumen.ahorro_co2_pct])
    _escribir_fila(writer, ["Ahorro de distancia (%)", resumen.ahorro_distancia_pct])
    _escribir_fila(
        writer,
        ["Reduccion significativa", "No" if resumen.sin_reduccion_significativa else "Si"],
    )

    _escribir_fila(writer, [])
    _escribir_fila(
        writer,
        ["Orden", "Destinatario", "Direccion", "Latitud", "Longitud", "Peso (kg)"],
    )
    for punto in sorted(resumen.puntos, key=lambda p: p.orden):
        _escribir_fila(
            writer,
            [
                punto.orden,
                punto.destinatario,
                punto.direccion,
                punto.latitud,
                punto.longitud,
                punto.peso_kg,
            ],
        )

    # utf-8-sig agrega el BOM que Excel necesita para respetar los acentos.
    return buffer.getvalue().encode("utf-8-sig")


def nombre_archivo_csv(ruta) -> str:
    """Nombre ASCII y predecible; no incorpora datos escritos por el usuario."""
    fecha = ruta.fecha_generacion.strftime("%Y%m%d")
    return f"ruta-{str(ruta.id_ruta)[:8]}-{fecha}.csv"
