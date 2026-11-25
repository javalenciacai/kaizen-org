# ADR 0002: Activación de perfiles directivos, Bloque B de autonomía, publicación pública e inicio de Fase 2

- **ID:** 0002
- **Fecha:** 2026-11-25
- **Estado:** Aceptada
- **Autores / Promotores:** Owner · `bot:Director General` · `bot:Subdirector 1`

---

## 1. Contexto

La Fase 1 de `kaizen-org` (`v0.1.0`, commit `05d3ef9ea1e7dae4ce9e895f42176a26e76f49e0`) cerró con verificación determinista en verde y **Validación Ciega Independiente** con veredicto canónico `GO`. Tras la revisión ejecutiva de los entregables fundacionales y de las propuestas en `perfiles-propuestos/`, el Owner aprobó formalmente el `2026-11-25` el paso a operación real controlada y la preparación del repositorio para publicación pública en GitHub.

Adicionalmente, la micro-retrospectiva Kaizen de Fase 1 identificó dos fricciones técnicas concretas (compatibilidad de `git init` con versiones de Git <2.28 y necesidad de auditar frontera exclusivamente sobre `git ls-files` + `git log` sin recorrer `.git` ni depender de `/proc`) que deben quedar institucionalizadas en el manual y en un verificador determinista multiplataforma.

---

## 2. Decisiones ratificadas (`2026-11-25`)

Por aprobación explícita del Owner se adoptan las siguientes decisiones en `v0.2.0`:

1. **Activación de perfiles `SOUL.md` directivos:**
   - Se ratifican los perfiles [perfiles-propuestos/director-general-SOUL.md](../perfiles-propuestos/director-general-SOUL.md) (`bot:Director General`) y [perfiles-propuestos/subdirector-1-SOUL.md](../perfiles-propuestos/subdirector-1-SOUL.md) (`bot:Subdirector 1`) para su instalación controlada en `<ORCA_HOME>/bots/<bot>/SOUL.md`.
2. **Promoción de `MATRIZ-AUTONOMIA.md` y activación del Bloque B:**
   - La matriz se promueve desde `perfiles-propuestos/matriz-autonomia.md` a documento vigente en raíz: [MATRIZ-AUTONOMIA.md](../MATRIZ-AUTONOMIA.md).
   - Quedan **ACTIVOS** los **Bloques (A) y (B)**, sujetando toda integración autónoma de Bloque B al cumplimiento estricto de checks deterministas, frontera de seguridad y `GO` canónico vigente sobre el `head` exacto (`sha40`).
   - El **Bloque (C)** permanece **100% intacto bajo aprobación explícita del Owner vía `Needs you`** (acciones `MUY ALTO`, repositorios remotos/visibilidad, edición de `SOUL.md` reales, alta/baja de bots permanentes, infraestructura crítica y excepciones a compuertas).
3. **Publicación pública de `kaizen-org` e inicio de Fase 2:**
   - Se autoriza preparar `kaizen-org` para su publicación como repositorio **público** en GitHub (`https://github.com/javalenciacai/kaizen-org`), endureciendo la frontera de tolerancia cero a secretos, tokens, UUIDs internos, handles de Orca, IPs privadas, nombres de host internos, correos personales reales y rutas locales privadas tanto en archivos versionados como en todo el historial `git log`.
   - Arranca **Fase 2**: diagnóstico y elaboración de propuestas de alineación `SOUL.md` para los 4 especialistas transversales en `perfiles-propuestos/especialistas-fase2/` (`Infra VM-Oracle`, `Infra Local Windows`, `Pull request review` y `Workspace cleanup`), **sin modificar infraestructura ni sus `SOUL.md` reales** hasta obtener aprobación explícita del Owner bajo Bloque C.

---

## 3. Incorporación formal de las 2 lecciones Kaizen de Fase 1

1. **Bootstrap Git compatible con Git <2.28:**
   - Todo repositorio nuevo se inicializa con `git init && git symbolic-ref HEAD refs/heads/main` en lugar de `git init -b main`, evitando fallos en nodos con Git anterior a 2.28.
2. **Verificador determinista multiplataforma sobre `git ls-files` + `git log`:**
   - Se incorpora [scripts/check_kaizen.py](../scripts/check_kaizen.py) (Python 3 estándar, compatible con `local` y `windows-local`, sin `/proc` ni `pwd`), que audita **exclusivamente** `git ls-files` y `git log` (nunca `os.walk` sobre `.git`), verificando UTF-8/`LF`, límite de líneas de [CONSTITUCION.md](../CONSTITUCION.md), Línea Canónica en [plantillas/veredicto.md](../plantillas/veredicto.md), frontera de repositorio público y validez del 100% de enlaces Markdown relativos.

---

## 4. Consecuencias y verificación

- **Inmediatas (`v0.2.0`):** `python3 scripts/check_kaizen.py` actúa como compuerta determinista obligatoria antes y después de cada commit en `kaizen-org`, tanto en `local` como en `windows-local`.
- **Operación bajo Bloque B:** Subdirección puede integrar cambios `BAJO`/`MEDIO` (y `ALTO` en ramas internas no productivas con validación reforzada) sin interrumpir al Owner siempre que todas las compuertas estén en verde; el Owner mantiene facultad de revocación inmediata en [MATRIZ-AUTONOMIA.md](../MATRIZ-AUTONOMIA.md).
- **Control de Fase 2:** las 4 propuestas en `perfiles-propuestos/especialistas-fase2/` permanecen en estado `PROPUESTA FASE 2` hasta superar validación independiente y firma explícita del Owner vía `Needs you`.
- **Criterio de medición Kaizen (próximas 3 entregas):** cero fallos de bootstrap Git, cero falsos positivos por lectura de `.git` y cero fugas de frontera detectadas en validación ciega.
