# M3 — Claude Code: Avanzado y CI/CD

**Videos:** M3V1, M3V2, M3V3, M3V4, M3V5  
**Dominio CCA-F:** D2 — Tool Use & Claude Code (22% del examen)

## ¿Qué cubre este módulo?

- **M3V1:** Claude Code en proyectos reales: CLAUDE.md como instrucción de operador, estructura inicial vs. final
- **M3V2:** Hooks y sistema de permisos: allow/deny en settings.json, PreToolUse y PostToolUse
- **M3V3:** MCP Servers en Claude Code: dos transportes (stdio y HTTP), scopes de permisos y diagnóstico
- **M3V4:** Sub-agentes con Claude Code: delegación y coordinación
- **M3V5:** Claude Code en CI/CD y flujos de equipo — **el más evaluado en el examen**

## Archivos

| Carpeta / Archivo | Video | Universo | Qué demuestra |
|-------------------|-------|----------|---------------|
| `ejercicio-video1/project-inicial/` | M3V1 | Rebel Alliance | CLAUDE.md mínimo: project overview, commands básicos, arquitectura del proyecto Flask + SQLite + pytest |
| `ejercicio-video1/project-final/` | M3V1 | Rebel Alliance | CLAUDE.md completo: agrega convenciones de código, notas de discrepancia entre docs y código real, instrucciones de test con coverage |
| `ejercicio-video2/settings.json` | M3V2 | Spider-Man | Sistema de permisos: allow list granular (`Bash(git *)`, `Bash(pytest *)`), deny list de operaciones destructivas (`rm -rf`, `sudo`, `curl | bash`, escritura a `.env`) |
| `ejercicio-video2/hooks/spider_sense.py` | M3V2 | Spider-Man | Hook PreToolUse: bloquea escrituras a rutas protegidas (`/secrets/`, `.env`, `config.prod`) y comandos bash peligrosos (regex sobre `rm -rf`, `sudo`, `chmod 777`) |
| `ejercicio-video2/hooks/audit_logger.py` | M3V2 | Spider-Man | Hook PostToolUse: registra cada acción del agente en `audit.log` con timestamp, tool name e input summary — solo observa, no toma decisiones |
| `ejercicio-video3/Puntoclaude/mcp/db_server.py` | M3V3 | Rebel Alliance | Servidor MCP `rebel-db` con transporte **stdio**: 3 tools (`list_tables`, `query_database` solo lectura, `execute_transaction` con guard) |
| `ejercicio-video3/Puntoclaude/mcp/github_server.py` | M3V3 | Rebel Alliance | Servidor MCP `rebel-github` con transporte **HTTP** (`streamable-http`, puerto 8080): 4 tools (`list_issues`, `get_file`, `create_pr`, `merge_branch`) |
| `ejercicio-video3/Puntoclaude/settings.json` | M3V3 | Rebel Alliance | Permisos de MCP tools explícitos: `mcp__rebel-db__query_database` permitido, `mcp__rebel-db__execute_transaction` denegado |
| `ejercicio-video3/Puntoclaude/settings.local.json` | M3V3 | Rebel Alliance | Activación local de MCP servers (`enabledMcpjsonServers`) — este archivo va en `.gitignore` |
| `ejercicio-video3/seed_db.py` | M3V3 | Rebel Alliance | Script para recrear la DB con 14 misiones, 5 agentes y 4 recursos |

## Conceptos CCA-F clave

### CLAUDE.md como instrucción de operador (M3V1)
- CLAUDE.md es leído automáticamente por Claude Code al iniciar — equivale al `system` prompt del operador
- Jerarquía de archivos: `~/.claude/CLAUDE.md` (global) → `.claude/CLAUDE.md` (proyecto) → subcarpetas
- El CLAUDE.md debe incluir: comandos del proyecto, arquitectura, convenciones de código, restricciones explícitas
- **Inicial vs. final:** la diferencia entre un CLAUDE.md mínimo y uno completo está en las convenciones y las notas sobre discrepancias entre docs y código real — Claude Code trabaja mejor cuanto más preciso es el contexto

### Hooks y sistema de permisos (M3V2)
- `settings.json` define las reglas de permiso; el sistema las aplica antes de ejecutar cualquier tool
- Permisos granulares: `Bash(git *)` permite solo comandos git, no cualquier bash
- **PreToolUse** (`spider_sense.py`): recibe el evento por stdin, devuelve `{"decision": "approve"}` o `{"decision": "block", "reason": "..."}` — puede cancelar la ejecución antes de que ocurra
- **PostToolUse** (`audit_logger.py`): recibe el resultado, no toma decisiones — solo registra; no necesita devolver nada
- Los hooks son procesos externos: Claude Code los ejecuta, pasa el contexto por stdin y lee la respuesta por stdout

### MCP Servers en Claude Code (M3V3)
- **Transporte stdio:** el servidor MCP corre como subproceso del cliente; Claude Code lo lanza y se comunica por stdin/stdout — ideal para tools locales
- **Transporte HTTP (`streamable-http`):** el servidor MCP escucha en un puerto; el cliente se conecta vía HTTP — permite servidores remotos y multi-cliente
- **Scopes de permisos MCP:** cada tool de un MCP server se puede permitir o denegar individualmente con el patrón `mcp__<server-name>__<tool-name>`
- **`settings.local.json`:** activa los servidores MCP para el entorno local; no se commitea porque puede contener rutas o tokens de la máquina del desarrollador
- Diagnóstico: si un MCP tool no aparece, verificar que el servidor esté corriendo, que el transporte coincida y que el tool esté en la allow list

### Modo headless y CI/CD (M3V5)
```bash
# Sin interacción — ideal para CI/CD
claude --print "Revisá los cambios en git diff y reportá problemas"
claude -p "Analizá este archivo" --output-format json
```

### Exit codes (M3V5)
| Código | Significado |
|--------|-------------|
| `0` | Éxito — tarea completada |
| `1` | Error de Claude (problema interno del modelo) |
| `2` | Tarea fallida (el modelo completó pero la tarea no se pudo cumplir) |
