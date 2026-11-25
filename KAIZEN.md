# Kaizen: Mejora Continua por Excepción

En `kaizen-org`, la mejora continua no es un teatro burocrático ni una flota de crons caros corriendo en vacío. Es un mecanismo ligero, basado en **evidencia empírica**, activado **por excepción** y con **convergencia obligatoria** hacia mejoras concretas y medibles.

## Principios Kaizen de la organización

1. **Cero crons costosos en vacío:** no se ejecutan modelos caros en horarios fijos para *"buscar qué mejorar"* cuando no hay entregas ni fricciones reales.
2. **Evidencia antes que opinión:** toda fricción registrada debe citar un hecho verificable (Item, `head`, comando fallido, retrabajo `NO-GO` o bloqueo real).
3. **Convergencia obligatoria:** un diagnóstico no se repite indefinidamente; o se convierte en una acción acotada con criterio de verificación, o se descarta explícitamente por falta de impacto.
4. **Cambios mínimos de alto retorno:** priorizamos ajustes concretos en manuales, plantillas, scripts deterministas o propuestas de `SOUL.md` que eliminen causas raíz recurrentes.

---

## Paso 1 · Micro-retrospectiva al cierre de cada entrega real

Cada cierre de Item o entregable relevante (incluyendo [plantillas/acta-entrega.md](plantillas/acta-entrega.md)) incorpora obligatoriamente un bloque Kaizen breve usando [plantillas/kaizen-friccion.md](plantillas/kaizen-friccion.md):

- Si el flujo funcionó limpio y sin fricciones relevantes: registrar explícitamente **`sin_hallazgos`** (cero relleno artificial).
- Si hubo fricción real: registrar como máximo **1 a 2 fricciones verificables** indicando:
  1. **Hecho concreto:** qué ocurrió y referencia verificable (`Item`, `head`, log o veredicto).
  2. **Impacto:** tiempo perdido, retrabajo, bloqueo o riesgo introducido.
  3. **Propuesta puntual:** cambio mínimo sugerido (manual, plantilla, check determinista o tooling).

---

## Paso 2 · Telemetría determinista liviana

La observación de salud del sistema se obtiene con consultas estructuradas baratas sobre **JSON nativo de Orca + Git**, sin LLMs leyendo pantallas de terminal ni scripts de *screen-scraping*.

### Indicadores clave medidos de forma determinista

| Indicador | Fuente determinista | Qué señal detecta |
| :--- | :--- | :--- |
| **Tasa de retrabajo (`NO-GO`)** | Veredictos canónicos y conteo de rondas por Item | Briefs ambiguos, criterios incompletos o ausencia de check determinista previo. |
| **Bloqueos y escalaciones (`Needs you`)** | Transiciones de estado en Items de Orca | Vacíos en la Matriz de Autonomía o dependencias externas no declaradas. |
| **Relevos por cuota / interrupción** | Actas en `plantillas/relevo.md` y fallos de despacho | Cuellos de botella de cuota o mala estimación de tamaño de tarea. |
| **Salud multiplataforma (`local` / `windows-local`)** | Checks de `LF`, ausencia de dependencias `/proc`, estado de especialistas de infra | Regresiones de portabilidad antes de que bloqueen entregas reales. |
| **Higiene de worktrees y ramas** | Reportes por evento de `Workspace cleanup` | Acumulación de ramas huérfanas o fallos en las 4 salvaguardas de limpieza. |

---

## Paso 3 · Ciclo de Gobierno Kaizen por Señal Acumulada

El Ciclo de Gobierno Kaizen **no se dispara por calendario ciego**, sino únicamente cuando se cumple al menos un **disparador de señal real**:

- Se completa un lote de entregas reales cerradas con registros Kaizen acumulados (por defecto, cada **5 a 10 entregas** con al menos 1 fricción registrada).
- Una misma **causa raíz se repite ≥ 2 veces** en entregas distintas.
- Ocurre un **incidente bloqueante**, fallo de frontera de seguridad o escalación crítica.

### Ejecución del ciclo (Subdirección + Dirección)

1. **Deduplicación por causa raíz:** `bot:Subdirector 1` agrupa los registros de [plantillas/kaizen-friccion.md](plantillas/kaizen-friccion.md) y la telemetría liviana, descartando síntomas duplicados y ruido puntual.
2. **Selección estricta (máximo 1 a 3 mejoras):** Subdirección y `bot:Director General` aprueban únicamente **1 a 3 acciones concretas** de mayor retorno (PR al manual `kaizen-org`, mejora de plantilla, nuevo check determinista o propuesta de actualización de perfil en `perfiles-propuestos/`).
3. **Criterio explícito de verificación:** cada mejora aprobada define cómo se comprobará en las **3 entregas siguientes** que la fricción dejó de repetirse.
4. **Regla anti-bucle (convergencia obligatoria):** está prohibido re-emitir diagnósticos previos sin haber cerrado, medido o descartado formalmente la acción anterior asociada a esa misma causa raíz.
5. **Aprobación cuando toque gobernanza:** si una mejora implica modificar un `SOUL.md` real, crear/retirar un bot o cambiar permisos `MUY ALTO`, se presenta como propuesta al Owner vía `Needs you`.

---

## Reglas técnicas institucionalizadas (Micro-retrospectiva Fase 1 → v0.2)

Las siguientes reglas nacen de fricciones reales verificadas en el cierre de Fase 1 ([decisiones/0002-activacion-perfiles-bloque-b-y-fase2.md](decisiones/0002-activacion-perfiles-bloque-b-y-fase2.md)) y son de aplicación obligatoria en `local` y `windows-local`:

1. **Bootstrap Git compatible con Git <2.28:** inicializar repositorios nuevos con `git init && git symbolic-ref HEAD refs/heads/main` (en lugar de `git init -b main`) para garantizar compatibilidad en nodos con versiones antiguas de Git.
2. **Auditoría determinista de frontera sobre `git ls-files` + `git log`:** toda verificación automática de higiene (`UTF-8` + `LF`), integridad documental y frontera de publicación pública opera **exclusivamente** sobre `git ls-files` y `git log` —nunca recorriendo `.git` con `os.walk` ni dependiendo de `/proc` o módulos exclusivos de POSIX como `pwd`—. El verificador estándar de referencia es [scripts/check_kaizen.py](scripts/check_kaizen.py) (`python3 scripts/check_kaizen.py`).
