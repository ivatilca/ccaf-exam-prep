# M0 — Fundamentos y Contexto CCA-F

**Videos:** M0V1, M0V2  
**Dominio CCA-F:** Introducción general (no entra directamente en el examen)

## ¿Qué cubre este módulo?

M0 establece el contexto del curso y de la certificación:

- **M0V1:** Qué es la CCA-F, los 6 dominios del examen y sus pesos, la estructura del ecosistema Claude (API, Claude Code, Claude.ai) — sin código
- **M0V2:** Primeros pasos con la API: system prompts, modelos, y pipeline multi-agente

## Archivos

| Archivo | Video | Qué demuestra |
|---------|-------|---------------|
| `ejercicio-video2-ej1.py` | M0V2 | System prompt con rol definido: J. Jonah Jameson generando titulares sesgados |
| `ejercicio-video2-ej2.py` | M0V2 | Pipeline multi-agente: Jameson (Haiku) genera el titular, un analista de medios (Sonnet) lo evalúa con JSON estructurado |

## Conceptos CCA-F

- **System prompt:** define el rol, el tono y las restricciones del modelo para toda la conversación
- **Selección de modelo por tarea:** Haiku para generación creativa simple, Sonnet para análisis y razonamiento
- **Output estructurado con JSON:** forzar a Claude a responder en JSON válido para parseo programático
- **Pipeline multi-agente básico:** la salida de un agente se convierte en el input del siguiente
