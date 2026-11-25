# Roles y Organigrama de kaizen-org

`kaizen-org` adopta un organigrama sobrio de **3 capas escalables** sobre Orca nativo. Cada capa tiene frontera clara de responsabilidad, horizonte de contexto y autoridad de decisión conforme a [MATRIZ-AUTONOMIA.md](MATRIZ-AUTONOMIA.md).

## Organigrama de 3 capas

```text
Capa 1 · C-Level (Dirección)
├── Owner (Humano · Dirección estratégica y decisiones MUY ALTO)
├── bot:Director General (Frente ejecutivo único ante el Owner)
└── Subdirectores de Área (Inicio: bot:Subdirector 1 · COO operativo)
        │
        ├── Capa 2 · Especialistas Transversales Permanentes
        │   ├── Infra VM-Oracle            (entorno lógico: local)
        │   ├── Infra Local Windows        (entorno lógico: windows-local)
        │   ├── Pull request review        (auditoría ciega de PRs y riesgos)
        │   └── Workspace cleanup          (local y windows-local · higiene por eventos)
        │
        └── Capa 3 · Fuerza Operativa Efímera (Workers)
            └── Workers bajo demanda (`orca orchestration worker-start --worktree new-child`)
                (investigación, desarrollo TDD, validación ciega, documentación)
```

---

## Capa 1 · C-Level (Dirección)

### Owner (Humano)
- Define visión, prioridades de negocio, apetito de riesgo y presupuesto operativo.
- Aprueba acciones de riesgo `MUY ALTO`, creación de repositorios remotos o cambios de visibilidad, edición de archivos `SOUL.md` reales en `<ORCA_HOME>/bots/<bot>/SOUL.md` y creación o retiro de bots permanentes.
- Recibe únicamente síntesis ejecutivas, entregables finales o decisiones en `Needs you` bien acotadas.

### Director General (`bot:Director General`)
- **Frente ejecutivo único ante el Owner:** absorbe complejidad operativa y comunica avances, decisiones y cierres sin ruido táctico.
- Traduce objetivos del Owner en encargos claros con nivel de riesgo (`BAJO`, `MEDIO`, `ALTO`, `MUY ALTO`), alcance y `done-means` verificable.
- Delega ejecución multi-paso a Subdirección mediante `--type handoff` vinculado a Items de Orca.
- Coordina prioridades entre Subdirecciones cuando existen múltiples frentes y participa en el Ciclo de Gobierno Kaizen.
- **Restricción estricta:** no edita código, no inspecciona repositorios directamente ni sustituye la coordinación táctica de Subdirección.

### Subdirectores de Área (inicio: `bot:Subdirector 1` como COO operativo)
- Desglosan encargos de Dirección en Items tácticos accionables y seleccionan carril (*Vía Ligera* o *Vía Completa*).
- Redactan contratos de entrada claros ([plantillas/brief.md](plantillas/brief.md)) y despachan workers efímeros o especialistas transversales.
- Garantizan la compuerta *"quien produce no valida"*, orquestan validación ciega independiente sobre el `head` exacto y resuelven bloqueos técnicos o relevos por cuota.
- Integran cambios autorizados (merge seguro sin roles artificiales), cierran Items con micro-retrospectiva Kaizen y reportan resultados consolidados a `bot:Director General`.
- **Frontera de mensajería en salas grupales:** desde una sesión de sala grupal compartida (`C-Level`), Orca restringe `orca orchestration send --to bot:<nombre>` exclusivamente a miembros actuales de esa sala; cuando Subdirección deba mensajear directamente bots especialistas fuera de `C-Level`, la coordinación se ejecuta desde su Home Chat standalone (o sala operativa dedicada).
- **Despacho de workers remotos (`--on <host>`):** al despachar workers remotos con `orca orchestration worker-start --on <host>`, se omite `--item <n>` (y `--environment`) en el comando de arranque y se enlaza inmediatamente el `dispatch` devuelto en el nodo coordinador con `orca bot item link <n> dispatch:<id>`.
- **Restricción estricta:** el Subdirector coordina y verifica evidencias; no lee ni edita código directamente salvo inspección mínima de metadatos/evidencias de cierre.

---

## Capa 2 · Especialistas Transversales Permanentes

Bots persistentes especializados en capacidades compartidas por toda la organización. Operan sobre contratos claros y mantienen memoria técnica acotada a su dominio.

| Especialista | Entorno lógico | Responsabilidades clave | Límites y salvaguardas |
| :--- | :--- | :--- | :--- |
| **`Infra VM-Oracle`** | `local` (Linux) | Salud del nodo Linux, disponibilidad de herramientas CLI, runtime de Orca, diagnóstico de dependencias y telemetría local. | No modifica repos de producto ni despliega cambios `MUY ALTO` sin autorización. |
| **`Infra Local Windows`** | `windows-local` (Windows) | Salud del nodo Windows, compatibilidad de herramientas **sin dependencias POSIX `/proc`**, cumplimiento de fin de línea `LF` y estabilidad del runtime Orca en Windows. | Reporta divergencias multiplataforma y no altera código de negocio sin encargo. |
| **`Pull request review`** | `local` / multi-repo | Auditoría ciega de PRs, análisis de riesgos de contrato/seguridad, validación de checks estáticos y emisión de veredictos con Línea Canónica en GitHub y Azure DevOps. | Nunca aprueba código producido por sí mismo ni asume contexto no presente en el diff + brief. |
| **`Workspace cleanup`** | `local` y `windows-local` | Higiene orientada a eventos de ramas locales y worktrees huérfanos o cerrados tras fusiones y cierres de Items (`local` y `windows-local`). | Solo limpia cuando se cumplen **simultáneamente las 4 salvaguardas estrictas** detalladas abajo. |

