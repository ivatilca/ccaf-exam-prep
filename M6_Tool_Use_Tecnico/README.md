# M6 — Tool Use: Diseño Técnico e Implementación

**Universo temático:** Spider-Man  
**Videos:** M6V1, M6V2, M6V3, M6V4, M6V5  
**Dominio CCA-F:** D1 + D2 — Agentic Architecture & Tool Use (27%)

## ¿Qué cubre este módulo?

- **M6V1:** Anatomía técnica de una tool definition, flujo de 5 pasos del tool call, parallel tool use, `tool_choice`, diseño de tools
- **M6V2:** Computer Use y herramientas avanzadas
- **M6V3:** Tool use en sistemas de producción: observabilidad, retry logic, timeouts
- **M6V4:** Patrones de integración y arquitecturas con tools
- **M6V5:** Repaso final y simulacro CCA-F

## Archivos

| Archivo | Video | Qué demuestra |
|---------|-------|---------------|
| `tool_definition_completa.py` | M6V1 | Anatomía completa de una tool definition con JSON Schema — los 3 campos obligatorios |
| `ned_tool_runner.py` | M6V1 | Loop completo con parallel tool use, `tool_choice`, y manejo de errores con `is_error` |

## Conceptos CCA-F clave (M6V1)

### Los 3 campos obligatorios de una tool
```python
{
    "name":         "nombre_snake_case",      # identificador único
    "description":  "Qué hace, cuándo usarla, qué devuelve, cuándo NO usarla",
    "input_schema": {                          # JSON Schema — siempre type: object
        "type": "object",
        "properties": { ... },
        "required": [...]
    }
}
```

### El flujo de 5 pasos
1. Request inicial (tu código → API)
2. Respuesta con `tool_use` block (`stop_reason: "tool_use"`)
3. Ejecutar la tool (tu código ejecuta la función real)
4. Enviar `tool_result` con `role: "user"` y `tool_use_id` que coincide
5. Respuesta final (`stop_reason: "end_turn"`)

### `tool_choice`
| Valor | Comportamiento |
|-------|---------------|
| `auto` (default) | Claude decide si usar una tool o responder directo |
| `any` | Claude debe usar al menos una tool |
| `tool` + `name` | Claude debe usar exactamente esa tool |

### Errores
- `is_error: True` → fallo técnico (timeout, excepción) — Claude puede reintentar
- JSON con `{"error": ..., "mensaje": ...}` en `content` → resultado negativo esperado ("no encontrado")
