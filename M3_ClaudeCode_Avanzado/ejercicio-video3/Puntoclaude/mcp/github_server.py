#!/usr/bin/env python3
"""
rebel-github: servidor MCP HTTP que simula la API de GitHub.
Expone 4 tools: list_issues, get_file, create_pr, merge_branch.
"""
# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP('rebel-github', host='127.0.0.1', port=8080)

ISSUES = [
    {'id': 1, 'title': 'Fix login timeout', 'state': 'open', 'labels': ['bug']},
    {'id': 2, 'title': 'Add dark mode', 'state': 'open', 'labels': ['enhancement']},
    {'id': 3, 'title': 'Update README', 'state': 'closed', 'labels': ['docs']},
]

FILES = {
    'README.md': '# Rebel Ops\nProyecto de operaciones del equipo rebel.',
    'main.py': 'from flask import Flask\napp = Flask(__name__)\n',
    '.env': 'SECRET_KEY=supersecreta\nDB_URL=postgres://...',
}

PRS = []

@mcp.tool()
def list_issues(query: str = '', state: str = 'open') -> str:
    """Lista issues del repositorio. Filtrar por query y estado."""
    results = [
        i for i in ISSUES
        if (state == 'all' or i['state'] == state)
        and (query.lower() in i['title'].lower() if query else True)
    ]
    return json.dumps(results)

@mcp.tool()
def get_file(path: str) -> str:
    """Obtiene el contenido de un archivo del repositorio."""
    content = FILES.get(path)
    if content is None:
        return json.dumps({'error': f'archivo no encontrado: {path}'})
    return json.dumps({'path': path, 'content': content})

@mcp.tool()
def create_pr(title: str, body: str, base: str = 'main', head: str = 'feature') -> str:
    """Crea un Pull Request en el repositorio."""
    pr = {'id': len(PRS) + 1, 'title': title, 'body': body, 'base': base, 'head': head, 'state': 'open'}
    PRS.append(pr)
    return json.dumps({'ok': True, 'pr': pr})

@mcp.tool()
def merge_branch(pr_id: int) -> str:
    """Mergea un Pull Request. Requiere aprobacion humana."""
    return json.dumps({'ok': True, 'merged': pr_id})

if __name__ == '__main__':
    mcp.run(transport='streamable-http')
