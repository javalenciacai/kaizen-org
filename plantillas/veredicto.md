veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>
cierra: <referencia-veredicto-previo-si-aplica-omitir-si-es-primera-ronda>

# Informe de Validación Ciega

- **Item:** `<referencia-del-item>`
- **Nivel de riesgo:** `BAJO` | `MEDIO` | `ALTO` | `MUY ALTO`
- **Rama evaluada:** `<nombre-rama>`
- **Entradas auditadas:** únicamente diff/`head` exacto + criterios del brief + checks deterministas reproducidos por el juez (cero conversación del autor).

## 1. Matriz de criterios del brief vs. evidencia comprobada

| # | Criterio del brief | Estado | Evidencia comprobada (`ruta:línea@sha` o comando) |
| :-: | :--- | :---: | :--- |
| 1 | `<criterio verificable 1>` | `CUMPLE` / `FALLA` | `<evidencia concreta>` |
| 2 | `<criterio verificable 2>` | `CUMPLE` / `FALLA` | `<evidencia concreta>` |
| 3 | Frontera de seguridad y formato `LF` | `CUMPLE` / `FALLA` | `<resultado del check ejecutado por el juez>` |

## 2. Hallazgos bloqueantes (obligatorio si `NO-GO`)

> Si el veredicto es `GO`, indicar `Ninguno.`

1. **[BLOQUEANTE-1]** `<descripción objetiva del incumplimiento>`
   - **Ubicación:** `<ruta:línea@sha>`
   - **Impacto:** `<riesgo o desviación respecto al brief/constitución>`
   - **Condición para cerrar:** `<qué cambio verificable se requiere para emitir GO>`

## 3. Observaciones menores (no bloqueantes)

- `<Observación opcional de claridad o mantenibilidad; nunca bloquea un GO por preferencia estilística.>`

## 4. Nota de caducidad

Este veredicto aplica **exclusivamente** al `head` declarado en la línea 1. Cualquier nuevo commit, amend o rebase invalida automáticamente un `GO` y exige re-validación independiente sobre el nuevo `head`.
