import anthropic, json

client = anthropic.Anthropic()

# ✅ HERRAMIENTAS BIEN DISEÑADAS
tools_batman = [
    {
        'name': 'buscar_sospechoso_gcpd',
        'description': 'Busca registros de sospechosos en la base de datos '
                       'de la GCPD (Gotham City Police Department) usando '
                       'nombre real o alias conocido. Usar cuando el testigo '
                       'o la evidencia menciona un nombre o alias. No usar '
                       'para búsquedas por descripción física.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'termino_busqueda': {
                    'type': 'string',
                    'description': 'Nombre real o alias del sospechoso. Ejemplo: El Acertijo, Edward Nygma'
                },
                'incluir_antecedentes': {
                    'type': 'boolean',
                    'description': 'Si true, incluye historial de arrestos y condenas previas'
                }
            },
            'required': ['termino_busqueda']
        }
    },
    {
        'name': 'analizar_evidencia_forense',
        'description': 'Analiza evidencia forense de la escena del crimen: '
                       'huellas dactilares, muestras de ADN, fibras, o '
                       'huellas de zapatos. Usar cuando hay evidencia física '
                       'recolectada en la escena. Devuelve coincidencias en '
                       'la base de datos forense de Gotham.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'tipo_evidencia': {
                    'type': 'string',
                    'enum': ['huella_dactilar', 'adn', 'fibra', 'huella_zapato'],
                    'description': 'Tipo de evidencia forense a analizar'
                },
                'descripcion': {
                    'type': 'string',
                    'description': 'Descripción de la evidencia encontrada en la escena'
                }
            },
            'required': ['tipo_evidencia', 'descripcion']
        }
    },
    {
        'name': 'generar_reporte_caso',
 'description': 'Genera el reporte final del caso de investigación. '
                       'Usar SOLO cuando ya se recolectó toda la evidencia '
                       'disponible y se identificaron los sospechosos. '
                       'No usar en medio de la investigación — es el paso final.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'sospechoso_principal': {'type': 'string'},
                'evidencia_recolectada': {'type': 'string'},
                'nivel_certeza': {
                    'type': 'string',
                    'enum': ['bajo', 'medio', 'alto', 'confirmado']
                }
            },
            'required': ['sospechoso_principal', 'evidencia_recolectada', 'nivel_certeza']
        }
    }
]

# Implementaciones simuladas de las herramientas
def buscar_sospechoso_gcpd(termino_busqueda, incluir_antecedentes=False):
    datos = {
        'El Acertijo': 'Edward Nygma. Antecedentes: 3 arrestos por crímenes temáticos. ' \
                       'Especialidad: acertijos y trampas elaboradas. Último avistamiento: ' \
                       'Distrito Financiero de Gotham.',
    }
    return datos.get(termino_busqueda, f'Sin registros para: {termino_busqueda}')

def analizar_evidencia_forense(tipo_evidencia, descripcion):
    return f'Análisis de {tipo_evidencia}: coincidencia encontrada en base de datos. ' \
           f'Índice de confianza: 87%. Coincide con muestra archivada de Edward Nygma.'

def generar_reporte_caso(sospechoso_principal, evidencia_recolectada, nivel_certeza):
    return f'REPORTE CASO #GC-2024-441 | Sospechoso: {sospechoso_principal} | ' \
           f'Certeza: {nivel_certeza} | Evidencia: {evidencia_recolectada} | ' \
           f'Recomendación: emitir orden de captura.'

IMPL = {
    'buscar_sospechoso_gcpd': buscar_sospechoso_gcpd,
    'analizar_evidencia_forense': analizar_evidencia_forense,
    'generar_reporte_caso': generar_reporte_caso
}

def correr_batman(caso):
    messages = [{'role': 'user', 'content': caso}]
    system = 'Sos Batman investigando un crimen en Gotham. Usá las herramientas disponibles ' \
             'para recolectar evidencia e identificar al sospechoso antes de cerrar el caso.'
    while True:
        resp = client.messages.create(model='claude-sonnet-4-6', max_tokens=800,
                                      system=system, tools=tools_batman, messages=messages)
        if resp.stop_reason == 'end_turn':
            for b in resp.content:
                if hasattr(b,'text'): print(f'Batman: {b.text}')
            break
        if resp.stop_reason == 'tool_use':
            messages.append({'role':'assistant','content':resp.content})
            results = []
            for b in resp.content:
                if b.type == 'tool_use':
                    print(f'[TOOL] {b.name} → {json.dumps(b.input, ensure_ascii=False)}')
                    r = IMPL[b.name](**b.input)
                    print(f'[RESULT] {r[:100]}...')
                    results.append({'type':'tool_result','tool_use_id':b.id,'content':r})
            messages.append({'role':'user','content':results})

caso = 'Escena del crimen en el Museo de Gotham. Hay una huella dactilar en el cristal roto. ' \
       'El guardia de seguridad menciona que escuchó a alguien decir El Acertijo antes de huir.'
correr_batman(caso)
