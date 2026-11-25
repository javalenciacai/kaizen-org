# kaizen-org

Sistema organizativo multi-agente nativo sobre **Orca**, diseñado para operar como una empresa real de múltiples cerebros: combina rigor determinista, continuidad de contexto sin saturación y mejora continua por excepción mientras produce resultados reales.

## Visión ejecutiva

`kaizen-org` resuelve los tres modos de fallo típicos de las operaciones multi-agente:

1. **Pérdida de contexto y ruido operativo:** separa el manual corporativo, el estado vivo, los contratos de traspaso y la memoria destilada para que cada rol lea solo lo que necesita para ejecutar bien.
2. **Auto-validación y bloqueos burocráticos:** exige verificación determinista primero y validación ciega independiente sobre el commit exacto (`head`), eliminando roles artificiales y bloqueos perpetuos mediante relevo formal y arbitraje acotado.
3. **Burocracia costosa sin impacto:** sustituye procesos en vacío por micro-retrospectivas al cierre de cada entrega real, telemetría estructurada liviana y ciclos de mejora activados únicamente por señal acumulada.

El sistema opera de forma homogénea en los entornos lógicos de referencia **`local`** (nodo Linux) y **`windows-local`** (nodo Windows), con higiene multiplataforma estricta (`UTF-8` + `LF`) y frontera de seguridad inviolable.

## Resumen arquitectónico

### 1. Organización en 3 capas escalables

| Capa | Integrantes | Responsabilidad principal |
| :--- | :--- | :--- |
| **Capa 1 · C-Level (Dirección)** | Owner, `bot:Director General`, Subdirectores de Área (inicio: `bot:Subdirector 1`) | Visión, apetito de riesgo, conversión de metas en encargos con `done-means`, coordinación operativa y síntesis ejecutiva. |
| **Capa 2 · Especialistas Transversales** | `Infra VM-Oracle`, `Infra Local Windows`, `Pull request review`, `Workspace cleanup` (`local` y `windows-local`) | Operación continua de infraestructura, auditoría independiente de PRs e higiene segura de ramas y worktrees orientada a eventos. |
| **Capa 3 · Fuerza Operativa Efímera** | Workers bajo demanda (`orca orchestration worker-start --worktree new-child`) | Ejecución aislada de una sola tarea acotada (investigación, desarrollo TDD, validación ciega, documentación) y cierre limpio. |

### 2. Memoria corporativa en 4 capas

| Capa | Fuente de verdad | Qué preserva |
| :--- | :--- | :--- |
| **Capa 1 · Manual Corporativo** | Repositorio `kaizen-org` y documentación de cada proyecto | Constitución, roles, compuertas, plantillas y ADRs (`decisiones/`). |
| **Capa 2 · Estado Vivo Operativo** | Items de Orca + Git / PRs | Responsable actual, estado (`in-progress`, `waiting`, `needs-you`, `done`), ramas, SHAs y resultados de CI. |
| **Capa 3 · Contratos de Traspaso** | `Brief`, `Acta de entrega` y `Acta de relevo` | Alcance explícito, referencias verificables `ruta:línea@sha` y evidencias reproducibles sin arrastrar historiales de chat. |
| **Capa 4 · Memoria Destilada** | `MEMORY.md` y `memory/<tema>.md` por bot persistente | Hechos duraderos, decisiones estables y procedimientos verificados; destilados antes de superar ~45% de contexto. |

### 3. Flujo por nivel de riesgo y bucle Kaizen

| Nivel de riesgo | Carril habitual | Compuerta mínima antes de integrar | Intervención del Owner |
| :--- | :--- | :--- | :--- |
| `BAJO` | Vía Ligera | Checks deterministas + 1 validación ciega (`GO` vigente) | Excepción o informe de cierre |
| `MEDIO` | Vía Ligera o Completa | Checks deterministas + 1 validación ciega (`GO` vigente) | Excepción o confirmación según Matriz |
| `ALTO` | Vía Completa | Checks deterministas + validación ciega reforzada (validador fuerte + especialista PR) | Excepción, arbitraje si aplica o aviso |
| `MUY ALTO` | Vía Completa | Checks deterministas + validación ciega reforzada + aprobación explícita | **Obligatoria** (`Needs you`) |

Cada entrega cerrada alimenta el bucle **Kaizen por excepción**: micro-retrospectiva al cierre → telemetría determinista (JSON de Orca + Git) → ciclo de gobierno únicamente cuando existe señal acumulada o causa raíz repetida.

## Índice navegable del repositorio

### Documentación fundacional

