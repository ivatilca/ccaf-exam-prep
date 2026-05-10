from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, Resource, Prompt,
    TextContent, ImageContent,
    GetPromptResult, PromptMessage
)
import asyncio
import json
from datetime import datetime

# El servidor tiene un nombre — es su identidad en el ecosistema MCP
app = Server('covert-mandaloriano')

# Base de datos en memoria — en producción sería una DB real
CONTRATOS_ACTIVOS = []
REGISTRO_GREMIO = {
    'moff_gideon': {'estado': 'buscado', 'recompensa': 1000000, 'peligrosidad': 'extrema'},
    'grogu': {'estado': 'protegido', 'recompensa': None, 'peligrosidad': 'ninguna'},
    'cara_dune': {'estado': 'aliada', 'recompensa': None, 'peligrosidad': 'alta_aliada'},
}

# ════════════════════════════════
# TOOL — aceptar_contrato
# ════════════════════════════════
@app.list_tools()
async def listar_tools():
    return [
        Tool(
            name='aceptar_contrato',
            description='Acepta un contrato de caza del Gremio de Cazarrecompensas. '
                        'Registra el objetivo, la recompensa y el plazo de entrega. '
                        'Usar cuando el cliente quiere tomar un nuevo trabajo. '
                        'No usar si el objetivo ya tiene un contrato activo.',
            inputSchema={
                'type': 'object',
                'properties': {
                    'objetivo': {
                        'type': 'string',
                        'description': 'Nombre o alias del objetivo del contrato'
                    },
                    'recompensa_creditos': {
                        'type': 'number',
                        'description': 'Valor del contrato en créditos imperiales'
                    },
                    'entrega': {
                        'type': 'string',
                        'enum': ['vivo', 'muerto', 'cualquiera'],
                        'description': 'Condición de entrega requerida por el cliente'
                    }
                },
                'required': ['objetivo', 'recompensa_creditos', 'entrega']
            }
        )
    ]

@app.call_tool()
async def ejecutar_tool(name: str, arguments: dict):
    if name == 'aceptar_contrato':
        objetivo = arguments['objetivo']
        recompensa = arguments['recompensa_creditos']
        entrega = arguments['entrega']

        # Validación de negocio
        if any(c['objetivo'] == objetivo for c in CONTRATOS_ACTIVOS):
            return [TextContent(type='text',
                text=f'Error: {objetivo} ya tiene un contrato activo. '
                     f'Completá el contrato existente antes de aceptar uno nuevo.')]

        contrato = {
            'id': f'CTR-{len(CONTRATOS_ACTIVOS)+1:04d}',
            'objetivo': objetivo,
            'recompensa': recompensa,
            'entrega': entrega,
            'fecha': datetime.now().isoformat()
        }
        CONTRATOS_ACTIVOS.append(contrato)
        return [TextContent(type='text',
            text=f'Contrato {contrato["id"]} aceptado. '
                 f'Objetivo: {objetivo}. Recompensa: {recompensa} créditos. '
                 f'Condición: {entrega}. This is the Way.')]

    return [TextContent(type='text', text=f'Tool desconocida: {name}')]

# ═══════════════════════════════════════
# RESOURCE — base_de_datos_gremio
# ═══════════════════════════════════════
@app.list_resources()
async def listar_resources():
    return [Resource(
        uri='covert://gremio/registro',
        name='Registro del Gremio de Cazarrecompensas',
        description='Base de datos de objetivos conocidos. Solo lectura. '
                    'Contiene estado, recompensa y nivel de peligrosidad.',
        mimeType='application/json'
    )]

@app.read_resource()
async def leer_resource(uri):
    if 'gremio/registro' in str(uri):
        return json.dumps(REGISTRO_GREMIO, ensure_ascii=False, indent=2)
    raise ValueError(f'Resource no encontrado: {uri}')

# ═══════════════════════════════════════
# PROMPT — iniciar_caceria
# ═══════════════════════════════════════
@app.list_prompts()
async def listar_prompts():
    return [Prompt(
        name='iniciar_caceria',
        description='Template para iniciar una operación de caza. '
                    'Incluye verificación del registro y aceptación del contrato.',
    )]

@app.get_prompt()
async def obtener_prompt(name: str, arguments: dict | None):
    if name == 'iniciar_caceria':
        return GetPromptResult(messages=[
            PromptMessage(role='user', content=TextContent(type='text', text=
                'Iniciando operación de caza. Primero consultá el registro del Gremio '
                'para verificar el estado del objetivo. Si está disponible, aceptá el '
                'contrato con las condiciones del cliente. Confirmá cada paso. '
                'This is the Way.'
            ))
        ])
    raise ValueError(f'Prompt no encontrado: {name}')

# ═══════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════
if __name__ == '__main__':
    print('Covert activo. Esperando clientes...', flush=True)
    asyncio.run(stdio_server(app))
