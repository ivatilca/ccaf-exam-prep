# M5 — Tool Use: Conceptual y Gestión de Contexto

**Universo temático:** Matrix  
**Videos:** M5V1, M5V2, M5V3, M5V4, M5V5  
**Dominio CCA-F:** D1 + D2 — Agentic Architecture & Tool Use (22%)

## ¿Qué cubre este módulo?

- **M5V1:** Conceptos fundamentales de tool use: qué son las tools, cuándo usarlas, principio del menor privilegio
- **M5V2:** Tool results y su impacto en el contexto: cómo los resultados consumen tokens
- **M5V3:** Gestión de contexto con tool use: filtrado, summarización, estrategias anti-overflow
- **M5V4:** Patrones de tool use en agentes: secuencial, paralelo, condicional
- **M5V5:** Tools como mecanismo de delegación entre agentes

## Archivos

| Archivo | Video | Qué demuestra |
|---------|-------|---------------|
| `tool_result_contexto.py` | M5V2/M5V3 | Cómo los tool results impactan el context window y estrategias de filtrado |

## Conceptos CCA-F clave

- **Principio del menor privilegio:** dar al agente solo las tools estrictamente necesarias para la tarea
- **Tool result size:** los tool results grandes consumen tokens del context window — filtrar antes de devolver
- **Context overflow:** cuando el historial de mensajes + tool results supera el límite del contexto
- **Estrategias anti-overflow:** summarización del historial, truncado de tool results, RAG
- **Delegación via tools:** un agente puede tener una tool que invoca a otro agente (sub-agente)