- [CONSTITUCION.md](CONSTITUCION.md) — Las 7 reglas invariantes de recarga rápida (<1 página).
- [ROLES.md](ROLES.md) — Organigrama de 3 capas, criterios de escalamiento de estructura y cadena de bloqueos.
- [MEMORIA-Y-CONTEXTO.md](MEMORIA-Y-CONTEXTO.md) — Protocolo de memoria en 4 capas e higiene preventiva de ventana (~45%).
- [FLUJO-Y-COMPUERTAS.md](FLUJO-Y-COMPUERTAS.md) — Niveles de riesgo, Vía Ligera/Completa, Línea Canónica de Veredicto, validación ciega, merge seguro, relevo y arbitraje acotado.
- [KAIZEN.md](KAIZEN.md) — Mejora continua por excepción, micro-retrospectivas, telemetría liviana y convergencia obligatoria.

### Plantillas operativas (`plantillas/`)

- [plantillas/brief.md](plantillas/brief.md) — Contrato de encargo estructurado con riesgo, carril y `done-means`.
- [plantillas/acta-entrega.md](plantillas/acta-entrega.md) — Reporte de cierre con `head`, evidencias deterministas y micro-retrospectiva Kaizen.
- [plantillas/veredicto.md](plantillas/veredicto.md) — Informe de validación ciega encabezado por la Línea Canónica de Veredicto.
- [plantillas/relevo.md](plantillas/relevo.md) — Traspaso limpio ante corte de cuota o interrupción sin pérdida de estado.
- [plantillas/kaizen-friccion.md](plantillas/kaizen-friccion.md) — Registro conciso de `sin_hallazgos` o hasta 2 fricciones verificables.

### Decisiones de arquitectura (`decisiones/`)

- [decisiones/INDICE.md](decisiones/INDICE.md) — Tabla índice de registros de decisión (ADRs).
- [decisiones/0001-fundacion-kaizen-org.md](decisiones/0001-fundacion-kaizen-org.md) — ADR 0001: Fundación de `kaizen-org`, herencia metodológica y descartes de raíz.

### Perfiles propuestos y gobernanza (`perfiles-propuestos/`)

> Los documentos en `perfiles-propuestos/` son propuestas versionadas para revisión y autorización del Owner; ningún agente modifica archivos `SOUL.md` reales en `<ORCA_HOME>/bots/<bot>/SOUL.md` sin aprobación explícita.

- [perfiles-propuestos/director-general-SOUL.md](perfiles-propuestos/director-general-SOUL.md) — Propuesta de perfil `SOUL.md` para `bot:Director General`.
- [perfiles-propuestos/subdirector-1-SOUL.md](perfiles-propuestos/subdirector-1-SOUL.md) — Propuesta de perfil `SOUL.md` para `bot:Subdirector 1`.
- [perfiles-propuestos/matriz-autonomia.md](perfiles-propuestos/matriz-autonomia.md) — Matriz de autonomía por operación y nivel de riesgo (`BAJO` a `MUY ALTO`).

## Guía rápida: ciclo de vida de un encargo

1. **Arranque:** el Owner plantea un objetivo a `bot:Director General`, quien evalúa impacto y riesgo (`BAJO`, `MEDIO`, `ALTO`, `MUY ALTO`) y crea o actualiza el Item en Orca con `done-means` verificable.
2. **Delegación asíncrona:** Dirección delega a Subdirección (`bot:Subdirector 1`) mediante `--type handoff` vinculado al Item. Subdirección selecciona carril (*Vía Ligera* o *Vía Completa*), redacta el encargo usando [plantillas/brief.md](plantillas/brief.md) y lanza un worker autor aislado con `orca orchestration worker-start --worktree new-child`.
3. **Ejecución y verificación determinista:** el worker ejecuta dentro de su worktree, corre checks deterministas (tests, linters, frontera de seguridad, formato `LF`), deja un commit limpio, documenta su cierre con [plantillas/acta-entrega.md](plantillas/acta-entrega.md) y emite `worker_done`.
4. **Validación ciega independiente:** Subdirección despacha un validador distinto al autor (o a `Pull request review`) con únicamente el diff/`head` exacto y los criterios del brief. El juez emite [plantillas/veredicto.md](plantillas/veredicto.md) iniciando en línea 1 con:
   `veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>`
5. **Integración y cierre Kaizen:** con checks en verde, `GO` canónico vigente sobre el `head` exacto y autorización conforme a [perfiles-propuestos/matriz-autonomia.md](perfiles-propuestos/matriz-autonomia.md), el coordinador o especialista habilitado integra el commit exacto, cierra el Item, registra la micro-retrospectiva en [plantillas/kaizen-friccion.md](plantillas/kaizen-friccion.md) y destila aprendizajes duraderos en `MEMORY.md` si aplica.
