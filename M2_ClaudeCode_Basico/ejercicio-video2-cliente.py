from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def usar_r2d2():
    params = StdioServerParameters(command='python', args=['servidor_r2d2.py'])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Descubrir capabilities
            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()
            print(f'Tools: {[t.name for t in tools.tools]}')
            print(f'Resources: {[r.name for r in resources.resources]}')
            print(f'Prompts: {[p.name for p in prompts.prompts]}')
            print()

            # Usar la TOOL
            resultado_tool = await session.call_tool(
                'hackear_puerta',
                {'panel_id': 'PANEL-AA-23', 'accion': 'abrir'}
            )
            print(f'TOOL: {resultado_tool.content[0].text}')

            # Leer el RESOURCE
            resultado_res = await session.read_resource('r2d2://planos/estrella-de-la-muerte')
            print(f'RESOURCE: {resultado_res.contents[0].text[:120]}...')

            # Obtener el PROMPT
            resultado_prompt = await session.get_prompt('iniciar_mision_rescate', {})
            print(f'PROMPT: {resultado_prompt["messages"][0]["content"]["text"][:100]}...')

asyncio.run(usar_r2d2())
