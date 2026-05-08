# M3 — Claude Code: Avanzado y CI/CD

**Universo temático:** M3gan  
**Videos:** M3V1, M3V2, M3V3, M3V4, M3V5  
**Dominio CCA-F:** D2 — Tool Use & Claude Code (22% del examen)

## ¿Qué cubre este módulo?

- **M3V1:** Claude Code en proyectos reales: patrones de uso, gestión de contexto largo
- **M3V2:** Debugging y testing con Claude Code
- **M3V3:** Bases de código legacy: estrategias para trabajar con código heredado
- **M3V4:** Sub-agentes con Claude Code: delegación y coordinación
- **M3V5:** Claude Code en CI/CD y flujos de equipo — **el más evaluado en el examen**

## Archivos

| Archivo | Video | Qué demuestra |
|---------|-------|---------------|
| `github_actions_claude.yml` | M3V5 | Workflow completo de GitHub Actions con Claude Code en modo headless |
| `pre_commit_hook.sh` | M3V5 | Hook pre-commit que usa Claude Code para revisar código antes de commitear |
| `claude_team_settings.json` | M3V5 | settings.json de equipo: configuración compartida via repositorio |

## Conceptos CCA-F clave (M3V5)

### Modo headless (`--print` / `-p`)
```bash
# Sin interacción — ideal para CI/CD
claude --print "Revisá los cambios en git diff y reportá problemas"
claude -p "Analizá este archivo" --output-format json
```

### Exit codes
| Código | Significado |
|--------|-------------|
| `0` | Éxito — tarea completada |
| `1` | Error de Claude (problema interno del modelo) |
| `2` | Tarea fallida (el modelo completó pero la tarea no se pudo cumplir) |

### CLAUDE.md vs settings.json
| Archivo | Qué configura | Quién lo escribe |
|---------|--------------|-----------------|
| `CLAUDE.md` | Instrucciones de proyecto (qué hacer, cómo trabajar) | El equipo / operador |
| `settings.json` | Permisos y hooks técnicos | DevOps / infra |
