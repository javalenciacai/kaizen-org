# Flujo de Trabajo y Compuertas de Calidad

Este documento regula cómo entra, se clasifica, se ejecuta, se valida, se integra y se desbloquea todo encargo en `kaizen-org`.

## 1. Clasificación de riesgo canónica

Todo encargo recibe un nivel de riesgo explícito antes de despacharse. Si un cambio eleva su impacto durante la ejecución, el nivel se promueve de inmediato.

| Nivel | Criterio y ejemplos concretos | Validación mínima | Autorización de cierre / integración |
| :--- | :--- | :--- | :--- |
| **`BAJO`** | Documentación interna, correcciones tipográficas, ajustes acotados en scripts/tests sin cambiar contratos ni datos. | Checks deterministas + 1 validación ciega independiente. | Subdirector responsable (conforme a Matriz de Autonomía). |
| **`MEDIO`** | Nueva funcionalidad acotada en 1 repo, refactor localizado, ajuste de plantillas/workflows o bugfix con impacto funcional controlado. | Checks deterministas + 1 validación ciega independiente sobre `head` exacto. | Subdirector responsable (Bloque B activo conforme a [MATRIZ-AUTONOMIA.md](MATRIZ-AUTONOMIA.md)). |
| **`ALTO`** | Cambios multi-repo, contratos públicos/API, seguridad, migraciones reversibles, automatizaciones críticas o cambios de gobernanza. | Checks deterministas + validación ciega reforzada (1 validador fuerte independiente + especialista `Pull request review`). | Subdirección + conocimiento de Dirección; escalamiento al Owner si hay excepción o disenso. |
| **`MUY ALTO`** | Operaciones destructivas o irreversibles, producción crítica, creación de repos remotos/visibilidad, cambios en `SOUL.md` reales, creación/retiro de bots permanentes, credenciales o infra crítica. | Checks deterministas + validación ciega reforzada + plan de reversión o contingencia explícito. | **Aprobación explícita obligatoria del Owner** (`Needs you`). |

---

## 2. Dos carriles de ejecución

### Carril A · Vía Ligera
- **Cuándo aplica:** riesgo `BAJO` o `MEDIO`, **1 solo repositorio**, sin cambios destructivos y sin ruptura de contratos externos.
- **Secuencia:**
  1. `Brief` directo ([plantillas/brief.md](plantillas/brief.md)) vinculado al Item con `done-means` verificable.
  2. Worker Autor en worktree hijo aislado (`orca orchestration worker-start --worktree new-child`).
  3. Checks deterministas locales (tests, lint, frontera de seguridad, `LF`) + commit limpio + [plantillas/acta-entrega.md](plantillas/acta-entrega.md).
  4. **1 Validación Ciega independiente** sobre el `head` exacto ([plantillas/veredicto.md](plantillas/veredicto.md)).
  5. Integración segura + cierre de Item con micro-retrospectiva Kaizen.

### Carril B · Vía Completa
- **Cuándo aplica:** iniciativas multi-repo, funcionalidades nuevas con superficie de usuario o API, cambios de arquitectura o riesgo `ALTO` / `MUY ALTO`.
- **Secuencia:**
  1. Definición previa de alcance, contratos (`ruta:línea@sha`) y criterios de prueba verificables.
  2. Descomposición en Items tácticos independientes (con dependencias explícitas en Orca).
  3. Desarrollo orientado a pruebas (TDD cuando aplica) en worktrees hijo aislados.
  4. Checks deterministas completos (suite de pruebas, análisis estático, compatibilidad `local` / `windows-local`, frontera de seguridad).
  5. **Validación Ciega reforzada:** 1 validador fuerte independiente + revisión de `Pull request review` en `ALTO`; y **aprobación explícita del Owner** en `MUY ALTO`.
  6. Integración segura sobre commit exacto + verificación post-entrega + cierre Kaizen.

---

## 3. Línea Canónica de Veredicto y Validación Ciega Real

### Línea Canónica de Veredicto (inviolable en línea 1)
Todo veredicto emitido por un validador o especialista inicia obligatoriamente en la **línea 1** con el formato exacto:

```text
veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>
```

