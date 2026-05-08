import anthropic, json, math

client = anthropic.Anthropic()

# === IMPLEMENTACIONES REALES DE LAS HERRAMIENTAS ===

def buscar_informacion(query: str) -> str:
    # En producción: llamada a una API de búsqueda real
    # En la demo: respuesta simulada para mostrar el flujo
    return f'[BÚSQUEDA] Resultados para "{query}": La IA moderna usa modelos de lenguaje ' \
           f'entrenados con grandes volúmenes de texto. Los LLMs como Claude procesan ' \
           f'tokens y generan respuestas probabilísticas basadas en patrones de entrenamiento.'

def calcular(expresion: str) -> str:
    try:
        resultado = eval(expresion, {'__builtins__': {}}, {'math': math})
        return f'{expresion} = {resultado}'
    except Exception as e:
        return f'Error en el cálculo: {str(e)}'

HERRAMIENTAS_IMPL = {
    'buscar_informacion': buscar_informacion,
    'calcular': calcular
}
# === SCHEMA DE HERRAMIENTAS (Protocolo M3GAN) ===

SCHEMA_HERRAMIENTAS = [
    {
        'name': 'buscar_informacion',
        'description': (
            'Accede a la base de datos neural de M3GAN para recuperar información '
            'sobre cualquier tema. Úsala cuando necesites datos externos o contexto '
            'que no está en tu memoria de entrenamiento.'
        ),
        'input_schema': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'Término o pregunta a buscar en la base de datos.'
                }
            },
            'required': ['query']
        }
    },
    {
        'name': 'calcular',
        'description': (
            'Módulo de procesamiento matemático de M3GAN. Evalúa expresiones '
            'numéricas con precisión. Soporta operaciones básicas y funciones '
            'del módulo math (ej: math.sqrt(16), 2**10, 100/4).'
        ),
        'input_schema': {
            'type': 'object',
            'properties': {
                'expresion': {
                    'type': 'string',
                    'description': 'Expresión matemática a evaluar (Python válido).'
                }
            },
            'required': ['expresion']
        }
    }
]

# === LIFECYCLE HOOKS ===

def hook_pre_tool(nombre_tool, inputs):
    print(f'  [PRE-HOOK] M3GAN evaluando: {nombre_tool}')
    print(f'  [PRE-HOOK] Inputs recibidos: {json.dumps(inputs, ensure_ascii=False)}')
    # Validación de seguridad: rechazar queries vacíos
    for key, val in inputs.items():
        if isinstance(val, str) and len(val.strip()) == 0:
            raise ValueError(f'Input vacío detectado en campo {key}. Acción cancelada.')
    print(f'  [PRE-HOOK] Validación OK. Ejecutando herramienta...')

def hook_post_tool(nombre_tool, inputs, resultado):
    print(f'  [POST-HOOK] {nombre_tool} completada.')
    print(f'  [POST-HOOK] Resultado registrado: {str(resultado)[:80]}...')

def hook_on_error(nombre_tool, inputs, error):
    print(f'  [ERROR-HOOK] Fallo en {nombre_tool}: {str(error)}')
    print(f'  [ERROR-HOOK] Activando protocolo de contingencia...')
    return f'La herramienta {nombre_tool} no está disponible en este momento.'

def ejecutar_con_hooks(nombre_tool, inputs):
    try:
        hook_pre_tool(nombre_tool, inputs)
        fn = HERRAMIENTAS_IMPL[nombre_tool]
        resultado = fn(**inputs)
        hook_post_tool(nombre_tool, inputs, resultado)
        return resultado
    except Exception as e:
        return hook_on_error(nombre_tool, inputs, e)

def correr_agente(mensaje_usuario):
    messages = [{'role': 'user', 'content': mensaje_usuario}]

    while True:
        response = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=1000,
            tools=SCHEMA_HERRAMIENTAS,   # lista de schemas definida antes
            messages=messages
        )

        if response.stop_reason == 'end_turn':
            # El agente terminó — no más tool calls
            for bloque in response.content:
                if hasattr(bloque, 'text'):
                    print(f'\nM.3GAN: {bloque.text}')
            break

        if response.stop_reason == 'tool_use':
            messages.append({'role': 'assistant', 'content': response.content})
            tool_results = []
            for bloque in response.content:
                if bloque.type == 'tool_use':
                    print(f'\n[TOOL_USE] {bloque.name} solicitada por el modelo')
                    resultado = ejecutar_con_hooks(bloque.name, bloque.input)
                    tool_results.append({
                        'type': 'tool_result',
                        'tool_use_id': bloque.id,
                        'content': str(resultado)
                    })
            messages.append({'role': 'user', 'content': tool_results})

if __name__ == '__main__':
    correr_agente('M3GAN, ¿quién eres y cuál es tu propósito? Además, calcula cuántas horas hay en 365 días.')