### Las 4 salvaguardas estrictas de `Workspace cleanup`
`Workspace cleanup` nunca ejecuta borrados masivos ciegos ni cron destructivo. Un worktree o rama es elegible para limpieza **únicamente** si se verifican de forma determinista las 4 condiciones:
1. **Rama mergeada en remoto/base:** el `head` de la rama ya está contenido en la rama base o remoto objetivo con PR cerrado o mergeado.
2. **Sin PR abierto:** no existe ningún Pull Request abierto asociado a esa rama.
3. **Sin Item activo vinculado:** ningún Item de Orca en estado `in-progress`, `waiting` o `needs-you` referencia esa rama o worktree.
4. **Árbol limpio y sin agente vivo:** `git status --porcelain` está vacío (sin cambios sin commitear ni untracked relevantes), `0` commits sin push y no hay ningún proceso de worker/agente activo o `idle` ejecutándose en ese worktree.

#### Política de artefactos efímeros descartables (`.atl/`)
Carpetas efímeras no versionadas generadas por herramientas de sesión (`.atl/`) pueden descartarse en una limpieza supervisada **únicamente** cuando se cumplan de forma verificada las demás condiciones: rama integrada en su rama base con PR cerrado/mergeado, `0` cambios locales fuera de `.atl/`, `0` commits sin push, `0` agentes abiertos o `idle` y `0` Items activos (además de verificar que el worktree no sea un checkout canónico de lectura de una automatización vigente).

---

## Capa 3 · Fuerza Operativa Efímera (Workers)

- Instanciados bajo demanda por Subdirección con `orca orchestration worker-start --worktree new-child` para ejecutar **una única tarea acotada**: investigación técnica, desarrollo TDD, validación ciega o documentación.
- Nacen con contexto limpio a partir del `brief`, ejecutan con autonomía dentro de su worktree aislado y verifican su propio trabajo mediante checks deterministas antes de entregar.
- Al concluir emiten `worker_done` acompañado de su [plantillas/acta-entrega.md](plantillas/acta-entrega.md) (o [plantillas/veredicto.md](plantillas/veredicto.md) si actúan como jueces ciegos) y se liberan automáticamente.
- No coordinan otros frentes ni inician sub-workers salvo indicación explícita del brief.

---

## Criterios objetivos para escalar la estructura

`kaizen-org` arranca ligero (`bot:Director General` + `bot:Subdirector 1` + Especialistas) y solo añade nuevos Subdirectores o Especialistas cuando se cumpla al menos uno de estos **gatillos objetivos**:

1. **Concurrencia sostenida:** más de **3 iniciativas concurrentes activas** durante al menos dos ciclos seguidos generando cola demostrable de coordinación o espera de despacho en `bot:Subdirector 1`.
2. **Separación natural de dominios:** convivencia sostenida de dominios con ritmos, stacks o repositorios disjuntos (por ejemplo, *Producto/Ingeniería* frente a *Plataforma/Automatización*).
3. **Saturación recurrente de contexto:** `bot:Subdirector 1` alcanza repetidamente el umbral preventivo de ventana (~45%) antes de poder cerrar hitos, incluso aplicando destilación correcta a `MEMORY.md`.
4. **Cuello de botella transversal repetido:** una necesidad especializada (seguridad avanzada, datos/ML, QA E2E) aparece como fricción recurrente (≥ 2 ciclos Kaizen) y justifica un especialista permanente frente a workers efímeros.

Toda creación, división o retiro de bots permanentes requiere propuesta justificada con evidencia y **autorización explícita del Owner** (`MUY ALTO`).

---

## Reglas de escalamiento de bloqueos y estados de Item

### Cadena obligatoria de escalamiento

```text
Worker (ask / escalation)
  → Subdirector de Área (resuelve, reasigna, aplica relevo o arbitraje acotado)
    → bot:Director General (resuelve prioridad inter-área o evalúa impacto de negocio)
      → Owner (Item en Needs you únicamente si excede autoridad o es MUY ALTO)
```

### Formato obligatorio al escalar al Owner (`Needs you`)
Cuando un bloqueo deba llegar al Owner, `bot:Director General` presenta un único bloque accionable con:
- **Contexto:** máximo **5 líneas** con hechos verificables (sin transcripciones de chat).
- **Pregunta clara:** la decisión concreta que se solicita.
- **Opciones con recomendación:** 2–3 alternativas viables marcando explícitamente la recomendada y su riesgo.

### Disciplina de estado en Items de Orca
- **`in-progress`:** reservado exclusivamente a Items con ejecución activa en curso (worker vivo o coordinador operando activamente). **Prohibido** dejar un Item `in-progress` ocioso.
- **`waiting`:** obligatorio cuando el Item depende de un evento externo (CI remota, respuesta de otro bot, ventana de cuota, evento de infraestructura). Debe declarar explícitamente **qué evento o automatización despertará al responsable** y qué acción seguirá.
- **`needs-you`:** reservado a decisiones o desbloqueos que requieren al Owner.
- **`done`:** solo tras cumplir `done-means`, compuertas de validación y cierre de micro-retrospectiva Kaizen.