Reglas asociadas:
- **Caducidad automática:** cualquier nuevo commit, amend o rebase cambia el `head` e **invalida automáticamente** todo `GO` anterior. No existe la aprobación *"por casi el mismo commit"*.
- **Cierre trazable de `NO-GO`:** cuando un veredicto subsana un `NO-GO` previo, debe incluir obligatoriamente en la **línea 2**:
  ```text
  cierra: <referencia-veredicto-previo>
  ```
- **Tipo de huella (`head`):** `sha40` para commits Git (regla general); `sha256:64hex` únicamente para artefactos inmutables fuera de Git.

### Principio de Validación Ciega Real
- El validador independiente recibe **únicamente**:
  1. El artefacto o `git diff` del `head` exacto a evaluar.
  2. Los criterios de aceptación y restricciones del `brief`.
  3. La salida reproducible de los checks deterministas (que puede y debe volver a ejecutar).
- **Nunca recibe** el historial de conversación del autor, sus excusas, sus notas de intención ni recomendaciones del coordinador sobre qué veredicto emitir.
- El validador debe pertenecer a una identidad/agente distinto al autor (y preferiblemente familia de modelo distinta cuando haya disponibilidad empírica).

---

## 4. Merge seguro sin roles artificiales

`kaizen-org` elimina el anti-patrón de crear workers efímeros cuyo único propósito sea ejecutar un merge.

Un entregable solo puede integrarse cuando se cumplen **simultáneamente** las 4 condiciones:
1. Checks deterministas en verde sobre el `head` exacto.
2. Veredicto canónico `GO` vigente emitido por un juez distinto al autor sobre ese mismo `head`.
3. Permiso vigente según [MATRIZ-AUTONOMIA.md](MATRIZ-AUTONOMIA.md) (incluyendo aprobación del Owner si es Bloque C / `MUY ALTO`).
4. Árbol destino limpio y verificación exacta del commit al integrar:
   - En integración local: `git merge --ff-only <sha40>` (o rebase/fast-forward verificado con re-validación si cambia el SHA).
   - En Pull Request remoto: `gh pr merge --match-head-commit <sha40>` (nunca mergear un PR sin fijar el SHA exacto auditado).

Cumplidas las 4 condiciones, el Subdirector responsable o el especialista habilitado ejecuta la integración directamente y registra el SHA final en el Item.

---

## 5. Disponibilidad empírica, relevo formal y arbitraje acotado

### Sondeo de disponibilidad empírica
Antes de asignar cargas pesadas o validaciones críticas, el coordinador verifica la disponibilidad real de herramientas, nodos (`local` / `windows-local`) y agentes/cuotas en lugar de asumir disponibilidad teórica.

### Relevo formal ante corte de cuota o interrupción
Si un worker o validador se queda sin cuota o es interrumpido:
1. Se preserva el progreso limpio en Git y se redacta [plantillas/relevo.md](plantillas/relevo.md) con el `sha40` exacto, lo verificado y lo pendiente.
2. El coordinador reasigna a otro agente disponible evaluando la independencia **únicamente respecto al autor activo del entregable actual**, evitando bloqueos matemáticos heredados de historiales antiguos.

### Arbitraje acotado (cero deadlocks)
Ningún frente puede quedar congelado por un empate técnico o por indisponibilidad de una familia de modelos:
1. **Desacuerdo técnico (>2 rondas autor ↔ validador):** tras 2 rondas de `NO-GO` sin convergencia, se detiene el ping-pong y se abre arbitraje acotado con evidencias concretas de ambas partes.
2. **Caída de cuota de la familia que emitió `NO-GO`:** una vez subsanados los hallazgos en un nuevo `head`, otro validador independiente disponible puede auditar y cerrar el `NO-GO` previo (`cierra: <referencia-veredicto-previo>`), sin esperar indefinidamente el retorno de la familia original.
3. **Resolución vinculante:**
   - En riesgo `BAJO`, `MEDIO` y `ALTO`: decide el Subdirector responsable o un tercer validador independiente designado por Subdirección, dejando justificación verificable en el Item.
   - En riesgo `MUY ALTO`: se escala al Owner vía `Needs you` (≤5 líneas de contexto, pregunta clara y opciones con recomendación).
