# Brief: <Título corto y accionable del encargo>

- **Item:** `<referencia-del-item-en-orca>`
- **Repositorio / Rama base:** `<nombre-repo>` · `<rama-base>` (`<sha40-base>`)
- **Nivel de riesgo:** `BAJO` | `MEDIO` | `ALTO` | `MUY ALTO`
- **Carril:** `Vía Ligera` | `Vía Completa`
- **Responsable de coordinación:** `bot:Subdirector 1` (u otro Subdirector de Área)
- **Rol asignado:** `Worker Autor` | `Worker Investigación` | `Worker Validador Ciego` | `<Especialista>`

## 1. Contexto mínimo

<2 a 5 líneas con el problema o necesidad real y el objetivo del encargo. Sin transcripciones de chat ni contexto irrelevante.>

## 2. Alcance

### Dentro de alcance
- <Entregable o cambio verificable 1>
- <Entregable o cambio verificable 2>

### Fuera de alcance
- <Qué NO debe modificarse ni investigarse en este encargo>

## 3. Referencias verificables (`ruta:línea@sha`)

- `<ruta/relativa/al/archivo.ext>:L10-L45@<sha40>` — <motivo de la referencia>
- `<ruta/relativa/al/contrato.md>:L1-L60@<sha40>` — <criterio o especificación aplicable>

## 4. Restricciones inviolables

- Operar exclusivamente dentro del worktree hijo asignado (`--worktree new-child`).
- Sin operaciones remotas destructivas ni cambios en `SOUL.md` reales del sistema.
- Frontera estricta de seguridad: cero secretos, credenciales, tokens, UUIDs internos, identificadores privados de sesión/despacho ni rutas absolutas privadas de máquina (usar rutas relativas o marcadores como `<ORCA_HOME>` y `<PROJECTS_ROOT>`).
- Higiene multiplataforma: UTF-8 con saltos de línea `LF` y compatibilidad con `local` y `windows-local`.
- <Restricciones adicionales específicas del encargo>

## 5. Evidencias deterministas exigidas

- [ ] Suite de pruebas / verificación determinista: `<comando exacto>` (exit code `0`)
- [ ] Linter / validación estática / formato `LF`: `<comando exacto>` (exit code `0`)
- [ ] Chequeo de frontera de seguridad y enlaces relativos: `<comando exacto>` (exit code `0`)
- [ ] Árbol limpio tras commit: `git status --porcelain` vacío y `git rev-parse HEAD` (`sha40`)

## 6. Criterio de cierre (`done-means`)

El encargo se considera completo únicamente cuando:
1. Todos los entregables dentro de alcance están comprometidos en un commit limpio en la rama del worktree.
2. Todas las evidencias deterministas pasan sin errores.
3. Se entrega el cierre estructurado usando [plantillas/acta-entrega.md](acta-entrega.md) con micro-retrospectiva Kaizen y se notifica `worker_done` (o se emite [plantillas/veredicto.md](veredicto.md) si es validación ciega).

Placement: local | windows-local — <motivo del entorno asignado>
