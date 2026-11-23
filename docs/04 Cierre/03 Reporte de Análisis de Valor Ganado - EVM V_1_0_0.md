[← Volver al README Principal](../../README.md)

# 03 Reporte de Análisis de Valor Ganado - EVM (Earned Value Analysis Report)

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Presupuesto hasta la Conclusión (BAC):** $9,978.08 (USD, estimado; costo de oportunidad)  
**Estado General:** cierre técnico parcial; sin Costo Real (AC) registrado  
**Versión:** 1.0.0

> **Base de cálculo verificable.** BAC = $9,978.08 según el
> [Presupuesto del proyecto](../02%20Planificación/04%20Presupuesto%20del%20proyecto%20V_1_0_0.md).
> Línea base = 49 Story Points. Valor unitario = $9,978.08 / 49 = **$203.634286 por SP**.
> PV se valora con los SP planificados acumulados y EV con los SP **cerrados**
> acumulados (16 + 16 + 4 = 36). Los 13 SP parciales (EN-02: 5, EN-03: 8) **no se
> acreditan como EV** porque no hay un porcentaje de avance real documentado para
> fraccionarlos. El Acta de Constitución registra además S/ 13,200.00 como referencial en
> soles; no se mezclan monedas. Serie de cierre:
> [01 Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md) ·
> [02 Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md) ·
> [03 EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) ·
> [04 Tableros](04%20Tableros%20de%20Control%20-%20Híbridos%20V_1_0_0.md) ·
> [05 Radiadores](05%20Radiadores%20de%20Información%20V_1_0_0.md) ·
> [06 Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md) ·
> [07 Lecciones](07%20Reporte%20Final%20de%20Lecciones%20Aprendidas%20V_1_0_0.md).

## 1. Métricas de Desempeño EVM

**Definición de columnas:** *Periodo actual* = Sprint 4 (09/11–17/11/2026); *Acumulado
periodo actual* = cierre del proyecto al 19/11/2026; *Acumulado periodo anterior* =
cierre al final del Sprint 3 (08/11/2026). El Sprint 4 no tenía SP planificados ni nuevos
SP cerrados: por eso PV y EV del periodo son $0.00 y su SPI es "no evaluable" (0/0).

| Métrica / Indicador | Periodo Actual | Acumulado Periodo Actual | Acumulado Periodo Anterior |
|:---|:---:|:---:|:---:|
| **Valor Planificado (PV)** | $0.00 | $9,978.08 | $9,978.08 |
| **Valor Ganado (EV)** | $0.00 | $7,330.83 | $7,330.83 |
| **Costo Real (AC)** | No disponible | No disponible | No disponible |
| **Variación del Cronograma (SV = EV - PV)** | $0.00 (sin SP en el periodo) | **-$2,647.25** | **-$2,647.25** |
| **Variación del Costo (CV = EV - AC)** | No evaluable (AC ausente) | No evaluable (AC ausente) | No evaluable (AC ausente) |
| **Índice de Desempeño del Cronograma (SPI = EV / PV)** | No evaluable (PV = 0) | **0.7347** | **0.7347** |
| **Índice de Desempeño del Costo (CPI = EV / AC)** | No evaluable (AC ausente) | No evaluable (AC ausente) | No evaluable (AC ausente) |

**Trazabilidad de PV y EV por sprint** (SP planificados / SP cerrados; montos en USD):

| Sprint | SP planificados | PV acumulado | SP cerrados | EV acumulado | SV acumulado | SPI acumulado |
|:---|:---:|---:|:---:|---:|---:|---:|
| 1 (05/10–18/10) | 21 | $4,276.32 | 16 | $3,258.15 | -$1,018.17 | 0.7619 |
| 2 (19/10–01/11) | 16 (37 acum.) | $7,534.47 | 16 (32 acum.) | $6,516.30 | -$1,018.17 | 0.8649 |
| 3 (02/11–08/11) | 12 (49 acum.) | $9,978.08 | 4 (36 acum.) | $7,330.83 | -$2,647.25 | 0.7347 |
| 4 (09/11–17/11) | 0 (49 acum.) | $9,978.08 | 0 (36 acum.) | $7,330.83 | -$2,647.25 | 0.7347 |

