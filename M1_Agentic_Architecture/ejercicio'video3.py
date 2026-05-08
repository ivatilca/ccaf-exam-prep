import anthropic, json

client = anthropic.Anthropic()

SYSTEM_PLANIFICADOR = '''Sos un agente planificador.
Dada una meta, generá un plan en JSON con esta estructura exacta:
{
  "meta": "descripcion de la meta",
  "pasos": [
    {"id": 1, "tarea": "descripcion ejecutable", "output_esperado": "qué debe producir"},
    {"id": 2, "tarea": "...", "output_esperado": "..."}
  ]
}
Generá entre 3 y 5 pasos. Cada paso debe ser concreto y ejecutable.
Respondé SOLO con el JSON, sin texto adicional.'''

SYSTEM_EJECUTOR = '''Sos un agente ejecutor especializado.
Recibirás una tarea específica y el contexto acumulado de pasos anteriores.
Ejecutá la tarea y devolvé el resultado en 2-3 oraciones concretas.
Usá el contexto previo para que tu output sea coherente con lo ya hecho.'''

def planificar(meta):
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=600,
        system=SYSTEM_PLANIFICADOR,
        messages=[{'role':'user','content':f'Meta: {meta}'}]
    )
    return json.loads(resp.content[0].text)

def ejecutar_paso(paso, session_state):
    contexto = json.dumps(session_state['resultados'], ensure_ascii=False)
    prompt = f'''Tarea: {paso['tarea']}
Output esperado: {paso['output_esperado']}
Contexto de pasos anteriores: {contexto}'''
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=300,
        system=SYSTEM_EJECUTOR,
        messages=[{'role':'user','content':prompt}]
    )
    return resp.content[0].text

def correr_mision(meta):
    # Inicializar session state
    session_state = {
        'meta': meta,
        'plan': None,
        'paso_actual': 0,
        'resultados': {},
        'completado': False
    }

    # Fase 1: planificar
    print('Consejo Rebelde planificando...')
    plan = planificar(meta)
    session_state['plan'] = plan
    print(f'Plan generado: {len(plan["pasos"])} pasos')
    print()

    # Fase 2: ejecutar cada paso
    for paso in plan['pasos']:
        print(f'--- Paso {paso["id"]}: {paso["tarea"][:60]}...')
        resultado = ejecutar_paso(paso, session_state)
        session_state['resultados'][f'paso_{paso["id"]}'] = resultado
        session_state['paso_actual'] = paso['id']
        print(f'Resultado: {resultado[:120]}...')
        print()

    # Fase 3: síntesis final
    session_state['completado'] = True
    todos = json.dumps(session_state['resultados'], ensure_ascii=False)
    resp = client.messages.create(
        model='claude-sonnet-4-6', max_tokens=400,
        messages=[{'role':'user','content':
            f'Sintetizá estos resultados en un resumen ejecutivo:\n{todos}'}]
    )
    print('=== SÍNTESIS FINAL ===')
    print(resp.content[0].text)

correr_mision('Preparar el lanzamiento de un producto nuevo en el mercado')
