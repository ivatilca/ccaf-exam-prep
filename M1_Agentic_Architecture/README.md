# M1 — Agentic Architecture

**Videos:** M1V1, M1V2, M1V3, M1V4, M1V5  
**Dominio CCA-F:** D1 — Agentic Architecture (27% del examen)

## ¿Qué cubre este módulo?

- **M1V1:** El agentic loop: while loop, condiciones de parada, iteraciones con historial de mensajes
- **M1V2:** Multi-agent pipelines: agentes especializados con roles distintos que se encadenan
- **M1V3:** Session state: cómo mantener y pasar estado entre pasos de un agente planificador/ejecutor
- **M1V4:** Tool use con lifecycle hooks: pre-hook (validación), post-hook (auditoría), error-hook
- **M1V5:** HITL, guardrails de entrada/salida, audit trail, y clasificación de acciones reversibles vs. irreversibles

## Archivos

| Archivo | Video | Universo | Qué demuestra |
|---------|-------|----------|---------------|
| `ejercicio-video1.py` | M1V1 | Sommelier | Agentic loop conversacional: while loop que itera hasta que el modelo emite `accion: recomendar`. Output en JSON estructurado. |
| `ejercicio-video2.py` | M1V2 | Harry Potter | Pipeline multi-agente de 3 roles: Hermione (análisis de hechos / Sonnet), Ron (impacto en lenguaje simple / Haiku), Dumbledore (síntesis integradora / Sonnet). |
| `ejercicio'video3.py` | M1V3 | Star Wars | Session state con dict: Planificador genera el plan en JSON, Ejecutor procesa cada paso usando el contexto acumulado de pasos anteriores. |
| `ejercicio'video4.py` | M1V4 | M3GAN | Tool use con hooks: `hook_pre_tool` (validación de inputs), `hook_post_tool` (registro de resultado), `hook_on_error` (manejo de fallos). |
| `ejercicio'video5.py` | M1V5 | Deadpool / X-Men | HITL para acciones irreversibles, guardrail de salida con regex, audit trail completo, clasificación reversible/irreversible por tool. |

## Conceptos CCA-F clave

### Agentic loop (M1V1)
- `while iteracion < max_iteraciones` → condición de parada por límite de turnos
- El historial de `messages` se acumula en cada iteración — Claude ve todo el contexto previo
- El loop termina cuando el modelo decide internamente (acción de cierre en JSON) o se alcanza el límite

### Multi-agent pipeline (M1V2)
- Cada agente tiene su propio `system` prompt con un rol específico
- La salida de un agente se pasa como input al siguiente
- Modelo por agente según la complejidad de la tarea: Haiku para síntesis simple, Sonnet para razonamiento

### Session state (M1V3)
- `session_state = {'meta': ..., 'plan': ..., 'paso_actual': ..., 'resultados': {}, 'completado': False}`
- El estado se pasa explícitamente a cada llamada — Claude no "recuerda" entre llamadas sin el contexto
- Patrón Planificador/Ejecutor: separar la generación del plan de la ejecución paso a paso

### Lifecycle hooks (M1V4)
- `hook_pre_tool(nombre, inputs)` → validación antes de ejecutar (puede cancelar la ejecución)
- `hook_post_tool(nombre, inputs, resultado)` → registro después de ejecutar
- `hook_on_error(nombre, inputs, error)` → manejo de fallos sin romper el loop

### HITL y guardrails (M1V5)
- `REVERSIBILITY` dict → clasifica cada tool como reversible o no
- Acciones irreversibles pasan por `colossus_approve()` → input humano antes de ejecutar
- `output_guardrail(text)` → regex sobre la respuesta final antes de mostrarla al usuario
- `audit_log` → lista de todas las acciones con timestamp, tool, aprobador y reversibilidad
