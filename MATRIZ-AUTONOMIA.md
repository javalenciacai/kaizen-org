# Matriz de Autonomía de kaizen-org (v0.2)

> **Estado:** Vigente (Bloques A y B ACTIVOS; Bloque C bajo autorización explícita del Owner)
> **Fecha de ratificación:** `2026-11-25` (registrada en [decisiones/0002-activacion-perfiles-bloque-b-y-fase2.md](decisiones/0002-activacion-perfiles-bloque-b-y-fase2.md))

Esta matriz define con precisión qué ejecuta `kaizen-org` de forma autónoma (**Bloques A y B ACTIVOS** bajo compuertas deterministas y validación ciega estricta) y qué permanece **100% sujeto a aprobación explícita del Owner** mediante un Item en `Needs you` (**Bloque C**).

## Clasificación de permisos

- **(A) ACTIVO · Pre-aprobado por defecto:** operación segura dentro de los límites del repositorio/worktree y del organigrama; se ejecuta sin interrumpir al Owner.
- **(B) ACTIVO · Pre-aprobado con compuertas deterministas (ratificado el `2026-11-25`):** autorizado de forma autónoma únicamente cuando **todas** las compuertas deterministas, la frontera de seguridad y la validación ciega independiente están en verde sobre el `head` exacto (`sha40`).
- **(C) RESTRINGIDO · Requiere SIEMPRE autorización explícita del Owner (`Needs you`):** permanece 100% bajo aprobación explícita del Owner por evento con contexto ≤5 líneas, pregunta clara y opciones con recomendación; jamás es delegable por defecto.

---

## Tabla de autonomía por operación y nivel de riesgo

