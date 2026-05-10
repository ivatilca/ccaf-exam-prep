# M2 — Tool Use y MCP: Fundamentos

**Videos:** M2V1, M2V2, M2V3, M2V4, M2V5  
**Dominio CCA-F:** D1 — Agentic Architecture (27%) · D3 — Claude Code (20%)

## ¿Qué cubre este módulo?

- **M2V1:** Anatomía de una tool: los 3 campos obligatorios, descriptions exhaustivas, schema tipado, y el agentic loop completo con tool use
- **M2V2:** MCP (Model Context Protocol): qué es, por qué existe, y las 3 primitivas (Tools, Resources, Prompts)
- **M2V3:** MCP transportes stdio vs HTTP, autenticación y seguridad
- **M2V4:** Principio de Menor Privilegio: cada agente recibe solo las tools que necesita
- **M2V5:** Error Handling en Tool Use: los 3 tipos de errores y cómo manejarlos

## Archivos

| Archivo | Video | Universo | Qué demuestra |
|---------|-------|----------|---------------|
| `ejercicio-video1.py` | M2V1 | Batman / DC | Tres tools bien diseñadas (`buscar_sospechoso_gcpd`, `analizar_evidencia_forense`, `generar_reporte_caso`) con descriptions exhaustivas, enums, y el loop completo de tool use. |
| `ejercicio-video2-r2d2.py` | M2V2 | Star Wars | Servidor MCP con las 3 primitivas: Tool (`hackear_puerta`), Resource (`r2d2://planos/estrella-de-la-muerte`), Prompt (`iniciar_mision_rescate`). |
| `ejercicio-video2-cliente.py` | M2V2 | Star Wars | Cliente MCP que se conecta al servidor R2D2 vía stdio, descubre capabilities y consume las 3 primitivas. |
| `ejercicio-video3.py` | M2V3 | The Mandalorian | Servidor MCP completo con transporte stdio: tool `aceptar_contrato`, resource `covert://gremio/registro`, prompt `iniciar_caceria`. |
| `ejercicio-video4.py` | M2V4 | Batman / DC | Principio de Menor Privilegio: Oracle recibe tools digitales, Robin tools de campo. Batman sintetiza sin tools propias. |
| `ejercicio-video5.py` | M2V5 | Los Vengadores | Error handling: error estructurado en `tool_result`, fallback entre tools (`radar_shield` → `sensor_local`), error documentado en description. |

---

## Conceptos CCA-F clave (M2V1 — Anatomía de una Tool)

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

## Conceptos CCA-F clave (M2V2 — Las 3 Primitivas MCP)

### Qué es MCP
El Model Context Protocol es un estándar abierto que define cómo los LLMs se conectan a sistemas externos. Separa el **host** (Claude) del **servidor** (la fuente de datos/acciones).

### Las 3 primitivas

| Primitiva | Dirección | Cuándo usarla | Ejemplo en R2D2 |
|-----------|-----------|---------------|-----------------|
| **Tool** | LLM → Sistema | Ejecutar acciones, mutar estado | `hackear_puerta` — abre/cierra puertas |
| **Resource** | Sistema → LLM | Exponer datos de solo lectura | `r2d2://planos/estrella-de-la-muerte` |
| **Prompt** | Sistema → LLM | Templates de instrucciones reutilizables | `iniciar_mision_rescate` |

### Cómo ejecutar el ejemplo Video 2
```bash
# Instalar dependencias
pip install mcp

# Terminal 1: el servidor corre en background (stdio)
# Terminal 2: ejecutar el cliente (levanta el servidor automáticamente)
python ejercicio-video2-cliente.py
```

---

## Conceptos CCA-F clave (M2V3 — Transportes stdio vs HTTP)

### stdio vs HTTP Streamable

| Aspecto | stdio | HTTP Streamable |
|---------|-------|-----------------|
| Comunicación | stdin/stdout del proceso | HTTP con SSE |
| Uso típico | Servidores locales, desarrollo | Servidores remotos, producción |
| Autenticación | Sin red — proceso hijo | OAuth 2.0, tokens |
| Ejemplo | `ejercicio-video2-r2d2.py`, `ejercicio-video3.py` | Servicios cloud |

El Mandaloriano (`ejercicio-video3.py`) usa **stdio**: el cliente levanta el servidor como subproceso, se comunica por pipes, y lo mata al terminar.

---

## Conceptos CCA-F clave (M2V4 — Principio de Menor Privilegio)

### La regla
Cada agente recibe **solo las tools necesarias para su rol**. No más.

### Implementación en Bat-Familia
```python
TOOLS_ORACLE = ['hackear_sistema', 'consultar_gcpd']   # solo digital
TOOLS_ROBIN  = ['analizar_forensic', 'entrevistar_testigo']  # solo campo
# Batman no tiene tools — solo sintetiza
```

### Por qué importa en el examen
- Reduce la superficie de ataque (un agente comprometido no puede escalar a otros sistemas)
- Mejora la predictibilidad (Oracle no intentará entrevistar testigos)
- Cada agente tiene un rol claro → descriptions más precisas → mejor selección de tools

---

## Conceptos CCA-F clave (M2V5 — Error Handling)

### Los 3 tipos de errores en Tool Use

| Tipo | Cómo se maneja | Ejemplo en JARVIS |
|------|---------------|-------------------|
| **Error en `tool_result`** | Devolver JSON estructurado con `error`, `causa`, `reintentable` | `radar_shield` devuelve `interferencia_electromagnetica` |
| **Fallback entre tools** | Documentado en `description` con instrucción explícita | "Si ves `reintentable=False`, cambiá a `sensor_local`" |
| **Error documentado** | La description especifica qué errores pueden ocurrir y qué hacer | Sección `ERRORES POSIBLES` en `radar_shield` |

### Patrón de error estructurado
```python
return json.dumps({
    'error': 'interferencia_electromagnetica',
    'causa': 'descripción humana del problema',
    'accion_sugerida': 'usar_sensor_local como alternativa',
    'reintentable': False   # Claude usa este flag para decidir si reintentar
})
```

El error va igual como `content` en `tool_result` — Claude lo lee y decide el siguiente paso.

---

## Comandos Claude Code CLI

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
