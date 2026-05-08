# M4 — Prompt Engineering

**Universo temático:** Los Vengadores  
**Videos:** M4V1, M4V2, M4V3, M4V4, M4V5  
**Dominio CCA-F:** D4 — Prompt Engineering (20% del examen)

## ¿Qué cubre este módulo?

- **M4V1:** Fundamentos de prompt engineering: claridad, especificidad, estructura
- **M4V2:** Few-shot prompting: ejemplos positivos y negativos, selección de ejemplos
- **M4V3:** Chain-of-thought y razonamiento estructurado con XML tags
- **M4V4:** Tool use desde el prompt: cuándo incluir tools y cómo describirlas
- **M4V5:** Prompts para sistemas multi-agente: instrucciones de orquestador y sub-agentes

## Archivos

| Archivo | Video | Qué demuestra |
|---------|-------|---------------|
| `few_shot_ejemplo.py` | M4V2 | Few-shot prompting con ejemplos positivos y negativos |
| `chain_of_thought.py` | M4V3 | Chain-of-thought forzado con XML tags estructurados |

## Conceptos CCA-F clave

- **Few-shot:** proveer ejemplos de input→output deseado para que Claude imite el patrón
- **Chain-of-thought:** pedir razonamiento explícito antes de la respuesta final — mejora precisión en tareas complejas
- **XML tags:** estructurar el output de Claude con etiquetas para parseo programático (`<respuesta>`, `<razonamiento>`, `<confianza>`)
- **Ejemplos negativos:** mostrar lo que NO se quiere — tan efectivo como los ejemplos positivos
- **Especificidad:** cuanto más específico el prompt, más predecible el output de Claude
