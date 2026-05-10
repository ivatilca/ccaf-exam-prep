import anthropic, json, time, random

client = anthropic.Anthropic()

# Contador para simular falla en el primer intento
intentos_radar = 0

def radar_shield(centro: str, radio_km: int) -> str:
    global intentos_radar
    intentos_radar += 1

    # Simular falla en el primer intento — interferencia electromagnética
    if intentos_radar == 1:
        return json.dumps({
            'error': 'interferencia_electromagnetica',
            'causa': 'Anomalía energética detectada en el área — señal de satélite bloqueada',
            'sistemas_afectados': ['radar_largo_alcance', 'comunicaciones_SHIELD'],
            'accion_sugerida': 'usar_sensor_local como alternativa inmediata',
            'reintentable': False
        })

    # Éxito en intentos posteriores
    return json.dumps({
        'estado': 'ok',
        'objetivos_detectados': [
            {'nombre': 'aeronave_no_identificada', 'coordenadas': '40.71N,74.01W', 'amenaza': 'alta'},
            {'nombre': 'vehiculo_terrestre', 'coordenadas': '40.73N,73.98W', 'amenaza': 'media'}
        ],
        'cobertura_km': radio_km,
        'fuente': 'red_satelital_SHIELD'
    })

def sensor_local(centro: str, radio_km: int) -> str:
    # Vision siempre disponible — fallback confiable
    radio_efectivo = min(radio_km, 15)  # Sensor local tiene menor alcance
    return json.dumps({
        'estado': 'ok',
        'objetivos_detectados': [
            {'nombre': 'aeronave_no_identificada', 'coordenadas': '40.71N,74.01W', 'amenaza': 'alta'}
        ],
        'cobertura_km': radio_efectivo,
        'nota': f'Alcance limitado a {radio_efectivo}km por uso de sensor local',
        'fuente': 'sensores_Vision'
    })

IMPLS = {'radar_shield': radar_shield, 'sensor_local': sensor_local}

TOOLS_AVENGERS = [
    {
        'name': 'radar_shield',
        'description': 'Detecta amenazas usando la red satelital de SHIELD. '
                       'Cobertura máxima: 500km. '
                       'ERRORES POSIBLES: '
                       '- interferencia_electromagnetica: usar sensor_local como fallback. '
                       '- satelite_no_disponible: reintentable después de 30 segundos. '
                       'Si ves un error con reintentable=False, cambiá a sensor_local directamente.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'centro': {'type': 'string', 'description': 'Punto central de detección'},
                'radio_km': {'type': 'integer', 'description': 'Radio de búsqueda en km (1-500)'}
            },
            'required': ['centro', 'radio_km']
        }
    },
    {
        'name': 'sensor_local',
        'description': 'Escáner de corto alcance de Vision — siempre disponible, '
                       'alcance máximo 15km. Usar como fallback si radar_shield falla. '
                       'Menos preciso que radar_shield pero no depende de satélites.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'centro': {'type': 'string'},
                'radio_km': {'type': 'integer', 'description': 'Hasta 15km efectivos'}
            },
            'required': ['centro', 'radio_km']
        }
    }
]

def jarvis(mision: str):
    messages = [{'role': 'user', 'content': mision}]
    system = ('Sos JARVIS, el sistema de IA de Iron Man. Tenés acceso a herramientas de detección. '
              'Si una herramienta falla, leé el error estructurado y elegí la alternativa correcta. '
              'Siempre informá qué herramienta usaste y por qué.')

    print(f'JARVIS iniciando: {mision[:60]}...')
    print()

    while True:
        resp = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=600,
            system=system,
            tools=TOOLS_AVENGERS,
            messages=messages
        )

        if resp.stop_reason == 'end_turn':
            for bloque in resp.content:
                if hasattr(bloque, 'text'):
                    print(f'JARVIS: {bloque.text}')
            break

        if resp.stop_reason == 'tool_use':
            messages.append({'role': 'assistant', 'content': resp.content})
            results = []
            for bloque in resp.content:
                if bloque.type == 'tool_use':
                    print(f'[TOOL_USE] {bloque.name} → {bloque.input}')
                    resultado = IMPLS[bloque.name](**bloque.input)
                    resultado_parsed = json.loads(resultado)

                    # Log del resultado — éxito o error
                    if 'error' in resultado_parsed:
                        print(f'[ERROR] {bloque.name} falló: {resultado_parsed["error"]}')
                        print(f'        Causa: {resultado_parsed["causa"]}')
                        print(f'        Acción sugerida: {resultado_parsed.get("accion_sugerida","n/a")}')
                    else:
                        print(f'[OK] {bloque.name} exitoso: {len(resultado_parsed.get("objetivos_detectados",[]))} objetivo(s)')

                    results.append({
                        'type': 'tool_result',
                        'tool_use_id': bloque.id,
                        'content': resultado  # El error estructurado va igual como tool_result
                    })
            messages.append({'role': 'user', 'content': results})

jarvis('Detectar amenazas en un radio de 50km alrededor de la Torre Avengers en Manhattan.')
