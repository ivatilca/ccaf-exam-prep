from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, Prompt, TextContent
import asyncio, json

app = Server('r2d2')

# ══════════════════════════════════
# PRIMITIVA 1: TOOL — hackear_puerta
# ══════════════════════════════════
@app.list_tools()
async def listar_tools():
    return [Tool(
        name='hackear_puerta',
        description='Hackea el sistema de cierre de una puerta en la instalación. '
                    'Puede abrir o cerrar. Requiere el ID del panel de control.',
        inputSchema={
            'type': 'object',
            'properties': {
                'panel_id': {'type': 'string', 'description': 'ID del panel de control'},
                'accion': {'type': 'string', 'enum': ['abrir', 'cerrar']}
            },
            're quired': ['panel_id', 'accion']
        }
    )]

@app.call_tool()
async def ejecutar_tool(name, arguments):
    if name == 'hackear_puerta':
        panel = arguments['panel_id']
        accion = arguments['accion']
        return [TextContent(type='text',
            text=f'Panel {panel}: puerta {accion}da exitosamente. Acceso {'concedido' if accion=="abrir" else 'bloqueado'}.'
        )]
# ═══════════════════════════════════════════════
# PRIMITIVA 2: RESOURCE — planos de la Estrella
# ═══════════════════════════════════════════════
@app.list_resources()
async def listar_resources():
    return [Resource(
        uri='r2d2://planos/estrella-de-la-muerte',
        name='Planos de la Estrella de la Muerte',
        description='Planos técnicos completos de la Estrella de la Muerte. Solo lectura.',
        mimeType='application/json'
    )]

@app.read_resource()
async def leer_resource(uri):
    if 'estrella-de-la-muerte' in str(uri):
        datos = {
            'nombre': 'DS-1 Orbital Battle Station',
            'diametro_km': 160,
            'debilidad': 'Puerto de escape termal, 2 metros de diámetro',
            'ubicacion_puerto': 'Ecuador de la estación, tramo norte'
        }
        return json.dumps(datos, ensure_ascii=False)

# ════════════════════════════════════════════
# PRIMITIVA 3: PROMPT — iniciar misión rescate
# ════════════════════════════════════════════
@app.list_prompts()
async def listar_prompts():
    return [Prompt(
        name='iniciar_mision_rescate',
        description='Template para iniciar una misión de rescate en instalación imperial.',
    )]

@app.get_prompt()
async def obtener_prompt(name, arguments):
    if name == 'iniciar_mision_rescate':
        return {
            'messages': [{
                'role': 'user',
                'content': {'type': 'text', 'text':
                    'Iniciando protocolo de rescate. Primero, hackeá la puerta del sector de detención. '
                    'Después, recuperá los planos de la instalación para identificar la ruta de escape. '
                    'Reportá el estado en cada paso.'
                }
            }]
        }

if __name__ == '__main__':
    asyncio.run(stdio_server(app))
