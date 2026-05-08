import anthropic, json, datetime, re
from typing import Any

client = anthropic.Anthropic()

# ── Audit trail ────────────────────────────────────────────────
audit_log = []

def log_action(tool_name: str, args: dict, result: Any,
               approved_by: str = 'auto', reversible: bool = True):
    audit_log.append({
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'tool': tool_name,
        'args_summary': str(args)[:120],   # sanitizado
        'result_summary': str(result)[:120],
        'reversible': reversible,
        'approved_by': approved_by
    })
    print(f'  📋 [AUDIT] {tool_name} | reversible={reversible} | aprobado por: {approved_by}')

# ── Guardrail de salida ─────────────────────────────────────────
SENSITIVE_PATTERN = re.compile(r'(password|token|secret|api_key)', re.IGNORECASE)

def output_guardrail(text: str) -> str:
    if SENSITIVE_PATTERN.search(text):
        print('  🛡️  [COLOSSUS-OUTPUT] Dato sensible detectado — RETENIDO para revisión')
        return '[RESPUESTA RETENIDA: contiene información sensible. Revisar antes de enviar.]'
    return text

# ── HITL simulation ─────────────────────────────────────────────
def colossus_approve(action: str, details: str) -> bool:
    print(f'\n  🦾 [COLOSSUS] Acción IRREVERSIBLE detectada: {action}')
    print(f'     Detalles: {details}')
    respuesta = input('     ¿Aprobar? (s/n): ').strip().lower()
    aprobado = respuesta == 's'
    print(f'     → {"APROBADO" if aprobado else "RECHAZADO"} por: operador_humano')
    return aprobado

# ── Tools ───────────────────────────────────────────────────────
TOOLS = [
    {
        'name': 'leer_expediente',
        'description': 'Lee el expediente de un objetivo. ACCIÓN REVERSIBLE — no modifica datos. Args: objetivo (str) — nombre del objetivo a consultar.',
        'input_schema': {'type': 'object', 'properties': {
            'objetivo': {'type': 'string', 'description': 'Nombre del objetivo'}
        }, 'required': ['objetivo']}
    },
    {
        'name': 'redactar_informe',
        'description': 'Redacta un informe de misión. ACCIÓN REVERSIBLE — solo crea borrador. Args: contenido (str) — cuerpo del informe.',
        'input_schema': {'type': 'object', 'properties': {
            'contenido': {'type': 'string'}
        }, 'required': ['contenido']}
    },
    {
        'name': 'enviar_mensaje_campo',
        'description': 'Envía un mensaje al agente en campo. ACCIÓN IRREVERSIBLE — requiere aprobación HITL. Args: destinatario (str), mensaje (str).',
        'input_schema': {'type': 'object', 'properties': {
            'destinatario': {'type': 'string'},
            'mensaje': {'type': 'string'}
        }, 'required': ['destinatario', 'mensaje']}
    },
]

# ── Mapa de reversibilidad ──────────────────────────────────────
REVERSIBILITY = {
    'leer_expediente': True,
    'redactar_informe': True,
    'enviar_mensaje_campo': False,   # ← Irreversible → HITL
}

# ── Ejecutor con Colossus ────────────────────────────────────────
def ejecutar_tool(name: str, args: dict):
    reversible = REVERSIBILITY.get(name, False)

    # Guardrail de entrada: validar campos requeridos
    if name == 'enviar_mensaje_campo':
        if not args.get('destinatario') or not args.get('mensaje'):
            return {'error': 'campos_requeridos_ausentes',
                    'causa': 'destinatario y mensaje son obligatorios'}

    # HITL para acciones irreversibles
    if not reversible:
        aprobado = colossus_approve(name, str(args))
        if not aprobado:
            log_action(name, args, 'RECHAZADO', 'operador_humano', reversible)
            return {'estado': 'rechazado_por_hitl', 'accion': name}

    # Simulación de ejecución
    if name == 'leer_expediente':
        resultado = {'expediente': args['objetivo'], 'estado': 'activo', 'nivel_amenaza': 'alto'}
    elif name == 'redactar_informe':
        resultado = {'borrador_creado': True, 'palabras': len(args['contenido'].split())}
    else:  # enviar_mensaje_campo
        resultado = {'enviado': True, 'destinatario': args['destinatario']}

    aprobador = 'operador_humano' if not reversible else 'auto'
    log_action(name, args, resultado, aprobador, reversible)
    return resultado

# ── Agentic loop con guardrails ──────────────────────────────────
def agente_deadpool(mision: str):
    print(f'\n🔴 [DEADPOOL] Iniciando misión: {mision}')
    print('🦾 [COLOSSUS] Guardrails activos. Monitoreando.\n')

    messages = [{'role': 'user', 'content': mision}]

    while True:
        response = client.messages.create(
            model='claude-sonnet-4-6', max_tokens=1024, tools=TOOLS, messages=messages
        )

        if response.stop_reason == 'end_turn':
            # Guardrail de salida
            texto_final = response.content[0].text
            texto_final = output_guardrail(texto_final)
            print(f'\n✅ [DEADPOOL] Misión completada: {texto_final}')
            break

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    print(f'\n⚡ [DEADPOOL] Quiere usar: {block.name}')
                    resultado = ejecutar_tool(block.name, block.input)
                    tool_results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': json.dumps(resultado)})

            messages.append({'role': 'assistant', 'content': response.content})
            messages.append({'role': 'user', 'content': tool_results})

    print('\n📋 AUDIT TRAIL COMPLETO:')
    for i, entry in enumerate(audit_log, 1):
        print(f'  {i}. [{entry["timestamp"]}] {entry["tool"]} | rev={entry["reversible"]} | by={entry["approved_by"]}')

# ── Entry point ──────────────────────────────────────────────────
agente_deadpool(
    'Necesito que investigues a Francis Freeman, prepares un informe de su nivel de amenaza, '
    'y luego avises al agente Colossus en campo sobre los resultados.'
)