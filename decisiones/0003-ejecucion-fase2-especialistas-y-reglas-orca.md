# ADR 0003: Ejecución de Fase 2, activación de especialistas, reglas operativas de Orca y refuerzo de check_kaizen

- **ID:** 0003
- **Fecha:** 2026-11-25
- **Estado:** Aceptada
- **Autores / Promotores:** Owner · `bot:Director General` · `bot:Subdirector 1`

---

## 1. Contexto

Tras la publicación de `kaizen-org` `v0.2.0` y la ratificación del Bloque B de autonomía ([0002-activacion-perfiles-bloque-b-y-fase2.md](0002-activacion-perfiles-bloque-b-y-fase2.md)), se abordó la ejecución integral de la Fase 2 orientada a alinear e incorporar de manera formal los perfiles de los bots especialistas transversales en los entornos `local` y `windows-local`, apagar de manera reversible automatizaciones heredadas redundantes y resolver fricciones empíricas de orquestación y limpieza en Orca.

El Owner aprobó formalmente bajo Bloque C el `2026-11-25` el conjunto de decisiones operativas de Fase 2 para consolidar el release `v0.3.0`, garantizando que el sistema opere con alta autonomía sin comprometer la estabilidad de los hosts ni la frontera estricta de publicación pública en GitHub (`https://github.com/javalenciacai/kaizen-org`).

---

## 2. Decisiones ratificadas bajo Bloque C (`2026-11-25`)

Por aprobación explícita del Owner se ejecutan y ratifican las siguientes cuatro decisiones en `v0.3.0`:

1. **Activación de perfiles `SOUL.md` y alineación de skills locales en los 5 especialistas:**
   - Se ratifican y aplican los perfiles vigentes en `<ORCA_HOME>/bots/<bot>/SOUL.md` para los 5 bots especialistas de la organización:
     - `Infra VM-Oracle` (entorno lógico `local`).
     - `Workspace cleanup vm oracle` (entorno lógico `local`).
     - `Infra Local Windows` (entorno lógico `windows-local`).
     - `Pull request review` (auditoría ciega multi-repo en GitHub y Azure DevOps).
     - `Workspace cleanup` (entorno lógico `windows-local`).
   - Se alinean las skills locales de cada bot para restringir su operación al dominio de su especialidad bajo las directrices de [../ROLES.md](../ROLES.md) y [../MATRIZ-AUTONOMIA.md](../MATRIZ-AUTONOMIA.md).

2. **Estandarización de fin de línea en Windows (`core.autocrlf=input`):**
   - En el entorno lógico `windows-local`, se establece `git config --global core.autocrlf input`, garantizando que cualquier commit generado en Windows normalice sus saltos de línea a `LF` puro (`0` bytes `\r`) y respete `.gitattributes`, previniendo divergencias multiplataforma.

3. **Apagado reversible del Lote 1 de automatizaciones y migración de alertas a `Infra VM-Oracle`:**
   - Se apaga de forma controlada y reversible el Lote 1 de timers y scripts heredados que realizaban sondeos redundantes.
   - La monitorización y reporte de alertas de salud de host se centraliza en `Infra VM-Oracle` mediante diagnósticos nativos livianos y no destructivos, preservando intactos los servicios de infraestructura aún requeridos por proyectos coexistentes.

4. **Limpieza supervisada bajo las 4 salvaguardas y política explícita de `.atl/`:**
   - Se ejecuta una higiene supervisada de ramas y worktrees huérfanos verificando el cumplimiento estricto y simultáneo de las 4 salvaguardas operativas de [../ROLES.md](../ROLES.md).
   - Se institucionaliza la política formal para carpetas efímeras no versionadas `.atl/`.

---

## 3. Reglas operativas descubiertas empíricamente e institucionalizadas

Durante la ejecución de Fase 2 se identificaron dos restricciones arquitectónicas del runtime de Orca que quedan formalmente incorporadas en el Manual Corporativo:

1. **Frontera de mensajería en salas grupales y despacho de workers remotos (`--on <host>`):**
   - **Salas grupales:** Desde una sala grupal compartida (`C-Level`), Orca restringe la mensajería directa `orca orchestration send --to bot:<nombre>` exclusivamente a los bots miembros actuales de esa sala. Cuando `bot:Subdirector 1` requiera mensajear o coordinar directamente con especialistas permanentes fuera de `C-Level`, debe operar desde su Home Chat standalone o desde una sala operativa dedicada.
   - **Workers remotos:** Al instanciar workers efímeros en un nodo remoto mediante `orca orchestration worker-start --on <host>`, se debe omitir `--item <n>` (y `--environment`) en el comando de arranque para evitar rechazos de contexto; el enlace con el Item de Orca se realiza inmediatamente después en el nodo coordinador ejecutando `orca bot item link <n> dispatch:<id>`.

2. **Política de artefactos efímeros descartables (`.atl/`) en `Workspace cleanup`:**
   - Carpetas temporales no versionadas generadas por herramientas de inspección o sesión (`.atl/`) pueden ser descartadas durante una limpieza supervisada **únicamente** cuando se verifiquen de forma exhaustiva las condiciones de seguridad:
     - Rama integrada en su rama base/remoto con PR cerrado o mergeado.
     - `0` cambios locales pendientes fuera de `.atl/`.
     - `0` commits locales pendientes de push.
     - `0` procesos de agentes abiertos o `idle` en el worktree.
     - `0` Items activos (`in-progress`, `waiting`, `needs-you`) vinculados.
     - Verificación confirmada de que el worktree no corresponde a un checkout canónico de lectura de una automatización vigente.

---

## 4. Refuerzo determinista de `scripts/check_kaizen.py`

Para garantizar tolerancia cero en la frontera del repositorio público:

1. **Ampliación de patrones de handles internos de Orca:**
   - Se añade la detección del prefijo de workers estructurados al patrón `orca_internal_handle`, construido de forma segura mediante concatenación de fragmentos literales en el código para evitar auto-disparos o falsos positivos en el análisis estático.

2. **Auditoría profunda de parches históricos (`git log -p --full-history`):**
   - El escaneo de frontera pública se extiende más allá de los metadatos y mensajes de commit, auditando el diff completo de cada parche histórico en el repositorio (`git log -p --full-history`). De este modo, cualquier información confidencial introducida en un commit anterior y eliminada posteriormente sigue siendo detectada de forma determinista antes de su publicación remota.

3. **Pruebas unitarias en memoria:**
   - Se incorporan validaciones deterministas en memoria que comprueban la detección de muestras sintéticas (handles internos, rutas locales privadas, UUIDs y tokens) tanto en contenido de archivos como en texto de parches `git log -p`, sin generar archivos temporales ni tocar el disco.

---

## 5. Consecuencias y verificación

- **Inmediatas (`v0.3.0`):** Los 5 especialistas transversales operan alineados con sus perfiles vigentes en `local` y `windows-local`.
- **Higiene preventiva:** Las compuertas de [../scripts/check_kaizen.py](../scripts/check_kaizen.py) aseguran que ningún commit ni parche histórico contenga fugas de frontera ni regresiones de portabilidad.
- **Preparación para Fase 3:** La gobernanza queda estabilizada y validada para avanzar hacia proyectos de producto y coexistencia multi-agente.
