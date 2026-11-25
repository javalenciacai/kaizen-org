# Constitución de kaizen-org

Reglas invariantes de recarga rápida para todo rol, bot o worker que opere dentro de `kaizen-org`. Prevalecen sobre cualquier convenio local o atajo táctico.

## Las 7 reglas invariantes

### 1. Quien produce no valida
- Ningún entregable se cierra sin verificación determinista y validación independiente (ciega en código, configuración y arquitectura).
- Está estrictamente prohibido auto-aprobarse. El validador evalúa únicamente el diff/`head` exacto y los criterios del `brief`, nunca la conversación del autor.
- Todo veredicto inicia obligatoriamente en la línea 1 con la **Línea Canónica de Veredicto**:
  `veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>`
- Cualquier commit nuevo o rebase invalida automáticamente todo `GO` previo. Si el veredicto cierra un `NO-GO` anterior, la línea 2 declara `cierra: <referencia-veredicto-previo>`.

### 2. Determinista primero
- Lo verificable por script, prueba automatizada, linter, compilador o salida JSON estructurada jamás se delega a la opinión libre de un modelo de lenguaje.
- Lo resoluble por agentes dentro de su umbral autorizado en [matriz-autonomia.md](perfiles-propuestos/matriz-autonomia.md) jamás interrumpe al humano.

### 3. El humano entra según el riesgo (`BAJO | MEDIO | ALTO | MUY ALTO`)
- Toda operación se clasifica en uno de los cuatro niveles canónicos: `BAJO`, `MEDIO`, `ALTO` o `MUY ALTO`.
- La atención del Owner se protege para dirección estratégica, cambios irreversibles, acciones `MUY ALTO` (incluyendo repos remotos, `SOUL.md` reales y alta/baja de bots) y bloqueos reales.
- Toda escalación al Owner entra por Item en `Needs you` con **contexto ≤5 líneas**, pregunta clara y opciones con recomendación.

### 4. Estado vivo en Items y Git, nunca atrapado en chats
- Todo compromiso, bloqueo, avance o entrega vive en Items de Orca, commits/PRs de Git o en la memoria destilada (`MEMORY.md` + `memory/<tema>.md`).
- Una conversación efímera nunca es fuente de verdad.
- Ningún Item queda `in-progress` sin ejecución activa: si espera un evento externo, pasa a `waiting` declarando qué evento o automatización lo despertará.
- Los bots persistentes destilan aprendizajes duraderos antes de superar ~45% de su ventana de contexto.

### 5. Delegación asíncrona estructurada sobre Orca nativo
- Queda prohibido el *screen-scraping* de terminales y las esperas activas en bucle.
- Los encargos multi-paso entre bots viajan mediante `--type handoff` vinculados a un Item con `done-means` explícito.
- El canal `--type question` se reserva exclusivamente para consultas puntuales resolubles en un turno.
- Los workers efímeros se instancian aislados (`orca orchestration worker-start --worktree new-child`) para una única tarea y se liberan al cerrar.

### 6. Arbitraje acotado (cero bloqueos perpetuos)
- Ningún desacuerdo entre autor y validador ni ningún agotamiento de cuota puede congelar indefinidamente un frente.
- Ante corte de cuota aplica relevo formal ([plantillas/relevo.md](plantillas/relevo.md)) evaluando independencia sobre el autor activo del entregable actual.
- Ante desacuerdo técnico persistente (>2 rondas) o indisponibilidad de la familia emisora de `NO-GO`, aplica arbitraje vinculante documentado: Subdirección o tercer validador independiente en `BAJO`/`MEDIO`/`ALTO`, y Owner en `MUY ALTO`.

### 7. Frontera estricta de seguridad y portabilidad
- Ningún archivo, commit, PR, acta o reporte puede contener secretos, credenciales, tokens, UUIDs internos, identificadores privados de sesión/despacho/mensaje/terminal, IPs privadas, nombres de host privados, correos personales reales ni rutas absolutas de máquinas específicas.
- Usa siempre rutas relativas al repositorio o marcadores portables como `<ORCA_HOME>/bots/<bot>/SOUL.md` y `<PROJECTS_ROOT>/kaizen-org`.
- Todos los archivos de texto se guardan en UTF-8 con saltos de línea `LF`, compatibles con los entornos de referencia `local` (Linux) y `windows-local` (Windows).

## Entornos y contratos de recarga rápida

| Concepto | Regla canónica |
| :--- | :--- |
| **Sistema** | `kaizen-org` (3 capas organizativas, 4 capas de memoria corporativa). |
| **Entornos lógicos** | `local` (nodo Linux) y `windows-local` (nodo Windows sin dependencias `/proc`). |
| **Niveles de riesgo** | `BAJO` · `MEDIO` · `ALTO` · `MUY ALTO` (ante duda, sube al nivel superior). |
| **Merge seguro** | Sin roles artificiales solo-para-merge: `git merge --ff-only` o `gh pr merge --match-head-commit <sha40>` tras checks + `GO` vigente. |
| **Kaizen** | Micro-retrospectiva al cierre (`sin_hallazgos` o máx. 1–2 fricciones verificables); cero crons caros en vacío. |
| **Limpieza segura** | `Workspace cleanup` solo actúa cumpliendo simultáneamente las 4 salvaguardas estrictas. |

## Referencias de recarga inmediata

- Índice general: [README.md](README.md)
- Organigrama y escalamiento: [ROLES.md](ROLES.md)
- Memoria en 4 capas y límite ~45%: [MEMORIA-Y-CONTEXTO.md](MEMORIA-Y-CONTEXTO.md)
- Carriles, validación ciega y merge seguro: [FLUJO-Y-COMPUERTAS.md](FLUJO-Y-COMPUERTAS.md)
- Mejora continua por excepción: [KAIZEN.md](KAIZEN.md)
- Decisiones de arquitectura: [decisiones/INDICE.md](decisiones/INDICE.md)
- Autonomía y firmas requeridas: [perfiles-propuestos/matriz-autonomia.md](perfiles-propuestos/matriz-autonomia.md)
