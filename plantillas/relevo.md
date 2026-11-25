# Acta de Relevo: <Título del encargo>

- **Item:** `<referencia-del-item>`
- **Nivel de riesgo:** `BAJO` | `MEDIO` | `ALTO` | `MUY ALTO`
- **Motivo del relevo:** `agotamiento_de_cuota` | `interrupcion_entorno` | `cambio_de_nodo` | `reasignacion`
- **Rol saliente:** `<identidad/familia>`
- **Entorno lógico:** `local` | `windows-local`

## 1. Estado limpio en Git

- **Repositorio:** `<nombre-repo>`
- **Rama:** `<nombre-rama-worktree>`
- **Head actual (`sha40`):** `<sha40-completo>`
- **Árbol limpio (`git status --porcelain` vacío):** `sí` | `no` *(si es `no`, detallar qué quedó sin commitear y por qué)*

## 2. Qué quedó verificado (no repetir)

- [x] `<Hito o archivo verificado 1>` — Evidencia: `<comando o ruta:línea@sha>`
- [x] `<Hito o archivo verificado 2>` — Evidencia: `<comando o ruta:línea@sha>`

## 3. Qué falta exactamente para `done-means`

1. `<Paso pendiente 1, acotado y verificable>`
2. `<Paso pendiente 2, acotado y verificable>`
3. Ejecutar verificación determinista final y emitir [plantillas/acta-entrega.md](acta-entrega.md).

## 4. Comandos para retomar de inmediato

```bash
git checkout <nombre-rama-worktree>
git rev-parse HEAD   # Debe coincidir con <sha40-completo>
<comando-de-verificacion-o-prueba-actual>
```

## 5. Regla de independencia en validación

Al reasignar el relevo, la regla *"quien produce no valida"* se evalúa sobre la identidad del autor activo del entregable actual, sin imponer bloqueos históricos innecesarios.
