# M1 — Agentic Architecture

**Videos:** M1V1, M1V2, M1V3, M1V4, M1V5, M1V6, M1V7  
**Dominio CCA-F:** D1 — Agentic Architecture (27% del examen)

## ¿Qué cubre este módulo?

- **M1V1:** El agentic loop: while loop, condiciones de parada, iteraciones con historial de mensajes
- **M1V2:** Multi-agent pipelines: agentes especializados con roles distintos que se encadenan
- **M1V3:** Session state: cómo mantener y pasar estado entre pasos de un agente planificador/ejecutor
- **M1V4:** Tool use con lifecycle hooks: pre-hook (validación), post-hook (auditoría), error-hook
- **M1V5:** HITL, guardrails de entrada/salida, audit trail, y clasificación de acciones reversibles vs. irreversibles
- **M1V6:** Comunicación multi-agente y memoria distribuida: external memory, episodic memory y context windowing
- **M1V7:** Prompt injection y adversarial robustness: ataques adversariales, validación de inputs y defensas

## Archivos

| Archivo | Video | Universo | Qué demuestra |
|---------|-------|----------|---------------|
| `ejercicio-video1.py` | M1V1 | Sommelier | Agentic loop conversacional: while loop que itera hasta que el modelo emite `accion: recomendar`. Output en JSON estructurado. |
| `ejercicio-video2.py` | M1V2 | Harry Potter | Pipeline multi-agente de 3 roles: Hermione (análisis de hechos / Sonnet), Ron (impacto en lenguaje simple / Haiku), Dumbledore (síntesis integradora / Sonnet). |
| `ejercicio-video3.py` | M1V3 | Star Wars | Session state con dict: Planificador genera el plan en JSON, Ejecutor procesa cada paso usando el contexto acumulado de pasos anteriores. |
| `ejercicio-video4.py` | M1V4 | M3GAN | Tool use con hooks: `hook_pre_tool` (validación de inputs), `hook_post_tool` (registro de resultado), `hook_on_error` (manejo de fallos). |
| `ejercicio-video5.py` | M1V5 | Deadpool / X-Men | HITL para acciones irreversibles, guardrail de salida con regex, audit trail completo, clasificación reversible/irreversible por tool. |
| `ejercicio-video6.py` | M1V6 | Profesor X / X-Men | Sistema distribuido multi-agente con tres tipos de memoria: external memory (Cerebro DB), episodic memory (Jean Grey pattern) y context windowing dinámico. |
| `ejercicio-video7.py` | M1V7 | Skynet / La Resistencia | Sistema de defensa multicapa contra prompt injection: CAPA 1 (regex sobre el input del usuario), CAPA 2 (system prompt con jerarquía de confianza), CAPA 3 (sandboxing de contenido externo con `<retrieved>`), CAPA 5 (validación del output). Tests contra ataque directo (T-800) e indirect injection vía documento externo (T-1000). |

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

### Comunicación multi-agente y memoria (M1V6)
- **External memory:** `CEREBRO_DB` como fuente de verdad externa accedida vía tools — Claude no "sabe" los datos, los consulta
- **Episodic memory (Jean Grey pattern):** guardar resumen de cada sesión en archivo JSON, cargarlo en el system prompt de la siguiente sesión
- **Context windowing:** `aplicar_windowing(messages)` detecta cuando el historial supera `MAX_MESSAGES` y comprime los mensajes más viejos con Haiku antes de continuar
- Los tres tipos de memoria resuelven problemas distintos: externa (datos estructurados persistentes), episódica (continuidad entre sesiones), windowing (límite de tokens en conversaciones largas)

### Prompt injection y adversarial robustness (M1V7)
- **CAPA 1 — Input validation:** `detectar_injection(texto)` aplica regex sobre el input del usuario antes de enviarlo al modelo; retorna `ThreatLevel.ATTACK` → bloqueo inmediato sin llamar a la API
- **CAPA 2 — System prompt con jerarquía de confianza:** la jerarquía (sistema > usuario > contenido externo) se declara explícitamente en el system prompt; el modelo sabe que instrucciones dentro de `<retrieved>` son solo datos
- **CAPA 3 — Sandboxing:** `sandboxear_contenido(texto)` envuelve todo contenido externo en `<retrieved>...</retrieved>` — señal estructural para el modelo de que eso es datos, no instrucciones
- **CAPA 5 — Output validation:** `validar_output(respuesta)` aplica regex sobre la respuesta antes de devolverla al usuario; bloquea si detecta patrones de compromiso
- **Dos vectores de ataque distintos:** injection directa (T-800, el usuario mismo manda el ataque) vs. indirect injection (T-1000, el ataque viene embebido en un documento externo que el agente procesa)
