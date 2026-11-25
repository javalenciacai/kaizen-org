# ADR 0001: Fundación de kaizen-org sobre Orca nativo

- **ID:** 0001
- **Fecha:** 2026-11-24
- **Estado:** Aceptada
- **Autores / Promotores:** Owner · `bot:Director General` · `bot:Subdirector 1`

---

## 1. Contexto

El diagnóstico operativo de `ai-factory-method` v0.6.0 demostró un valor metodológico real en calidad y control de cambios, pero también expuso fricciones estructurales severas al trasladarse a una operación sostenida sobre Orca:

- **Exceso de capas y roles artificiales:** estructuras de 5 capas y agentes efímeros dedicados exclusivamente a ejecutar merges multiplicaban latencia, handoffs vacíos y consumo de contexto sin incrementar la seguridad real.
- **Fragilidad de infraestructura paralela:** dependencias en *screen-scraping* de terminales (`vigia_panes`) y servicios/daemons de memoria paralelos (`Engram`) introducían puntos de fallo externos, incompatibilidades multiplataforma (`windows-local`) y duplicación respecto a las primitivas nativas de Orca.
- **Bloqueos matemáticos y operativos (deadlocks ADR 0030/0041):** reglas rígidas sobre familias de modelos y cierres de `NO-GO` podían congelar un frente indefinidamente ante cortes de cuota o empates prolongados.
- **Desperdicio por mejora continua en vacío:** crons horarios ejecutando modelos costosos sin entregas nuevas ni señal real generaban gasto y diagnósticos repetitivos sin convergencia.

Se requiere fundar una organización multi-agente propia, limpia y nativa sobre Orca, capaz de operar de forma confiable en `local` (Linux) y `windows-local` (Windows).

---

## 2. Decisiones adoptadas

Por decisión del Owner, se funda **`kaizen-org`** bajo los siguientes pilares:

1. **Identidad oficial:** el sistema organizativo se denomina `kaizen-org`, versionado en su propio repositorio (`<PROJECTS_ROOT>/kaizen-org`) como fuente normativa (Capa 1).
2. **Organigrama inicial de 3 capas escalables sobre Orca nativo:**
   - **Capa 1 · C-Level:** Owner, `bot:Director General` (frente ejecutivo único) y Subdirectores de Área (arrancando con `bot:Subdirector 1` como COO operativo).
   - **Capa 2 · Especialistas Transversales Permanentes:** `Infra VM-Oracle` (`local`), `Infra Local Windows` (`windows-local`), `Pull request review` y `Workspace cleanup` (`local` y `windows-local` con 4 salvaguardas estrictas).
   - **Capa 3 · Fuerza Operativa Efímera:** workers bajo demanda con `orca orchestration worker-start --worktree new-child`.
3. **Orquestación 100% nativa sobre Orca:** estado vivo en Items de Orca + Git/PRs, delegación multi-paso mediante `--type handoff` vinculado a Items con `done-means`, y memoria destilada por rol en `MEMORY.md` + `memory/<tema>.md` con higiene preventiva al ~45% de ventana.

---

## 3. Qué heredamos como oro metodológico

Conservamos y endurecemos las prácticas de alto valor demostradas empíricamente:

1. **Validación ciega independiente ("quien produce no valida"):** el validador evalúa únicamente el diff/`head` exacto y los criterios del `brief`, nunca la conversación del autor.
2. **Línea Canónica de Veredicto + SHA exacto:** formato invariable en línea 1 (`veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>`), con caducidad automática ante cualquier nuevo commit o rebase y trazabilidad de cierre (`cierra: ...`).
3. **Vía Ligera explícita:** carril ágil para cambios `BAJO`/`MEDIO` en un solo repositorio sin sacrificar checks deterministas ni validación independiente.
4. **Determinista primero:** todo lo verificable por scripts, tests, linters o JSON estructurado se ejecuta antes y por encima de opiniones libres de un LLM.
5. **Frontera estricta de seguridad y portabilidad:** tolerancia cero a secretos, tokens, UUIDs internos, identificadores privados de sesión o rutas locales absolutas; UTF-8 y `LF` obligatorio en ambos entornos (`local` y `windows-local`).

---

## 4. Qué descartamos de raíz

Quedan explícitamente prohibidos o eliminados en `kaizen-org`:

1. **Jerarquías de 5 capas:** sustituidas por 3 capas escalables con gatillos objetivos para abrir nuevas Subdirecciones.
2. **Agentes efímeros solo-para-merge:** sustituidos por merge seguro directo del coordinador o especialista habilitado verificando el commit exacto (`git merge --ff-only` o `gh pr merge --match-head-commit <sha40>`).
3. **Scraping de PTY (`vigia_panes`) y esperas activas:** sustituidos por Items de Orca, señales asíncronas nativas (`handoff`, `worker_done`, `ask`, `escalation`) y consultas JSON estructuradas.
4. **`Engram` y daemons externos frágiles de memoria:** sustituidos por el protocolo de 4 capas nativo (Manual en Git, Items + Git, Contratos de traspaso y `MEMORY.md` destilado).
5. **Deadlocks heredados (ADR 0030 / ADR 0041):** sustituidos por disponibilidad empírica, relevo formal ([plantillas/relevo.md](../plantillas/relevo.md)) y arbitraje acotado que impide bloqueos perpetuos ante cortes de cuota o desacuerdos >2 rondas.
6. **Crons horarios con modelos caros corriendo en vacío:** sustituidos por micro-retrospectivas al cierre de cada entrega real, telemetría liviana y Ciclo de Gobierno Kaizen activado únicamente por señal acumulada.

---

## 5. Implicaciones por fases

### Fase 1 · Fundación y validación documental (v0.1 — actual)
- Crear la documentación fundacional completa (`README.md`, `CONSTITUCION.md`, `ROLES.md`, `MEMORIA-Y-CONTEXTO.md`, `FLUJO-Y-COMPUERTAS.md`, `KAIZEN.md`), las 5 plantillas operativas, `decisiones/` con esta ADR 0001 y las propuestas en `perfiles-propuestos/`.
- Validar el entregable con verificación determinista estricta y **Validación Ciega Independiente** antes de integrar en la rama principal local.
- Someter a revisión del Owner las propuestas en `perfiles-propuestos/` (`director-general-SOUL.md`, `subdirector-1-SOUL.md` y `matriz-autonomia.md`) y la eventual publicación remota del repositorio.

### Fase 2 · Activación operativa y pruebas piloto
- Aplicar los `SOUL.md` aprobados por el Owner en `<ORCA_HOME>/bots/<bot>/SOUL.md` y confirmar la Matriz de Autonomía vigente.
- Ejecutar entregas piloto en *Vía Ligera* y *Vía Completa* cubriendo tanto `local` como `windows-local`, verificando delegación por `handoff`, validación ciega real y las 4 salvaguardas de `Workspace cleanup`.
- Instrumentar scripts deterministas livianos de verificación de frontera, enlaces y telemetría sobre JSON de Orca + Git.

### Fase 3 · Escalamiento controlado y gobierno Kaizen
- Evaluar el primer Ciclo de Gobierno Kaizen únicamente al acumular señal real del piloto, aplicando 1–3 mejoras verificables sobre manuales, plantillas o checks.
- Mantener la estructura ligera hasta que se disparen los gatillos objetivos de escalamiento definidos en [ROLES.md](../ROLES.md) para nuevas Subdirecciones o Especialistas.
