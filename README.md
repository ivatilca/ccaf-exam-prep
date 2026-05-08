# CCA-F Exam Prep — Curso Completo en Español

> El primer curso completo en español para la certificación **CCA-F (Claude Certified Associate — Foundations)** de Anthropic.  
> 7 módulos · 30 videos · 6 dominios del examen · Universos temáticos por módulo

---

## ¿Qué es la certificación CCA-F?

La CCA-F es la certificación técnica oficial de Anthropic para el ecosistema Claude. Evalúa competencias en arquitecturas agentivas, tool use, Claude Code en producción, prompt engineering, gestión de contexto e IA responsable. Este repositorio contiene **todo el código** que se presenta en los videos del curso.

---

## Mapa del Curso

| Módulo | Tema | Universos usados | Dominio Principal |
|--------|------|-----------------|-------------------|
| M0 | Fundamentos y contexto CCA-F | Spider-Man (Jameson) | — |
| M1 | Agentic Architecture | Sommelier · Harry Potter · Star Wars · M3GAN · Deadpool | D1 (27%) |
| M2 | Claude Code — Fundamentos | Batman / DC | D3 (20%) |
| M3 | Claude Code — Avanzado y CI/CD | M3gan | D2 (22%) |
| M4 | Prompt Engineering | Los Vengadores | D4 (20%) |
| M5 | Tool Use — Conceptual y Contexto | Matrix | D1+D2 (22%) |
| M6 | Tool Use — Diseño Técnico | Spider-Man | D1+D2 (27%) |

---

## Dominios del Examen CCA-F

| Dominio | Nombre | Peso |
|---------|--------|------|
| D1 | Agentic Architecture | 27% |
| D2 | Tool Use & Claude Code | 22% |
| D3 | Claude Code | 20% |
| D4 | Prompt Engineering | 20% |
| D5 | Context Management | 11% |
| D6 | Responsible AI | 5% |

---

## Estructura del Repositorio

```
ccaf-exam-prep/
├── README.md
├── .gitignore
│
├── M0_Fundamentos/
│   ├── README.md
│   ├── ejercicio-video2-ej1.py   ← system prompt: J. Jonah Jameson (titulares sesgados)
│   └── ejercicio-video2-ej2.py   ← multi-agente: Jameson (Haiku) + analista de medios (Sonnet)
│
├── M1_Agentic_Architecture/
│   ├── README.md
│   ├── ejercicio-video1.py       ← agentic loop: sommelier conversacional con while loop
│   ├── ejercicio-video2.py       ← pipeline multi-agente: Hermione · Ron · Dumbledore
│   ├── ejercicio'video3.py       ← session state: planificador + ejecutor (Star Wars)
│   ├── ejercicio'video4.py       ← tool use con hooks pre/post/error (M3GAN)
│   └── ejercicio'video5.py       ← HITL · guardrails · audit trail (Deadpool / Colossus)
│
├── M2_ClaudeCode_Basico/
│   ├── README.md
│   └── ejercicio-video1.py       ← tool design: 3 tools bien diseñadas (Batman / GCPD)
│
├── M3_ClaudeCode_Avanzado/
│   └── README.md                 ← código próximamente
│
├── M4_Prompt_Engineering/
│   └── README.md                 ← código próximamente
│
├── M5_Tool_Use_Conceptual/
│   └── README.md                 ← código próximamente
│
└── M6_Tool_Use_Tecnico/
    └── README.md                 ← código próximamente
```

---

## Requisitos

```bash
pip install anthropic
```

Todos los ejemplos usan el SDK oficial de Anthropic para Python. Necesitás una API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Cómo usar este repositorio

Cada carpeta de módulo tiene su propio `README.md` con:
- El tema del módulo y los videos que cubre
- Los conceptos CCA-F que se trabajan en el código
- Instrucciones de ejecución para cada archivo

Los archivos de código están ordenados para seguirse en paralelo con los videos del curso. No es necesario ejecutarlos para entender el contenido — pero sí ayuda.

---

## Videos del Curso

| # | Video ID | Título |
|---|----------|--------|
| 01 | M0V1 | Introducción al Ecosistema Claude y la Certificación CCA-F |
| 02 | M0V2 | Modelos Claude: Opus, Sonnet y Haiku — Cuándo Usar Cada Uno |
| 03 | M1V1 | Qué es un Agente y el Agentic Loop |
| 04 | M1V2 | El Context Window: Límites, Estrategias y Gestión |
| 05 | M1V3 | System Prompts en Arquitecturas Agentivas |
| 06 | M1V4 | Multi-Agent Systems: Orquestadores y Sub-agentes |
| 07 | M2V1 | Claude Code: Instalación, CLI y CLAUDE.md |
| 08 | M2V2 | Hooks y Permisos en Claude Code |
| 09 | M2V3 | MCP Servers: Extendiendo Claude Code |
| 10 | M2V4 | Flujos Complejos con Claude Code |
| 11 | M3V1 | Claude Code en Proyectos Reales |
| 12 | M3V2 | Debugging y Testing con Claude Code |
| 13 | M3V3 | Claude Code y Bases de Código Legacy |
| 14 | M3V4 | Sub-agentes con Claude Code |
| 15 | M3V5 | Claude Code en CI/CD y Flujos de Equipo |
| 16 | M4V1 | Fundamentos de Prompt Engineering para el CCA-F |
| 17 | M4V2 | Few-Shot Prompting y Ejemplos |
| 18 | M4V3 | Chain-of-Thought y Razonamiento Estructurado |
| 19 | M4V4 | Tool Use desde el Prompt: Cuándo y Cómo |
| 20 | M4V5 | Prompts para Sistemas Multi-agente |
| 21 | M5V1 | Tool Use: Conceptos Fundamentales |
| 22 | M5V2 | Tool Results y su Impacto en el Contexto |
| 23 | M5V3 | Gestión de Contexto con Tool Use |
| 24 | M5V4 | Patrones de Tool Use en Agentes |
| 25 | M5V5 | Tools como Mecanismo de Delegación |
| 26 | M6V1 | Tool Use: Diseño e Implementación Técnica |
| 27 | M6V2 | Computer Use y Herramientas Avanzadas |
| 28 | M6V3 | Tool Use en Sistemas de Producción |
| 29 | M6V4 | Patrones de Integración y Arquitecturas |
| 30 | M6V5 | Repaso Final y Simulacro CCA-F |

---

## Licencia

Uso educativo personal. El contenido del curso es propiedad de la autora.
