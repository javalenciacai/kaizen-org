estado: LISTO_PARA_VALIDACION | PARCIAL | BLOQUEADO · item: <referencia-del-item>

# Acta de entrega: <Título del encargo>

## 1. Resumen ejecutivo

<Máximo 4 líneas explicando qué se construyó o resolvió, qué se comprobó y qué paso sigue.>

## 2. Identificación Git

- **Entorno lógico:** `local` | `windows-local`
- **Repositorio:** `<nombre-repo>`
- **Rama:** `<nombre-rama-worktree>`
- **Head (`sha40`):** `<sha40-completo>`
- **Estado del árbol:** `git status --porcelain` vacío (`sí` / `no`)

## 3. Archivos modificados o creados

- `<ruta/relativa/archivo-1>` — <cambio breve>
- `<ruta/relativa/archivo-2>` — <cambio breve>

## 4. Salida de checks deterministas y frontera de seguridad

| Verificación | Comando ejecutado | Resultado | Evidencia resumida |
| :--- | :--- | :--- | :--- |
| Pruebas / contrato | `<comando>` | `PASS` / `FAIL` | `<conteo o salida breve>` |
| Higiene `LF` / formato | `<comando>` | `PASS` / `FAIL` | `<0 archivos CRLF>` |
| Frontera de seguridad | `<comando>` | `PASS` / `FAIL` | `<0 secretos, 0 UUIDs, 0 rutas privadas>` |
| Enlaces / integridad | `<comando>` | `PASS` / `FAIL` | `<todos los enlaces válidos>` |

## 5. Riesgos, supuestos o pendientes

- <Ninguno, o listar de forma honesta cualquier límite, riesgo residual o pendiente exacto.>

## 6. Micro-retrospectiva Kaizen

> Completar con `sin_hallazgos` o con 1 a 2 fricciones reales verificables siguiendo [plantillas/kaizen-friccion.md](kaizen-friccion.md).

- **Estado Kaizen:** `sin_hallazgos` | `con_hallazgos`
- **Fricción 1 (opcional):** <Hecho verificable · impacto · propuesta puntual>
- **Fricción 2 (opcional):** <Hecho verificable · impacto · propuesta puntual>
