#!/usr/bin/env python3
"""
Spider-sense: hook PreToolUse que protege zonas sensibles del proyecto.
Recibe el contexto de la tool por stdin, devuelve decision por stdout.
"""
import sys, json, re

PROTECTED_PATHS = ['/secrets/', '.env', 'config.prod', 'credentials']
DANGEROUS_BASH = [r'rm\s+-rf', r'sudo\s+', r'curl.+\|\s*bash', r'chmod\s+777']

def spider_sense(event: dict) -> dict:
    tool_name  = event.get('tool_name', '')
    tool_input = event.get('tool_input', {})

    if tool_name in ('Write', 'Edit', 'MultiEdit'):
        path = tool_input.get('file_path', '') or tool_input.get('path', '')
        for protected in PROTECTED_PATHS:
            if protected in path:
                return {
                    'decision': 'block',
                    'reason': f'SPIDER-SENSE: {path} es zona protegida. Modificacion bloqueada.'
                }

    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        for protected in PROTECTED_PATHS:
            if protected in command:
                return {
                    'decision': 'block',
                    'reason': f'SPIDER-SENSE: El comando toca una zona protegida ({protected}). Modificacion bloqueada.'
                }
        for pattern in DANGEROUS_BASH:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    'decision': 'block',
                    'reason': f'SPIDER-SENSE: Comando peligroso detectado: {command[:60]}. Aprobacion manual requerida.'
                }
        print(f'[SPIDER-SENSE LOG] Bash permitido: {command[:80]}', file=sys.stderr)

    return {'decision': 'approve'}

if __name__ == '__main__':
    event = json.loads(sys.stdin.read())
    result = spider_sense(event)
    print(json.dumps(result))
