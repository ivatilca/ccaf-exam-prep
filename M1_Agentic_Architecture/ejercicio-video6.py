import anthropic, json, datetime
from pathlib import Path

client = anthropic.Anthropic()

# ── EXTERNAL MEMORY: base de datos de mutantes (Cerebro simulado) ──
CEREBRO_DB = {
    'cyclops': {'nombre': 'Scott Summers', 'poder': 'rayos ópticos', 'nivel': 'omega', 'equipo': 'X-Men'},
    'storm': {'nombre': 'Ororo Munroe', 'poder': 'control del clima', 'nivel': 'omega', 'equipo': 'X-Men'},
    'magneto': {'nombre': 'Erik Lehnsherr', 'poder': 'magnetismo', 'nivel': 'omega', 'afiliacion': 'neutral'},
    'mystique': {'nombre': 'Raven Darkholme', 'poder': 'metamorfosis', 'nivel': 'beta', 'afiliacion': 'variable'},
    'beast': {'nombre': 'Hank McCoy', 'poder': 'intelecto/fisico mejorado', 'nivel': 'beta', 'equipo': 'X-Men'},
}

# ── EPISODIC MEMORY: archivo de sesiones pasadas (Jean Grey pattern) ─
EPISODIC_FILE = '/tmp/xavier_episodic_memory.json'

def cargar_memoria_episodica() -> list:
    if Path(EPISODIC_FILE).exists():
        with open(EPISODIC_FILE) as f:
            return json.load(f)
    return []

def guardar_memoria_episodica(resumen: dict):
    memoria = cargar_memoria_episodica()
    memoria.append(resumen)
    memoria = memoria[-5:]  # guardar solo las ultimas 5 sesiones
    with open(EPISODIC_FILE, 'w') as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

# ── WINDOWING: comprimir context si crece demasiado ─────────────────
MAX_MESSAGES = 8

def aplicar_windowing(messages: list) -> list:
    if len(messages) <= MAX_MESSAGES:
        return messages

    print(f'  🔄 [JEAN GREY] Context largo ({len(messages)} msgs) — comprimiendo...')
    msgs_a_comprimir = messages[:-4]  # comprimir todo menos los ultimos 4
    texto = json.dumps(msgs_a_comprimir, ensure_ascii=False)

    resumen_resp = client.messages.create(
        model='claude-haiku-4-5-20251001', max_tokens=512,
        messages=[{'role': 'user', 'content': f'Resume los puntos clave de esta conversacion: {texto[:3000]}'}]
    )
    resumen_texto = resumen_resp.content[0].text

    mensaje_resumen = {
        'role': 'user',
        'content': f'[RESUMEN DE CONVERSACION ANTERIOR]: {resumen_texto}'
    }
    return [mensaje_resumen] + messages[-4:]

# ── TOOLS ───────────────────────────────────────────────────────────
TOOLS = [
    {
        'name': 'consultar_cerebro',
        'description': 'Consulta la base de datos Cerebro para obtener informacion de un mutante. Usar cuando necesites datos sobre poderes, nivel o afiliacion de un mutante especifico.',
        'input_schema': {'type': 'object', 'properties': {
            'nombre_clave': {'type': 'string', 'description': 'Nombre clave del mutante (ej: cyclops, storm, magneto)'}
        }, 'required': ['nombre_clave']}
    },
    {
        'name': 'buscar_mutantes_por_nivel',
        'description': 'Busca todos los mutantes de un nivel de poder especifico en Cerebro.',
        'input_schema': {'type': 'object', 'properties': {
            'nivel': {'type': 'string', 'enum': ['omega', 'beta', 'alpha'], 'description': 'Nivel de poder mutante'}
        }, 'required': ['nivel']}
    },
]

def ejecutar_tool(name: str, args: dict) -> dict:
    if name == 'consultar_cerebro':
        key = args['nombre_clave'].lower()
        if key in CEREBRO_DB:
            print(f'  🔵 [CEREBRO] Perfil recuperado: {key}')
            return {'encontrado': True, 'perfil': CEREBRO_DB[key]}
        return {'encontrado': False, 'mensaje': f'Mutante {key} no registrado en Cerebro'}
    elif name == 'buscar_mutantes_por_nivel':
        nivel = args['nivel']
        resultados = {k: v for k, v in CEREBRO_DB.items() if v.get('nivel') == nivel}
        print(f'  🔵 [CEREBRO] {len(resultados)} mutantes nivel {nivel} encontrados')
        return {'nivel': nivel, 'mutantes': resultados}
    return {'error': 'tool desconocida'}


# ── AGENTE CON MEMORIA COMPLETA ──────────────────────────────────────
def xavier(mision: str):
    print('\n🧠 [XAVIER] Iniciando sesión...')

    # Recuperar memoria episódica
    episodios = cargar_memoria_episodica()
    if episodios:
        ultimo = episodios[-1]
        print(f'  📚 [JEAN GREY] Memoria episódica cargada: {ultimo["timestamp"]}')
        print(f'     {ultimo["resumen"][:100]}...')
        contexto_episodico = f'[MEMORIA EPISODICA DE SESION ANTERIOR ({ultimo["timestamp"]})]: {ultimo["resumen"]}'
    else:
        contexto_episodico = '[Sin memoria episodica previa]'
        print('  📚 [JEAN GREY] Primera sesion — sin episodios previos.')

    # Sistema prompt con in-context + episodic memory
    system = f'''Sos el Agente Xavier, coordinador de los X-Men.
Tenes acceso a Cerebro (base de datos de mutantes) via herramientas.

MEMORIA EPISODICA: {contexto_episodico}

Instrucciones:
- Usa consultar_cerebro cuando necesites datos de un mutante especifico
- Usa buscar_mutantes_por_nivel para identificar grupos por poder
- Fundamenta tus respuestas en los datos de Cerebro, no en suposiciones'''

    messages = [{'role': 'user', 'content': mision}]
    print(f'  🎯 Misión: {mision[:80]}\n')

    while True:
        # Windowing: comprimir si el context crece
        messages = aplicar_windowing(messages)

        response = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=1024,
            system=system,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == 'end_turn':
            respuesta_final = response.content[0].text
            print(f'\n✅ [XAVIER]: {respuesta_final}')
            break

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    resultado = ejecutar_tool(block.name, block.input)
                    tool_results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': json.dumps(resultado, ensure_ascii=False)})
            messages.append({'role': 'assistant', 'content': response.content})
            messages.append({'role': 'user', 'content': tool_results})

    # Generar y guardar memoria episódica (Jean Grey pattern)
    print('\n📝 [JEAN GREY] Generando resumen episódico...')
    resumen_resp = client.messages.create(
        model='claude-haiku-4-5-20251001', max_tokens=256,
        messages=[{'role': 'user', 'content': f'Resume en 2-3 oraciones los hallazgos clave de esta sesion sobre mutantes: Mision: {mision}. Respuesta: {respuesta_final}'}]
    )
    resumen = resumen_resp.content[0].text
    guardar_memoria_episodica({'timestamp': datetime.datetime.now().isoformat()[:19], 'mision': mision[:60], 'resumen': resumen})
    print(f'  ✓ Episodio guardado: {resumen[:80]}...')
    return respuesta_final

# ── Entry point ──────────────────────────────────────────────────────
xavier('Necesito un briefing de todos los mutantes nivel omega disponibles y una evaluacion de la amenaza que representa Magneto si actua junto a Mistica.')

