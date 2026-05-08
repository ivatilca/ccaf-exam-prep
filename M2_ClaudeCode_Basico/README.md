# M2 — Claude Code: Fundamentos

**Videos:** M2V1, M2V2, M2V3, M2V4  
**Dominio CCA-F:** D3 — Claude Code (20% del examen)

## ¿Qué cubre este módulo?

- **M2V1:** Diseño de tools: los 3 campos obligatorios, descriptions exhaustivas, schema tipado, y el agentic loop completo con tool use
- **M2V2:** Hooks y permisos en Claude Code: `PreToolUse`, `PostToolUse`, `allowedTools`, `disallowedTools`
- **M2V3:** MCP Servers: qué son, cómo configurarlos, herramientas disponibles
- **M2V4:** Flujos complejos: slash commands, sesiones largas, patrones de uso avanzado

## Archivos

| Archivo | Video | Universo | Qué demuestra |
|---------|-------|----------|---------------|
| `ejercicio-video1.py` | M2V1 | Batman / DC | Tres tools bien diseñadas (`buscar_sospechoso_gcpd`, `analizar_evidencia_forense`, `generar_reporte_caso`) con descriptions exhaustivas, enums, y el loop completo de tool use. |

## Conceptos CCA-F clave (M2V1 — Tool Design)

### Los 3 campos obligatorios de una tool
```python
{
    "name":         "buscar_sospechoso_gcpd",       # snake_case, autodescriptivo
    "description":  "Qué hace. Cuándo usarla. Qué devuelve. Cuándo NO usarla.",
    "input_schema": {
        "type": "object",                            # SIEMPRE object en el raíz
        "properties": { ... },
        "required": [...]
    }
}
```

### Por qué la description es el campo más crítico
Claude decide qué tool usar basándose principalmente en la `description`, no en el `name`. Una description que incluye **cuándo NO usar la tool** es tan importante como explicar cuándo sí usarla. Ver `generar_reporte_caso` en el ejercicio: *"Usar SOLO cuando ya se recolectó toda la evidencia... No usar en medio de la investigación."*

### Tipos JSON Schema usados en el ejercicio
| Campo | Tipo | Detalle |
|-------|------|---------|
| `termino_busqueda` | `string` | texto libre |
| `incluir_antecedentes` | `boolean` | flag opcional |
| `tipo_evidencia` | `string` + `enum` | valor de lista fija: `huella_dactilar`, `adn`, `fibra`, `huella_zapato` |
| `nivel_certeza` | `string` + `enum` | `bajo`, `medio`, `alto`, `confirmado` |

### Principios de diseño demostrados
- **Una responsabilidad por tool:** cada una hace exactamente una cosa
- **Nombre autodescriptivo:** `buscar_sospechoso_gcpd` comunica qué hace y sobre qué datos
- **Enums para valores fijos:** evitan que Claude pase valores inventados
- **`required` solo para lo obligatorio:** `incluir_antecedentes` es opcional → no está en `required`

---

## Comandos Claude Code CLI (M2V1+)

```bash
# Instalación
npm install -g @anthropic-ai/claude-code

# Modo interactivo
claude

# Modo headless (CI/CD)
claude --print "tarea"
claude -p "tarea" --output-format json
claude -p "tarea" --max-turns 5
claude -p "tarea" --allowedTools Bash,Read
```

## Exit codes (examen CCA-F)
| Código | Significado |
|--------|-------------|
| `0` | Éxito |
| `1` | Error interno de Claude |
| `2` | Tarea fallida |