La SPI acumulada coincide con 36 / 49 = 0.734693… porque PV y EV se derivan del mismo
valor unitario. **No se divide entre cero en ningún cálculo**: cuando el denominador es
cero (PV del Sprint 4) o no existe (AC), el indicador se declara no evaluable.

## 2. Porcentajes de Avance Acumulado (Respecto al BAC)

- **Porcentaje Planificado (PV / BAC):** $9,978.08 / $9,978.08 = **100.00 %**.
- **Porcentaje Ganado (EV / BAC):** $7,330.83 / $9,978.08 = **73.47 %** (36 de 49 SP).
- **Porcentaje Gastado (AC / BAC):** **no disponible**. No existe AC real; no se reporta
  0 % porque eso afirmaría un desembolso nulo que no está registrado.

## 3. Análisis de Desviaciones

- **Causa raíz de la variación del cronograma:** de los 13 SP no cerrados, 5
  corresponden a EN-02 (JWT terminado, HTTPS pendiente del entorno) y 8 a EN-03 (CI
  implementada y ejecutada, pero sin host de Staging ni credenciales para desplegar).
  El Sprint 1 ya había arrastrado 5 SP parciales y el Sprint 3 añadió 8; el Sprint 4
  trabajó en calidad y documentación sin SP del backlog.
- **Impacto en el cronograma:** el valor no ganado asciende a **$2,647.25**, equivalente
  al **26.53 % del BAC**. La SPI de 0.7347 indica que por cada día de trabajo planificado
  se devengó, en promedio, 0.73 días de valor aceptado. El PMV funciona en local, pero
  H6 no se cerró en la fecha prevista y no hay aceptación formal.
- **Causa raíz de la variación del costo:** no determinable por ausencia total de
  registros de ejecución presupuestaria. La documentación aclara que los montos son
  costo de oportunidad académico, no desembolsos.
- **Impacto en el presupuesto:** desconocido. No es posible afirmar sobrecoste ni
  ahorro. La contingencia estimada de $1,069.08 no tiene registro de uso.

## 4. Estimaciones a la Conclusión (EAC)

Las tres fórmulas se escriben primero en forma simbólica y después se sustituye con los
datos disponibles. En los tres casos el resultado es **no evaluable** porque el
denominador depende de CPI = EV / AC y **AC no existe**. No se sustituye AC por cero, por
el presupuesto estimado ni por horas estimadas.

- **Fórmula 1 (EAC = BAC / CPI):** `EAC₁ = $9,978.08 / ($7,330.83 / AC)` → **no evaluable**.
  Requiere AC real.
- **Fórmula 2 (EAC = BAC / (CPI × SPI)):** `EAC₂ = $9,978.08 / [($7,330.83 / AC) × 0.7347]`
  → **no evaluable**. Requiere AC real; SPI sí está disponible (0.7347).
- **Fórmula 3 (EAC = AC + [(BAC - EV) / (CPI × SPI)]):**
  `EAC₃ = AC + [($9,978.08 − $7,330.83) / (($7,330.83 / AC) × 0.7347)]` → **no evaluable**.
  Requiere AC real.
- **EAC Seleccionado, Justificación y Explicación:** **no se selecciona ninguna
  fórmula**, porque seleccionar una sin AC produciría una cifra inventada y violaría la
  trazabilidad. Criterio diferido: una vez registrado AC real, si CPI y SPI se mantienen
  por debajo de 1, la **Fórmula 2** sería la candidata porque incorpora el desempeño de
  costos y de cronograma; la Fórmula 3 sería preferible si el desempeño observado no debe
  repetirse en el trabajo restante; la Fórmula 1 solo si el cronograma dejara de incidir.
  Este criterio es una regla de decisión, **no una estimación numérica**.

> **Datos que faltan para completar el EVM:** monto ejecutado real por sprint (AC),
> horas reales por integrante/rol y su tarifa efectiva, y —para acreditar los 13 SP
> parciales— porcentaje de avance verificado de EN-02 y EN-03. Hasta que existan, CV,
> CPI y las tres EAC permanecen como "no evaluable" en este documento y en el
> [Reporte de Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md).

---

[← Volver al README Principal](../../README.md)
