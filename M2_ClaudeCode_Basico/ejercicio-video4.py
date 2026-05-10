import anthropic, json

client = anthropic.Anthropic()

# ═══════════════════════════════════════════
# TOOLS DE ORACLE — investigación digital
# ═══════════════════════════════════════════
TOOLS_ORACLE = [
    {
        'name': 'hackear_sistema',
        'description': 'Accede remotamente a sistemas de seguridad: cámaras, alarmas, registros digitales. '
                       'Usar cuando hay infraestructura digital en la escena del crimen.',
        'input_schema': {'type':'object','properties':{
            'sistema': {'type':'string','description':'Tipo de sistema: camaras, alarmas, base_datos'},
            'ubicacion': {'type':'string'}
        },'required':['sistema','ubicacion']}
    },
    {
        'name': 'consultar_gcpd',
        'description': 'Consulta registros de la GCPD: arrestos, antecedentes, alias conocidos.',
        'input_schema': {'type':'object','properties':{
            'sospechoso': {'type':'string','description':'Nombre o alias del sospechoso'}
        },'required':['sospechoso']}
    }
]

# ═══════════════════════════════════════════
# TOOLS DE ROBIN — investigación de campo
# ═══════════════════════════════════════════
TOOLS_ROBIN = [
    {
        'name': 'analizar_forensic',
        'description': 'Analiza evidencia física en la escena: huellas, ADN, objetos dejados. '
                       'Usar cuando hay evidencia material recolectable.',
        'input_schema': {'type':'object','properties':{
            'tipo_evidencia': {'type':'string','enum':['huella','adn','objeto','rastro']},
            'descripcion': {'type':'string'}
        },'required':['tipo_evidencia','descripcion']}
    },
    {
        'name': 'entrevistar_testigo',
        'description': 'Entrevista a un testigo en la escena. Obtiene descripción del sospechoso, '
                       'timeline de eventos, y detalles del incidente.',
        'input_schema': {'type':'object','properties':{
            'nombre_testigo': {'type':'string'},
            'foco_entrevista': {'type':'string','description':'Qué información se busca obtener'}
        },'required':['nombre_testigo','foco_entrevista']}
    }
]

# Implementaciones simuladas
def hackear_sistema(sistema, ubicacion):
    resultados = {
        'camaras': f'Acceso a cámaras de {ubicacion} obtenido. Footage del Joker identificado: 22:47hs, salida norte.',
        'alarmas': f'Registro de alarmas de {ubicacion}: activada a las 22:43hs, desactivada internamente.',
        'base_datos': f'Base de datos de {ubicacion}: acceso denegado, sistema encriptado.'
    }
    return resultados.get(sistema, f'Sistema {sistema} no encontrado.')

def consultar_gcpd(sospechoso):
    return ('Joker — Jack Napier. 47 arrestos, 47 evasiones. Alias: el Príncipe Payaso. '
            'Último avistamiento: Arkham Asylum, fuga hace 3 semanas. MO: crímenes teatrales con gas de la risa.')

def analizar_forensic(tipo_evidencia, descripcion):
    return (f'Análisis de {tipo_evidencia}: naipes de la baraja del Joker encontrados en la escena. '
            f'Huella dactilar parcial en el cofre principal. Coincidencia 73% con archivo GCPD del Joker.')

def entrevistar_testigo(nombre_testigo, foco_entrevista):
    return (f'Testimonio de {nombre_testigo}: "Vi a un hombre con traje morado y maquillaje blanco. '
            f'Entró por la ventana norte a las 22:40, llevaba una bolsa verde. Se fue riendo."')

IMPL_ORACLE = {'hackear_sistema': hackear_sistema, 'consultar_gcpd': consultar_gcpd}
IMPL_ROBIN  = {'analizar_forensic': analizar_forensic, 'entrevistar_testigo': entrevistar_testigo}

def correr_subagente(nombre, system_prompt, tools, impls, mision):
    """Función genérica que corre cualquier subagente con sus tools específicas."""
    messages = [{'role': 'user', 'content': mision}]
    print(f'--- {nombre} investigando ---')
    while True:
        resp = client.messages.create(
            model='claude-sonnet-4-6', max_tokens=600,
            system=system_prompt, tools=tools, messages=messages
        )
        if resp.stop_reason == 'end_turn':
            resultado = next((b.text for b in resp.content if hasattr(b,'text')), '')
            print(f'{nombre}: {resultado[:150]}...')
            return resultado
        if resp.stop_reason == 'tool_use':
            messages.append({'role':'assistant','content':resp.content})
            results = []
            for b in resp.content:
                if b.type == 'tool_use':
                    print(f'  [TOOL] {nombre} usa: {b.name}')
                    r = impls[b.name](**b.input)
                    results.append({'type':'tool_result','tool_use_id':b.id,'content':r})
            messages.append({'role':'user','content':results})

def bat_familia(mision):
    print(f'BATMAN recibe misión: {mision[:80]}...')
    print()

    # Delegar a subagentes con sus tools específicas
    reporte_oracle = correr_subagente(
        'ORACLE',
        'Sos Oracle — investigadora digital de la Bat-Familia. Usá tus herramientas para '
        'recolectar toda la información digital disponible sobre el caso.',
        TOOLS_ORACLE, IMPL_ORACLE, mision
    )
    reporte_robin = correr_subagente(
        'ROBIN',
        'Sos Robin — investigador de campo. Analizá la evidencia física y entrevistá testigos.',
        TOOLS_ROBIN, IMPL_ROBIN, mision
    )

    # Batman sintetiza
    print()
    print('--- BATMAN sintetizando ---')
    sintesis = client.messages.create(
        model='claude-sonnet-4-6', max_tokens=400,
        system='Sos Batman. Sintetizá los reportes de Oracle y Robin en una conclusión operativa.',
        messages=[{'role':'user','content':
            f'Reporte Oracle (digital):\n{reporte_oracle}\n\n'
            f'Reporte Robin (campo):\n{reporte_robin}\n\n'
            f'Generá la conclusión y el próximo paso.'}]
    )
    print(f'BATMAN: {sintesis.content[0].text}')

bat_familia(
    'El Joker fue visto en el Banco de Gotham. '
    'Hay cámaras de seguridad y un testigo llamado Clark Kent en la escena.'
)