| Categoría | Operación concreta | Nivel de riesgo | Autoridad / Rol ejecutor | Compuertas obligatorias |
| :---: | :--- | :---: | :--- | :--- |
| **(A)** | Crear/actualizar Items tácticos en Orca, clasificar riesgo y delegar vía `--type handoff` / `--type question` | `BAJO` | `bot:Director General` / Subdirectores | `done-means` explícito; estado fiel (`in-progress` solo con ejecución activa) |
| **(A)** | Instanciar workers efímeros aislados (`worker-start --worktree new-child`) para investigar, codificar TDD, documentar o validar en ciego | `BAJO` | Subdirectores | Brief estructurado ([plantillas/brief.md](plantillas/brief.md)) + worktree hijo aislado |
| **(A)** | Ejecutar checks deterministas locales (tests, linters, formato `LF`, frontera de seguridad, telemetría JSON de Orca/Git) | `BAJO` | Workers / Especialistas | Sin efectos externos ni escritura fuera del worktree |
| **(A)** | Realizar commits locales en ramas de worktree hijo y redactar actas de entrega, veredictos y relevos | `BAJO` | Workers / Subdirectores | Frontera de seguridad en verde; `UTF-8` + `LF`; árbol limpio |
| **(A)** | Diagnóstico no destructivo de salud en `local` y `windows-local` (`Infra VM-Oracle`, `Infra Local Windows`) | `BAJO` | Especialistas de Infra | Solo lectura / sondeo empírico sin cambios de configuración persistente |
| **(A)** | Limpieza local orientada a eventos de ramas y worktrees cerrados (`Workspace cleanup`) | `BAJO` | `Workspace cleanup` | Cumplimiento determinista simultáneo de las **4 salvaguardas estrictas** ([ROLES.md](ROLES.md)) |
| **(A)** | Destilar memoria en `MEMORY.md` / `memory/<tema>.md` y registrar micro-retrospectivas Kaizen | `BAJO` | Bots persistentes | Cero secretos, cero estado efímero, cero instrucciones no autorizadas |
| **(A)** | Arbitraje acotado por desacuerdo (>2 rondas) o relevo por caída de cuota en riesgo `BAJO` / `MEDIO` / `ALTO` | `MEDIO` / `ALTO` | Subdirector / 3.er validador independiente | Justificación verificable en el Item; no elimina checks deterministas ni frontera |
| **(B)** | Integración/merge en rama principal **local** (o PR interno sin despliegue productivo) de cambios `BAJO` | `BAJO` | Subdirector / Especialista habilitado | Checks deterministas PASS + 1 `GO` canónico vigente sobre `head` exacto (`git merge --ff-only` o `--match-head-commit`) |
| **(B)** | Integración/merge en rama principal **local** (o PR interno sin despliegue productivo) de cambios `MEDIO` | `MEDIO` | Subdirector / Especialista habilitado | Checks deterministas PASS + 1 `GO` canónico vigente sobre `head` exacto + verificación de contratos |
| **(B)** | Apertura de Pull Requests (borrador o listos para revisión) en repositorios remotos **ya autorizados** por el Owner | `MEDIO` | Subdirector / Worker designado | Checks deterministas PASS + frontera de seguridad verificada (`0` secretos/UUIDs/rutas privadas) |
| **(B)** | Integración de cambios `ALTO` en ramas internas no productivas (p. ej. staging/desarrollo) tras validación ciega reforzada | `ALTO` | Subdirector con conocimiento de `bot:Director General` | Checks PASS + validador fuerte independiente + `GO` de `Pull request review` sobre `head` exacto + reversibilidad probada |
| **(C)** | Integración/merge de cambios `MUY ALTO` o despliegues en **producción crítica** / operaciones destructivas o irreversibles | `MUY ALTO` | Owner autoriza → Subdirector / Especialista ejecuta | Validación ciega reforzada + plan de reversión + **aprobación explícita en `Needs you`** |
| **(C)** | Crear repositorios remotos (p. ej. en GitHub), publicar código por primera vez o cambiar visibilidad (`private` ↔ `public`) | `MUY ALTO` | Owner autoriza → Ejecución tras firma | Auditoría completa de frontera de seguridad + **aprobación explícita en `Needs you`** |
| **(C)** | Editar archivos `SOUL.md` reales en `<ORCA_HOME>/bots/<bot>/SOUL.md` o modificar reglas de [CONSTITUCION.md](CONSTITUCION.md) con impacto de gobernanza | `MUY ALTO` | Owner autoriza | Propuesta versionada en `perfiles-propuestos/` validada + **aprobación explícita en `Needs you`** |
| **(C)** | Crear, dividir o retirar bots permanentes (nuevos Subdirectores o Especialistas) | `MUY ALTO` | Owner autoriza | Evidencia de gatillos objetivos ([ROLES.md](ROLES.md)) + **aprobación explícita en `Needs you`** |
| **(C)** | Cambios en infraestructura crítica, credenciales, tokens, permisos de red/Tailscale, secretos o configuración de host en `local` / `windows-local` | `MUY ALTO` | Owner autoriza | Plan de impacto y reversión + **aprobación explícita en `Needs you`** |
| **(C)** | Arbitraje final en desacuerdos de riesgo `MUY ALTO` o cualquier excepción que solicite relajar una compuerta obligatoria | `MUY ALTO` | Owner decide | Resumen ≤5 líneas + evidencias de ambas partes + recomendación en `Needs you` |

---

## Reglas de aplicación y salvaguardas

1. **Ante duda, se sube el nivel:** si una operación cae en zona gris entre dos categorías, se aplica siempre la categoría más restrictiva.
2. **Prohibida la elevación silenciosa:** ningún bot puede relajar compuertas obligatorias del bloque **(B)** ni otorgarse permisos del bloque **(C)** sin confirmación explícita registrada del Owner.
3. **Revocación inmediata:** el Owner puede promover cualquier operación de **(B)** a **(C)** en cualquier momento; el cambio se versiona en este archivo y se destila en el `MEMORY.md` de Dirección y Subdirección.
